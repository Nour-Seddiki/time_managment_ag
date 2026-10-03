# Focus: a study-schedule and time-management agent

Focus is a chat agent that runs in your terminal. It reads and writes your Google Calendar, keeps a
task list, and runs focus/break timers. **When a session ends, it starts the conversation itself.**
It asks how the session went, then helps you choose what's next: keep going, switch tasks, or take
a break. It sizes that next block around your upcoming classes.

```
Focus: Morning! You have Linear Algebra at 10:00 and the Physics lab report is due Monday.
       Want to (1) do a 45-min block on the lab report before class, (2) plan the whole day, or (3) something else?
you> 1
  · start_session
Focus: Timer's running, 45 min on the lab report. Ends at 9:47. Go!

⏰ [Sat 2026-10-03 09:47] focus session finished
Focus: Done! How did that go? A 1-5 focus rating is plenty.
you> 4, finished the intro and method
  · log_session_reflection
  · list_calendar_events
Focus: Nice progress. Lecture starts in 13 min, so: (1) 5-min break then head out, or (2) a quick 10-min review of last week's notes?
```

## How it works

| File | Role |
|---|---|
| `agent.py` | Claude Agent SDK client (your Claude account), the coaching prompt, and the tool wrappers |
| `tools.py` | 14 tools: calendar, tasks, timers, reflections, daily summary |
| `calendar_client.py` | Google Calendar OAuth + events/free-slot logic |
| `sessions.py` | Timer thread. Fires an event when a session ends and keeps Windows from sleeping mid-session |
| `store.py` | Tasks and the session log in `data/state.json` |
| `voice.py` | Voice mode: mic + local Whisper speech recognition, neural text-to-speech |
| `__main__.py` | Terminal app. Your typing and timer events feed one queue |

Safety rules in the prompt: Focus proposes a plan before it writes study blocks to your calendar.
It asks before moving or deleting events, and it never starts a timer you didn't agree to. The
OAuth scope is `calendar.events` only, so it can't touch your calendar settings, sharing, or other
Google data. Events it creates are tagged, so it can tell them apart from your classes.

## Setup

### 0. Get the code
The repo is the `focus_agent` Python package itself, so clone it under that name:
```powershell
git clone https://github.com/Nour-Seddiki/time_managment_ag.git focus_agent
pip install -r focus_agent/requirements.txt
```

### 1. Your Claude account (no API key)
Focus runs on the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview). The SDK
drives your locally installed Claude Code, so it uses the Claude account you're logged in to there,
and usage counts against your plan. You need Claude Code installed and logged in once:
```powershell
claude        # then type /login if it asks
```
Claude Code's built-in tools are turned off, so the coach can't read files or run commands. It
also doesn't load your Claude Code settings or memories, and it only sees its 14 study tools.

> Account login is for **your own personal use**. Anthropic doesn't allow apps you give to other
> people to use claude.ai login. If you share Focus, each person needs their own API key
> (`ANTHROPIC_API_KEY`). The SDK picks that up automatically when it's set.

### 2. Google Calendar access (one time, about 5 minutes)
1. Go to <https://console.cloud.google.com/> and create a project (e.g. "focus-agent").
2. **APIs & Services → Library** → search **Google Calendar API** → **Enable**. If you skip this,
   login still succeeds but every calendar call fails with `403 accessNotConfigured`.
3. **Google Auth Platform → Get started**: enter the app name and support email, set Audience to
   **External**, enter your contact email, accept the policy, then **Create**.
4. **Audience → Test users → Add users**: add your own Gmail address.
5. **Clients → Create client** → Application type **Desktop app** → **Create** → **Download JSON**.
6. Save the downloaded file as `focus_agent/credentials.json`.

On first launch, a browser window asks you to allow calendar access. Google shows "hasn't verified
this app"; click **Continue**, because it's your own app. The token is cached in `data/token.json`.
Both files are git-ignored. While the app is in Testing mode, Google expires the login after
7 days and Focus reopens the browser. Click **Audience → Publish app** to stop that. Without
`credentials.json`, Focus runs in offline mode, and tasks and timers still work.

### 3. Run
```powershell
.\focus_agent\run.ps1
```
or `python -m focus_agent` from the folder that contains `focus_agent`. `run.ps1` picks
`$env:FOCUS_PYTHON`, then a python.org 3.14 install, then `python` on PATH. It also loads a
`.venv` next to the package, or `$env:FOCUS_SITE_PACKAGES`, through `site.addsitedir` rather
than `PYTHONPATH`, because the SDK's `pywin32` dependency needs `.pth` files to run.

In the chat, type naturally ("plan my afternoon", "add task: read chapter 4 for Bio by Thursday",
"25 min on the lab report", "give me 10 more minutes"). Commands: `/status`, `/bye` (end-of-day
recap), `/quit`.

## Voice mode

Talk to Focus out loud, hands-free, like a call:
```powershell
.\focus_agent\run.ps1 -Voice      # or type /voice in the chat
```
When a session ends, Focus speaks the check-in and opens the mic for your answer. It keeps the
conversation going for as long as it's asking you questions. Press **Enter** to talk at any
other time, and type `/voice off` to go back to text. Typing always works too.

- **Listening:** OpenAI Whisper runs locally on your GPU, so your audio never leaves the machine.
  It handles English and French. Focus uses the best model it finds in `data/models/`, trying
  `whisper-large-v3-turbo` (~1.6 GB, most accurate), then `whisper-small`, then `whisper-base`
  (~290 MB). If none is there, it downloads `openai/whisper-base`. To add a model, put its files from
  `huggingface.co/openai/<name>` into `data/models/<name>/`.
- **Speaking:** Microsoft's multilingual neural voice through `edge-tts`. This voice is online, so
  the text of Focus's replies is sent to Microsoft's speech service. If that fails, Focus falls
  back to the offline Windows voice.
- **Privacy:** the mic only opens right after Focus speaks, or when you press Enter. It never
  listens in the background or while Focus is talking.

| Variable | Default | |
|---|---|---|
| `FOCUS_STT_MODEL` | best model in `data/models/` | a hub id or a local folder path |
| `FOCUS_TTS_VOICE` | `en-US-EmmaMultilingualNeural` | any `edge-tts --list-voices` name, e.g. `fr-FR-DeniseNeural` |
| `FOCUS_TTS_RATE` | `+5%` | speaking speed |

## Configuration (environment variables)

| Variable | Default | |
|---|---|---|
| `FOCUS_AGENT_MODEL` | your account's default | e.g. `claude-opus-5-5`, `sonnet`, `haiku` |
| `FOCUS_AGENT_EFFORT` | `medium` | `low` is faster and cheaper for chat; `high` plans more carefully |
| `FOCUS_AGENT_CALENDAR` | `primary` | Calendar ID to use |
| `FOCUS_AGENT_DATA` | `focus_agent/data` | Where tasks, session log and token live |

Session lengths (25-min focus, 5-min short break, 15-min long break after 4 sessions) are in
`config.py`.
