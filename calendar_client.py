"""Google Calendar access (OAuth desktop flow + the few calls the agent needs)."""
from datetime import datetime, timedelta

from . import config, timeutil

# Read/write events only; no access to calendar settings, sharing or other Google data.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
AGENT_MARK = "focus_agent"  # stored in extendedProperties.private.createdBy


class CalendarNotConnected(RuntimeError):
    pass


class CalendarClient:
    def __init__(self, calendar_id: str = config.CALENDAR_ID):
        self.calendar_id = calendar_id
        self._service = None

    @property
    def connected(self) -> bool:
        return self._service is not None

    def connect(self):
        """Load the cached token or run the browser consent flow once. Call at startup."""
        from google.auth.exceptions import RefreshError
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        creds = None
        if config.TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(config.TOKEN_FILE), SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:  # revoked or expired refresh token: consent again
                creds = None
        if not creds or not creds.valid:
            if not config.CREDENTIALS_FILE.exists():
                raise CalendarNotConnected(f"missing OAuth client file {config.CREDENTIALS_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(str(config.CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        config.TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        config.TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        self._service = build("calendar", "v3", credentials=creds, cache_discovery=False)

    @property
    def events(self):
        if self._service is None:
            raise CalendarNotConnected(
                "Google Calendar is not connected (see focus_agent/README.md). "
                "Tasks and timers still work."
            )
        return self._service.events()

    # ---- reads ----------------------------------------------------------

    def list_events(self, start: datetime, end: datetime, query: str | None = None, limit: int = 50):
        resp = self.events.list(
            calendarId=self.calendar_id,
            timeMin=timeutil.fmt(start),
            timeMax=timeutil.fmt(end),
            singleEvents=True,
            orderBy="startTime",
            maxResults=limit,
            q=query,
        ).execute()
        return [_simplify(e) for e in resp.get("items", []) if e.get("status") != "cancelled"]

    def free_slots(self, start: datetime, end: datetime, min_minutes: int = 25):
        """Gaps between timed, non-transparent events. All-day events are ignored (usually reminders)."""
        busy = []
        for e in self.list_events(start, end, limit=250):
            if e["all_day"] or e["transparent"] or e["declined"]:
                continue
            busy.append((max(timeutil.parse(e["start"]), start), min(timeutil.parse(e["end"]), end)))
        busy.sort()
        slots, cursor = [], start
        for b_start, b_end in busy:
            if b_start > cursor:
                slots.append((cursor, b_start))
            cursor = max(cursor, b_end)
        if cursor < end:
            slots.append((cursor, end))
        min_len = timedelta(minutes=min_minutes)
        return [
            {"start": timeutil.fmt(s), "end": timeutil.fmt(e), "minutes": int((e - s).total_seconds() // 60)}
            for s, e in slots
            if e - s >= min_len
        ]

    # ---- writes ---------------------------------------------------------

    def create_event(self, title, start: datetime, end: datetime, description=None, color_id=None):
        body = {
            "summary": title,
            "start": {"dateTime": timeutil.fmt(start)},
            "end": {"dateTime": timeutil.fmt(end)},
            "extendedProperties": {"private": {"createdBy": AGENT_MARK}},
        }
        if description:
            body["description"] = description
        if color_id:
            body["colorId"] = str(color_id)
        return _simplify(self.events.insert(calendarId=self.calendar_id, body=body).execute())

    def update_event(self, event_id, title=None, start: datetime | None = None, end: datetime | None = None,
                     description=None):
        body = {}
        if title is not None:
            body["summary"] = title
        if description is not None:
            body["description"] = description
        if start is not None:
            body["start"] = {"dateTime": timeutil.fmt(start)}
        if end is not None:
            body["end"] = {"dateTime": timeutil.fmt(end)}
        resp = self.events.patch(calendarId=self.calendar_id, eventId=event_id, body=body).execute()
        return _simplify(resp)

    def delete_event(self, event_id):
        self.events.delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def get_event(self, event_id):
        return _simplify(self.events.get(calendarId=self.calendar_id, eventId=event_id).execute())


def _simplify(e: dict) -> dict:
    start, end = e.get("start", {}), e.get("end", {})
    all_day = "date" in start
    me = next((a for a in e.get("attendees", []) if a.get("self")), {})
    return {
        "id": e["id"],
        "title": e.get("summary", "(no title)"),
        "start": start.get("dateTime") or start.get("date"),
        "end": end.get("dateTime") or end.get("date"),
        "all_day": all_day,
        "location": e.get("location"),
        "description": (e.get("description") or "")[:300] or None,
        "transparent": e.get("transparency") == "transparent",
        "declined": me.get("responseStatus") == "declined",
        "created_by_focus_agent": e.get("extendedProperties", {}).get("private", {}).get("createdBy") == AGENT_MARK,
    }
