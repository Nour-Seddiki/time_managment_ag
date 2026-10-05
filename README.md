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
conversation going for as long as it's asking you questions. A short two-note tone means it's
your turn. Press **Enter** to talk at any other time, or **while Focus is speaking** to cut it off
and answer right away. Typing while it speaks also stops it and sends what you typed. Type
`/voice off` to go back to text.

- **"Hi Focus":** start Focus with `run.ps1 -Voice`. It loads quietly, plays a ready tone, and
  waits. The first "Hi Focus" gets a greeting with what's coming up today; after that it answers
  "Yes?" straight away. "Hi Focus, start 25 minutes on stats" does it in one go. The mic only
  listens while Focus is open, nothing runs in the background after you close it, and everything
  is transcribed locally. Turn the wake word off with `FOCUS_WAKE_WORD=0`; Focus then greets you as
  soon as it starts.
- **Ending:** say "bye" (or "goodbye", "that's all", "au revoir") to end the conversation, and Focus
  goes back to waiting for "Hi Focus". Say "close Focus" to quit. Both are recognised instantly on
  your laptop.
- **Fast replies:** Focus speaks while Claude is still writing. The first sentence is synthesized
  and played as soon as it's complete, so you hear the answer about as soon as it starts.
- **Turn-taking:** Silero VAD, a small neural speech detector, decides when you start and stop
  talking. Fans, traffic and keyboard noise don't open or hold the mic. If Silero isn't installed,
  a loudness threshold is used instead.
- **Fast replies:** speech is generated sentence by sentence, and the voice connection is warmed
  up when voice mode starts. Focus starts talking about a second after its reply is ready.

- **Listening:** OpenAI Whisper runs locally on your GPU, so your audio never leaves the machine.
  It handles English and French. Focus uses the best model it finds in
  `%LOCALAPPDATA%\FocusAgent\models\` (or `data/models/`), trying `whisper-large-v3-turbo`
  (~1.6 GB, most accurate), then `whisper-small`, then `whisper-base` (~290 MB). If none is there,
  it downloads `openai/whisper-base`. To add a model, put its files from
  `huggingface.co/openai/<name>` into `%LOCALAPPDATA%\FocusAgent\models\<name>\`. That folder sits
  outside the project on purpose, so cloud-synced folders like OneDrive don't upload gigabytes of
  model weights.
- **Speaking:** Microsoft's multilingual neural voice through `edge-tts`. This voice is online, so
  the text of Focus's replies is sent to Microsoft's speech service. If that fails, Focus falls
  back to the offline Windows voice.
- **Privacy:** the mic only opens right after Focus speaks, or when you press Enter. It never
  listens in the background or while Focus is talking.

| Variable | Default | |
|---|---|---|
| `FOCUS_STT_MODEL` | best local model | a hub id or a local folder path |
| `FOCUS_MODELS_DIR` | `%LOCALAPPDATA%\FocusAgent\models` | where Focus looks for Whisper models |
| `FOCUS_TTS_VOICE` | `en-US-EmmaMultilingualNeural` | any `edge-tts --list-voices` name, e.g. `fr-FR-DeniseNeural` |
| `FOCUS_TTS_RATE` | `+5%` | speaking speed |

## Eval: the session check-in

`evals/checkin.py` measures how well Focus handles the end-of-session check-in. Each of its 38
cases recreates a moment in a student's day, with a fixed clock, a fake calendar and task list,
and earlier sessions. Focus gets the real "session ended" event and scripted student replies, and
the conversation is graded:

- **By code:** no timer before the student chooses, the chosen session started with the right
  length and task, the rating logged, the right task marked done, the calendar untouched, replies
  short.
- **By an LLM judge** (Sonnet 5.5, through your Claude account): asks how it went, gives a clear
  next step, respects the case's key context (a class in 10 minutes, exhaustion, 1am before an
  exam), supportive tone.

```powershell
python -m focus_agent.evals.checkin --review     # cases.md: read every input
python -m focus_agent.evals.checkin --selftest   # grader sanity checks, no model calls
python -m focus_agent.evals.checkin --reps 2     # full run (resumes where it stopped)
python -m focus_agent.evals.checkin --variant v1 --reps 2   # after editing the prompt
```

**Baseline (Claude Sonnet 5, 38 cases × 2 reps): 68% of check-ins pass every check.** The weak
spots were upcoming calendar events (8%) and re-asking after the student had already chosen. Three
tuning rounds, each kept, are recorded in `.claude/hillclimb/checkin/` (`narrative.md`, `v1/` to `v3/`):

1. A "coming up" note with the next events and deadlines is attached to every app event.
2. The student's choice counts as the go-ahead, so Focus starts the timer instead of re-asking.
3. Deadline dates in the note are unambiguous ("tomorrow Tue 09:00", "Mon 12 Oct, in 7 days").

The result: held-out test went from 71% to 82%, but +12 ± 27 points isn't significant with 17 test
cases. Train went from 67% to 95%. Acting on the student's choice went from 75% to 100% and context
fit from 80% to 95%, and Focus still never starts a timer early or changes the calendar on its own.
A confirmation on 20 fresh cases (`checkin_fresh`) is in progress. If the runner, cases or grader change, it refuses
to run until you review them and pass `--approve-harness` once.

## Configuration (environment variables)

| Variable | Default | |
|---|---|---|
| `FOCUS_AGENT_MODEL` | your account's default | e.g. `claude-opus-5-5`, `sonnet`, `haiku` |
| `FOCUS_AGENT_EFFORT` | `medium` | `low` is faster and cheaper for chat; `high` plans more carefully |
| `FOCUS_AGENT_CALENDAR` | `primary` | Calendar ID to use |
| `FOCUS_AGENT_DATA` | `focus_agent/data` | Where tasks, session log and token live |

Session lengths (25-min focus, 5-min short break, 15-min long break after 4 sessions) are in
`config.py`.
