"""Focus/break timer. A ticker thread compares wall-clock time so a laptop sleep can't stall it."""
import sys
import threading
import time
import uuid
from datetime import timedelta

from . import config, timeutil
from .store import Store

_ES_CONTINUOUS = 0x80000000
_ES_SYSTEM_REQUIRED = 0x00000001


def _keep_awake(on: bool):
    """Stop Windows Modern Standby from suspending the process mid-session."""
    if sys.platform == "win32":
        import ctypes

        flags = _ES_CONTINUOUS | (_ES_SYSTEM_REQUIRED if on else 0)
        ctypes.windll.kernel32.SetThreadExecutionState(flags)


class SessionManager:
    def __init__(self, store: Store, on_event):
        """on_event(dict) is called from the ticker thread when a session runs out."""
        self.store = store
        self.on_event = on_event
        self.active: dict | None = None
        self._lock = threading.Lock()
        threading.Thread(target=self._tick, daemon=True, name="session-ticker").start()

    def start(self, kind: str, minutes: int, label: str, task_id: str | None = None,
              calendar_event_id: str | None = None) -> dict:
        with self._lock:
            if self.active:
                raise ValueError(f"A {self.active['kind']} session is already running: {self.active['label']}")
            start = timeutil.now()
            self.active = {
                "id": uuid.uuid4().hex[:6],
                "kind": kind,
                "label": label,
                "task_id": task_id,
                "planned_minutes": minutes,
                "start": timeutil.fmt(start),
                "ends_at": timeutil.fmt(start + timedelta(minutes=minutes)),
                "calendar_event_id": calendar_event_id,
            }
            _keep_awake(True)
            return dict(self.active)

    def extend(self, minutes: int) -> dict:
        with self._lock:
            if not self.active:
                raise ValueError("No session is running.")
            ends = timeutil.parse(self.active["ends_at"]) + timedelta(minutes=minutes)
            self.active["ends_at"] = timeutil.fmt(ends)
            self.active["planned_minutes"] += minutes
            return dict(self.active)

    def stop(self, outcome: str = "stopped_early") -> dict:
        with self._lock:
            if not self.active:
                raise ValueError("No session is running.")
            return self._finish(outcome)

    def status(self) -> dict:
        start, end = timeutil.day_bounds()
        today = [s for s in self.store.sessions_between(start, end) if s["kind"] == "focus"]
        out = {
            "active": None,
            "focus_sessions_today": len(today),
            "focus_minutes_today": sum(s["actual_minutes"] for s in today),
            "focus_streak_since_long_break": self._streak(),
            "suggested_break_minutes": self.suggested_break(),
        }
        with self._lock:
            if self.active:
                remaining = timeutil.parse(self.active["ends_at"]) - timeutil.now()
                out["active"] = {**self.active, "minutes_remaining": max(0, round(remaining.total_seconds() / 60))}
        return out

    def suggested_break(self) -> int:
        streak = self._streak()
        if streak and streak % config.FOCUS_SESSIONS_BEFORE_LONG_BREAK == 0:
            return config.LONG_BREAK_MINUTES
        return config.SHORT_BREAK_MINUTES

    # ---- internals ------------------------------------------------------

    def _streak(self) -> int:
        """Focus sessions since the last long break (or since the start of the day)."""
        start, end = timeutil.day_bounds()
        streak = 0
        for s in reversed(self.store.sessions_between(start, end)):
            if s["kind"] == "break" and s["actual_minutes"] >= config.LONG_BREAK_MINUTES:
                break
            streak += s["kind"] == "focus" and s["actual_minutes"] >= 10
        return streak

    def _finish(self, outcome: str) -> dict:
        session, self.active = self.active, None
        end = timeutil.now()
        session.update(
            end=timeutil.fmt(end),
            actual_minutes=round((end - timeutil.parse(session["start"])).total_seconds() / 60),
            outcome=outcome,
        )
        session.pop("ends_at", None)
        self.store.log_session(session)
        _keep_awake(False)
        return session

    def _tick(self):
        while True:
            time.sleep(1)
            with self._lock:
                if not self.active or timeutil.now() < timeutil.parse(self.active["ends_at"]):
                    continue
                session = self._finish("completed")
            self.on_event({"type": "session_ended", "session": session})
