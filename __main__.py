"""Terminal chat: `python -m focus_agent`.

User input and timer events feed one queue, so a session ending mid-afternoon starts a check-in
conversation even if the student hasn't typed anything.
"""
import asyncio
import json
import sys
import threading
from pathlib import Path

from claude_agent_sdk import ClaudeSDKError, CLINotFoundError

from . import config, timeutil
from .agent import FocusAgent
from .calendar_client import CalendarClient, CalendarNotConnected
from .sessions import SessionManager
from .store import Store
from .tools import ToolBox

HELP = """Commands: /status  timer and today's totals
          /voice   talk to Focus out loud (toggle); then Enter = talk
          /bye     end-of-day wrap-up, then exit
          /quit    exit immediately
Anything else is a message to Focus, e.g. "plan my afternoon" or "25 min on the lab report"."""


def _alert():
    if sys.platform == "win32":
        import winsound

        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    else:
        print("\a", end="", flush=True)


def _describe(event: dict) -> str:
    s = event["session"]
    if s["kind"] == "focus":
        return (f"[EVENT] The {s['actual_minutes']}-minute focus session on \"{s['label']}\" just ended. "
                "Run the end-of-session check-in.")
    return f"[EVENT] The {s['actual_minutes']}-minute break just ended. Ask if they're ready and propose what's next."


def _prompt():
    print("you> ", end="", flush=True)


