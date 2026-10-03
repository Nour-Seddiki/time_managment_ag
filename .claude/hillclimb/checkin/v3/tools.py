"""Tool schemas exposed to Claude and their implementations."""
import json
from datetime import timedelta

from . import config, timeutil
from .calendar_client import CalendarClient, CalendarNotConnected
from .sessions import SessionManager
from .store import Store

_ISO = "Local time, ISO 8601 (e.g. 2026-10-03T14:00)."


def _tool(name, description, properties=None, required=()):
    return {
        "name": name,
        "description": description,
        "input_schema": {"type": "object", "properties": properties or {}, "required": list(required)},
    }


TOOLS = [
    # ---- calendar ----
    _tool(
        "list_calendar_events",
        "List the student's Google Calendar events between two times (classes, exams, study blocks, "
        "personal plans). Use before planning or suggesting what to do next.",
        {
            "start": {"type": "string", "description": _ISO},
            "end": {"type": "string", "description": _ISO},
            "query": {"type": "string", "description": "Optional free-text filter, e.g. 'exam'."},
        },
        ["start", "end"],
    ),
    _tool(
        "find_free_slots",
        "Find free gaps in the calendar between two times that are at least min_minutes long.",
        {
            "start": {"type": "string", "description": _ISO},
            "end": {"type": "string", "description": _ISO},
            "min_minutes": {"type": "integer", "description": "Minimum gap length. Default 25."},
        },
        ["start", "end"],
    ),
    _tool(
        "create_calendar_event",
        "Create a calendar event, e.g. a planned study block. Only after the student agreed to it.",
        {
            "title": {"type": "string"},
            "start": {"type": "string", "description": _ISO},
            "end": {"type": "string", "description": _ISO},
            "description": {"type": "string"},
        },
        ["title", "start", "end"],
    ),
    _tool(
        "update_calendar_event",
        "Rename or move a calendar event. For events not created by you (created_by_focus_agent=false), "
        "ask the student first.",
        {
            "event_id": {"type": "string"},
            "title": {"type": "string"},
            "start": {"type": "string", "description": _ISO},
            "end": {"type": "string", "description": _ISO},
            "description": {"type": "string"},
        },
        ["event_id"],
    ),
    _tool(
        "delete_calendar_event",
        "Delete a calendar event. Always get the student's explicit yes in the conversation first.",
        {"event_id": {"type": "string"}},
        ["event_id"],
    ),
    # ---- tasks ----
    _tool(
        "add_task",
        "Add a study task (assignment, reading, revision, project work) to the student's task list.",
        {
            "title": {"type": "string"},
            "course": {"type": "string"},
            "estimate_minutes": {"type": "integer"},
            "due": {"type": "string", "description": "Deadline. " + _ISO},
            "priority": {"type": "string", "enum": ["high", "medium", "low"]},
            "notes": {"type": "string"},
        },
        ["title"],
    ),
    _tool(
        "list_tasks",
        "List tasks, sorted by due date then priority. Includes focus_minutes already spent.",
        {"status": {"type": "string", "enum": ["open", "done", "all"], "description": "Default open."}},
    ),
    _tool(
        "update_task",
        "Edit a task, or mark it done with status='done'.",
        {
            "task_id": {"type": "string"},
            "title": {"type": "string"},
            "status": {"type": "string", "enum": ["open", "done"]},
            "estimate_minutes": {"type": "integer"},
            "due": {"type": "string", "description": _ISO},
            "priority": {"type": "string", "enum": ["high", "medium", "low"]},
            "notes": {"type": "string"},
        },
        ["task_id"],
    ),
    # ---- focus sessions ----
    _tool(
        "start_session",
        "Start a focus or break timer. When it runs out you'll receive an [EVENT] message and should "
        "check in with the student. Call it as soon as the student picks a next step (their choice is "
        "the agreement, so don't ask them to confirm again); never start one they haven't chosen.",
        {
            "kind": {"type": "string", "enum": ["focus", "break"]},
            "minutes": {"type": "integer", "description": f"Default {config.DEFAULT_FOCUS_MINUTES} for focus."},
            "label": {"type": "string", "description": "What the student is working on, or 'Short break'."},
            "task_id": {"type": "string", "description": "Link a focus session to a task."},
            "block_calendar": {
                "type": "boolean",
                "description": "Also add the session to Google Calendar so others see the student is busy.",
            },
        },
        ["kind", "label"],
    ),
    _tool(
        "extend_session",
        "Add minutes to the running session (e.g. 'give me 10 more minutes').",
        {"minutes": {"type": "integer"}},
        ["minutes"],
    ),
    _tool(
        "stop_session",
        "Stop the running session early (student is done, interrupted, or wants to switch).",
        {"reason": {"type": "string", "enum": ["stopped_early", "interrupted", "switched_task"]}},
    ),
    _tool(
        "session_status",
        "Running session (minutes remaining), today's focus totals, current streak and suggested break length.",
    ),
    _tool(
        "log_session_reflection",
        "Save the student's check-in about the session that just ended: focus rating 1-5 and notes "
        "(what got done, blockers, energy).",
        {
            "focus_rating": {"type": "integer", "minimum": 1, "maximum": 5},
            "notes": {"type": "string"},
        },
    ),
    _tool(
        "daily_summary",
        "Focus sessions logged on a day with ratings and notes, plus tasks completed. For end-of-day reviews.",
        {"day": {"type": "string", "description": "Date, e.g. 2026-10-03. Default today."}},
    ),
]


