"""Local-time helpers. All times the agent sees are local ISO 8601 strings."""
from datetime import datetime, timedelta


def now() -> datetime:
    return datetime.now().astimezone().replace(microsecond=0)


def parse(value: str) -> datetime:
    """Parse ISO 8601; naive values are interpreted as local time (DST-correct for that date)."""
    dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    return dt.astimezone() if dt.tzinfo is None else dt


def fmt(dt: datetime) -> str:
    return dt.astimezone().replace(microsecond=0).isoformat()


def stamp(dt: datetime | None = None) -> str:
    """Human stamp prefixed to every message, e.g. 'Sat 2026-10-03 14:05'."""
    return (dt or now()).strftime("%a %Y-%m-%d %H:%M")


def day_bounds(day: str | None = None) -> tuple[datetime, datetime]:
    start = parse(day) if day else now()
    start = start.replace(hour=0, minute=0, second=0)
    return start, start + timedelta(days=1)