async def amain():
    for stream in (sys.stdout, sys.stdin):  # emoji and accents in a Windows console
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    loop = asyncio.get_running_loop()
    events: asyncio.Queue = asyncio.Queue()

    def put(item):  # safe to call from the stdin and timer threads
        loop.call_soon_threadsafe(events.put_nowait, item)

    voice = None  # a voice.Voice while voice mode is on
    busy = threading.Event()  # set while Focus is thinking, speaking or listening: wake word ignored
    wake_stop = threading.Event()
    wake_on = False  # listening for "Hi Focus" (only while Focus is open)

    async def set_voice(on: bool):
        nonlocal voice, wake_stop, wake_on
        if not on:
            voice = None
            wake_stop.set()
            wake_on = False
            print("🔇 Voice off.")
            return
        from .voice import Voice, WakeListener

        print(f"🎙 Loading speech recognition ({Path(config.STT_MODEL).name})...", flush=True)
        v = Voice()
        try:
            await asyncio.to_thread(v.load)
        except Exception as e:  # missing package, no mic, download failed
            print(f"! Voice unavailable: {type(e).__name__}: {e}")
            return
        voice = v
        detector = "Silero VAD" if v.vad is not None else "loudness"
        wake = ""
        if config.WAKE_WORD and v.vad is not None:
            wake_stop = threading.Event()
            listener = WakeListener(v.transcribe, on_wake=lambda rest: put(("wake", rest)))
            threading.Thread(target=listener.run, args=(wake_stop, busy), daemon=True, name="wake").start()
            wake_on = True
            wake = ' Say "Hi Focus" to talk.'
        print(f"🎙 Voice on ({detector}): Focus speaks and listens after each question (you'll hear a short "
              f"tone).{wake} Enter also talks, or cuts Focus off mid-sentence. /voice off to stop.", flush=True)

    # Start loading speech recognition now, so it overlaps with connecting to the calendar and Claude.
    voice_ready = asyncio.create_task(set_voice(True)) if config.VOICE else None

    store = Store(config.STATE_FILE)
    sessions = SessionManager(store, on_event=lambda e: put(("timer", e)))

    calendar = CalendarClient()
    try:
        calendar.connect()
        print("✓ Google Calendar connected")
    except CalendarNotConnected as e:
        print(f"! Calendar offline ({e}). Tasks and timers still work.")

    agent = FocusAgent(
        ToolBox(store, calendar, sessions),
        on_tool=lambda name, args: print(f"  · {name}", flush=True),
    )
    try:
        await agent.connect()
    except CLINotFoundError:
        sys.exit("Claude Code isn't installed or not on PATH. Install it, run `claude` once and /login.")
    print("✓ Connected to your Claude account")

    async def listen() -> str | None:
        print("🎙 your turn...", flush=True)
        heard = await asyncio.to_thread(voice.listen, on_speech=lambda: print("   (hearing you)", flush=True))
        if heard:
            print(f"you (voice)> {heard}", flush=True)
        return heard

    async def farewell(kind: str) -> bool:
        """Handle "bye" (end the conversation) or "close Focus" (quit) locally. True if handled."""
        if kind == "close":
            await asyncio.to_thread(voice.speak, "Closing Focus. Bye!")
            put(("user", "/quit"))
        elif kind == "bye":
            await asyncio.to_thread(voice.speak, "Bye! Say Hi Focus when you need me.")
        return kind is not None

    async def ask(text: str) -> tuple[str | None, bool]:
        """Send to Claude, printing (and in voice mode speaking) the reply as it is written.
        Returns (reply, interrupted)."""
        speaker = voice.stream() if voice else None
        started = False

        def on_text(chunk: str):
            nonlocal started
            if not started:
                print("\nFocus: ", end="", flush=True)
                started = True
            print(chunk, end="", flush=True)
            if speaker:
                speaker.feed(chunk)

        try:
            reply = await agent.send(f"[VOICE] {text}" if voice else text, on_text=on_text)
        except ClaudeSDKError as e:
            print(f"! Claude Code error: {e}")
            reply = None
        if started:
            print("\n", flush=True)
        elif reply:  # nothing streamed (e.g. a usage-limit notice): show it whole
            print(f"\nFocus: {reply}\n", flush=True)
            if speaker:
                speaker.feed(reply)
        interrupted = await asyncio.to_thread(speaker.finish) if speaker else False
        return reply, interrupted

    async def say(text: str):
        """Send a message. In voice mode, keep talking while Focus ends on a question; "bye" ends
        the conversation, "close Focus" quits."""
        from .voice import asks_question, goodbye_kind

        busy.set()
        try:
            while True:
                reply, interrupted = await ask(text)
                if reply is None or not voice:
                    break
                if interrupted and voice.interrupt_reason == "text":
                    break  # they started typing; the typed message is already queued
                if not interrupted and not asks_question(reply):
                    break
                text = await listen()
                if not text:
                    print('(didn\'t hear an answer - say "Hi Focus", press Enter to talk, or type)')
                    break
                if await farewell(goodbye_kind(text)):
                    break
        finally:
            busy.clear()
        _prompt()

    def read_stdin():
        for line in sys.stdin:
            line = line.strip().lstrip("﻿")  # PowerShell pipes add a BOM
            if voice is not None and voice.speaking:  # typing while Focus talks cuts it off
                voice.stop("text" if line else "enter")
                if not line:
                    continue  # Enter alone: the mic opens right after Focus stops
            put(("user", line))
        put(("user", "/quit"))  # stdin closed

    threading.Thread(target=read_stdin, daemon=True).start()  # before the greeting, so it can be interrupted

    from .voice import goodbye_kind

    print(HELP)
    greeted = False
    if voice_ready:
        await voice_ready
    if wake_on:  # quiet start: nothing happens until "Hi Focus"
        import winsound

        winsound.MessageBeep(winsound.MB_OK)
        print('\n✓ Focus is ready. Say "Hi Focus" to start.', flush=True)
        _prompt()
    else:
        await say("[EVENT] App started. Greet the student, check today's calendar and open tasks, "
                  "and ask what they'd like to work on first.")
        greeted = True

    try:
        while True:
            source, item = await events.get()
            if source == "timer":
                _alert()
                print(f"\n\n⏰ [{timeutil.stamp()}] {item['session']['kind']} session finished", flush=True)
                await say(_describe(item))
            elif source == "wake":
                if not voice or busy.is_set():
                    continue
                print("\n👋 Hi Focus" + (f": {item}" if item else ""), flush=True)
                if not greeted and not item:  # first "Hi Focus": greet with what's coming up today
                    greeted = True
                    await say("[EVENT] The student just said \"Hi Focus\". Greet them in one short sentence, "
                              "mention what's next today if anything, and ask what they want to do.")
                    continue
                greeted = True
                busy.set()
                if not item:  # just "Hi Focus": answer right away, then listen
                    await asyncio.to_thread(voice.speak, "Yes?")
                    item = await listen()
                handled = not item or await farewell(goodbye_kind(item))
                busy.clear()
                if not handled:  # "Hi Focus, start 25 minutes on stats" or the answer to "Yes?"
                    await say(item)
                else:
                    _prompt()
            elif not item:
                if voice:  # Enter = push to talk
                    busy.set()
                    heard = await listen()
                    handled = not heard or await farewell(goodbye_kind(heard))
                    busy.clear()
                    if not handled:
                        await say(heard)
                        continue
                _prompt()
            elif item in ("/voice", "/voice on", "/voice off"):
                await set_voice(item != "/voice off" and (item == "/voice on" or voice is None))
                _prompt()
            elif item == "/quit":
                break
            elif item == "/status":
                print(json.dumps(sessions.status(), indent=2, ensure_ascii=False))
                _prompt()
            elif item == "/help":
                print(HELP)
                _prompt()
            elif item == "/bye":
                await say("[EVENT] The student is ending the day. Stop any running session, then give "
                          "the end-of-day recap and suggest tomorrow's first task.")
                break
            else:
                await say(item)
    finally:
        wake_stop.set()
        if sessions.active:
            sessions.stop("interrupted")
        await agent.close()
    print("Bye - good work today.")


def main():
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        print("\nBye.")


if __name__ == "__main__":
    main()