class ToolBox:
    def __init__(self, store: Store, calendar: CalendarClient, sessions: SessionManager):
        self.store = store
        self.calendar = calendar
        self.sessions = sessions

    def execute(self, name: str, args: dict) -> tuple[str, bool]:
        """Returns (json_result, is_error). Errors go back to Claude as tool_result errors."""
        handler = getattr(self, f"_{name}", None)
        if handler is None:
            return f"Unknown tool {name}", True
        try:
            return json.dumps(handler(**args), ensure_ascii=False, default=str), False
        except CalendarNotConnected as e:
            return str(e), True
        except (ValueError, TypeError, KeyError) as e:
            return f"{type(e).__name__}: {e}", True
        except Exception as e:  # Google HttpError, network, etc.
            return f"{type(e).__name__}: {e}", True

    def schedule_context(self) -> str:
        """What's coming up, attached to app events so check-ins are sized around real time limits."""
        now = timeutil.now()
        lines = [f"Coming up (now {now:%a %H:%M}):"]

        def when(dt):
            mins = int((dt - now).total_seconds() // 60)
            days = (dt.date() - now.date()).days
            if mins < 0:
                return "now"
            if mins < 120:
                return f"{dt:%H:%M}, in {mins} min"
            if days == 0:
                return f"today {dt:%H:%M}, in {mins // 60}h{mins % 60:02d}"
            if days == 1:
                return f"tomorrow {dt:%a %H:%M}, in {mins // 60}h{mins % 60:02d}"
            return f"{dt:%a %d %b %H:%M}, in {days} days"  # explicit date: "Mon" alone reads as today

        try:
            events = [e for e in self.calendar.list_events(now, now + timedelta(hours=18))
                      if not e["all_day"] and not e["declined"]]
            for e in events[:3]:
                start, end = timeutil.parse(e["start"]), timeutil.parse(e["end"])
                status = f"until {end:%H:%M}" if start <= now else when(start)
                lines.append(f"- {e['title']} ({status})")
            if not events:
                lines.append("- Calendar: nothing in the next 18 hours")
        except CalendarNotConnected:
            lines.append("- Calendar: not connected")
        due = [t for t in self.store.list_tasks("open") if t["due"]][:3]
        for t in due:
            lines.append(f"- Due: {t['title']} ({when(timeutil.parse(t['due']))})")
        return "\n".join(lines)

    # ---- calendar ----

    def _list_calendar_events(self, start, end, query=None):
        return self.calendar.list_events(timeutil.parse(start), timeutil.parse(end), query=query)

    def _find_free_slots(self, start, end, min_minutes=25):
        return self.calendar.free_slots(timeutil.parse(start), timeutil.parse(end), min_minutes)

    def _create_calendar_event(self, title, start, end, description=None):
        return self.calendar.create_event(title, timeutil.parse(start), timeutil.parse(end), description)

    def _update_calendar_event(self, event_id, title=None, start=None, end=None, description=None):
        return self.calendar.update_event(
            event_id,
            title=title,
            start=timeutil.parse(start) if start else None,
            end=timeutil.parse(end) if end else None,
            description=description,
        )

    def _delete_calendar_event(self, event_id):
        self.calendar.delete_event(event_id)
        return {"deleted": event_id}

    # ---- tasks ----

    def _add_task(self, title, course=None, estimate_minutes=None, due=None, priority="medium", notes=None):
        if due:
            due = timeutil.fmt(timeutil.parse(due))
        return self.store.add_task(title, course, estimate_minutes, due, priority, notes)

    def _list_tasks(self, status="open"):
        return self.store.list_tasks(status)

    def _update_task(self, task_id, **fields):
        if fields.get("due"):
            fields["due"] = timeutil.fmt(timeutil.parse(fields["due"]))
        task = self.store.update_task(task_id, **fields)
        if task is None:
            raise KeyError(f"no task with id {task_id}")
        return task

    # ---- sessions ----

    def _start_session(self, kind, label, minutes=None, task_id=None, block_calendar=False):
        if minutes is None:
            minutes = config.DEFAULT_FOCUS_MINUTES if kind == "focus" else self.sessions.suggested_break()
        if not 1 <= minutes <= 180:
            raise ValueError("minutes must be between 1 and 180")
        if task_id and self.store.get_task(task_id) is None:
            raise KeyError(f"no task with id {task_id}")
        event_id, note = None, None
        if block_calendar and kind == "focus":
            start = timeutil.now()
            try:
                event = self.calendar.create_event(f"🎯 Focus: {label}", start, start + timedelta(minutes=minutes))
                event_id = event["id"]
            except CalendarNotConnected:
                note = "Calendar not connected; timer started without a calendar block."
        session = self.sessions.start(kind, minutes, label, task_id, calendar_event_id=event_id)
        return {"started": session, "note": note} if note else {"started": session}

    def _extend_session(self, minutes):
        session = self.sessions.extend(minutes)
        if session.get("calendar_event_id"):
            self.calendar.update_event(session["calendar_event_id"], end=timeutil.parse(session["ends_at"]))
        return session

    def _stop_session(self, reason="stopped_early"):
        session = self.sessions.stop(reason)
        if session.get("calendar_event_id"):
            # Shrink the calendar block to what actually happened.
            self.calendar.update_event(session["calendar_event_id"], end=timeutil.parse(session["end"]))
        return session

    def _session_status(self):
        return self.sessions.status()

    def _log_session_reflection(self, focus_rating=None, notes=None):
        last = self.store.update_last_session(focus_rating=focus_rating, reflection=notes)
        if last is None:
            raise ValueError("No session to reflect on yet.")
        return last

    def _daily_summary(self, day=None):
        start, end = timeutil.day_bounds(day)
        sessions = self.store.sessions_between(start, end)
        done = [t for t in self.store.list_tasks("done") if t["completed"] and start <= timeutil.parse(t["completed"]) < end]
        focus = [s for s in sessions if s["kind"] == "focus"]
        return {
            "day": start.date().isoformat(),
            "focus_sessions": len(focus),
            "focus_minutes": sum(s["actual_minutes"] for s in focus),
            "sessions": sessions,
            "tasks_completed": done,
        }
