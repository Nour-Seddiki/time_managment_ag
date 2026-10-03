"""Tiny JSON store for tasks and the focus-session log."""
import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

from . import timeutil


class Store:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.RLock()  # the session ticker thread writes too
        self.data = {"tasks": [], "sessions": []}
        if path.exists():
            self.data.update(json.loads(path.read_text(encoding="utf-8")))

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)

    # ---- tasks ----------------------------------------------------------

    def add_task(self, title, course=None, estimate_minutes=None, due=None, priority="medium", notes=None):
        task = {
            "id": uuid.uuid4().hex[:6],
            "title": title,
            "course": course,
            "estimate_minutes": estimate_minutes,
            "due": due,
            "priority": priority,
            "status": "open",
            "focus_minutes": 0,
            "notes": notes,
            "created": timeutil.fmt(timeutil.now()),
            "completed": None,
        }
        with self._lock:
            self.data["tasks"].append(task)
            self._save()
        return task

    def get_task(self, task_id):
        return next((t for t in self.data["tasks"] if t["id"] == task_id), None)

    def list_tasks(self, status="open"):
        tasks = [t for t in self.data["tasks"] if status == "all" or t["status"] == status]
        rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (t["due"] or "9999", rank.get(t["priority"], 1)))

    def update_task(self, task_id, **fields):
        with self._lock:
            task = self.get_task(task_id)
            if task is None:
                return None
            task.update({k: v for k, v in fields.items() if v is not None})
            if fields.get("status") == "done" and not task["completed"]:
                task["completed"] = timeutil.fmt(timeutil.now())
            self._save()
            return task

    # ---- sessions -------------------------------------------------------

    def log_session(self, session: dict):
        with self._lock:
            self.data["sessions"].append(session)
            if session["kind"] == "focus" and session.get("task_id"):
                task = self.get_task(session["task_id"])
                if task:
                    task["focus_minutes"] += session["actual_minutes"]
            self._save()

    def last_session(self):
        return self.data["sessions"][-1] if self.data["sessions"] else None

    def update_last_session(self, **fields):
        with self._lock:
            last = self.last_session()
            if last is None:
                return None
            last.update({k: v for k, v in fields.items() if v is not None})
            self._save()
            return last

    def sessions_between(self, start: datetime, end: datetime):
        return [s for s in self.data["sessions"] if start <= timeutil.parse(s["start"]) < end]
