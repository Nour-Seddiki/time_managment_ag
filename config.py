"""Paths and tunables. Everything can be overridden with environment variables."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("FOCUS_AGENT_DATA", BASE_DIR / "data"))

# OAuth client secret downloaded from Google Cloud Console (Desktop app).
CREDENTIALS_FILE = Path(os.environ.get("FOCUS_AGENT_CREDENTIALS", BASE_DIR / "credentials.json"))
TOKEN_FILE = DATA_DIR / "token.json"
STATE_FILE = DATA_DIR / "state.json"

CALENDAR_ID = os.environ.get("FOCUS_AGENT_CALENDAR", "primary")

# Unset = whatever model your Claude account uses by default in Claude Code.
MODEL = os.environ.get("FOCUS_AGENT_MODEL") or None
# low | medium | high | xhigh | max. Chat check-ins are light work; medium is a good default.
EFFORT = os.environ.get("FOCUS_AGENT_EFFORT", "medium")

DEFAULT_FOCUS_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15
FOCUS_SESSIONS_BEFORE_LONG_BREAK = 4
