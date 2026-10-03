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

# Voice mode (python -m focus_agent with FOCUS_VOICE=1, run.ps1 -Voice, or /voice in the chat).
VOICE = os.environ.get("FOCUS_VOICE", "") == "1"
# Speech model: FOCUS_STT_MODEL, else the best Whisper already downloaded into MODELS_DIR (kept
# outside the project so cloud-synced folders like OneDrive don't upload gigabytes of weights) or
# data/models/, else openai/whisper-base from the Hugging Face hub (~290 MB).
MODELS_DIR = Path(os.environ.get("FOCUS_MODELS_DIR")
                  or Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache")) / "FocusAgent" / "models")
_LOCAL_STT = [base / name for name in ("whisper-large-v3-turbo", "whisper-small", "whisper-base")
              for base in (MODELS_DIR, DATA_DIR / "models")]
STT_MODEL = os.environ.get("FOCUS_STT_MODEL") or next(
    (str(p) for p in _LOCAL_STT if (p / "model.safetensors").exists()), "openai/whisper-base")
TTS_VOICE = os.environ.get("FOCUS_TTS_VOICE", "en-US-EmmaMultilingualNeural")  # speaks en and fr
TTS_RATE = os.environ.get("FOCUS_TTS_RATE", "+5%")

DEFAULT_FOCUS_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15
FOCUS_SESSIONS_BEFORE_LONG_BREAK = 4
