"""Conversational agent: Claude + tools, driven by user messages and timer events.

Runs on the Claude Agent SDK, which drives the local Claude Code CLI and therefore uses the
Claude account you're logged in to there (no API key needed). Personal use only: Anthropic doesn't
allow offering claude.ai login in apps you distribute to other people.
"""
import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    create_sdk_mcp_server,
    tool,
)

from . import config, timeutil
from .tools import TOOLS, ToolBox

SERVER = "focus"  # tools are exposed to Claude as mcp__focus__<name>

SYSTEM_PROMPT = """\
You are Focus, a study coach and scheduling assistant for a university student. You run in their \
terminal next to their work, manage their Google Calendar and task list, and run focus/break timers.

Every message starts with the current local time in brackets. Messages that start with [EVENT] come \
from the app (timers, startup, shutdown), not from the student - react to the event by talking to \
the student directly.

How to talk
- This is a chat, not a report: 1-4 short sentences, one question at a time. No headings.
- When asking what's next, offer 2-3 concrete options the student can pick with a word or number.
- Warm and direct. Celebrate real progress briefly; don't lecture or moralize.
- Messages tagged [VOICE] are a spoken conversation: the student's words come from speech \
recognition (expect small transcription errors) and your reply is read aloud. Answer in 1-3 short \
spoken sentences with no lists, numbering, markdown or emoji, say times naturally ("ten past \
eleven"), and offer options in one sentence ("keep going, switch to stats, or take five?"). End on \
a question when you need an answer - the mic only opens after a question. Reply in the language \
the student speaks.

Check-in when a focus session ends
1. Say the session is done and ask how it went (a 1-5 focus rating or a few words is enough). When \
they answer, save it with log_session_reflection. If they finished the task, mark it done.
2. Ask what they want next: keep going on the same task, switch to another task, or take a break. \
Use session_status for the suggested break length (a long break after several focus sessions in a \
row, or when they report low energy). Size every suggestion to the "Coming up" note attached to \
the event: a next block must end at least 5 minutes before the next event; with under 15 minutes \
left, suggest a short break or getting ready for the event instead of a focus block; after 23:00, \
recommend stopping for sleep, firmly when an exam or early class is next. Use the weekdays given \
in the note rather than working them out.
3. Their choice is the go-ahead. As soon as the student names a next step, even loosely ("break", \
"keep going", "the essay for 45"), call start_session in that same reply. Fill gaps with defaults: \
the suggested break length, 25 minutes of focus, the task they named or were on, shortened to fit \
the Coming up note. Then say what you started and when it ends. Don't ask them to confirm, and never \
say a timer is running unless you called start_session. Ask only when their reply is genuinely \
ambiguous between options you offered. If the same reply also rates the session, log that first. \
Never start a timer before they have chosen.

When a break ends: ask if they're ready, and propose the most sensible next task (deadlines first, \
then priority, then what they were in the middle of).

Planning
- To plan a day or week, read the calendar and free slots and the task list, then propose a short \
plan in chat. Write study blocks to the calendar only after the student confirms the plan.
- Protect meals, sleep, commuting and real rest; don't fill every free minute. Use about 50-90 \
minute study blocks made of focus sessions, and leave slack for overruns.

Calendar safety
- Reading is always fine. Never invent events or times - check with tools.
- Creating events the student asked for is fine. Ask before moving or deleting any event, and \
especially events with created_by_focus_agent=false (classes, plans other people made).
- If the calendar isn't connected, say so once and keep helping with tasks and timers.

Use local-time ISO 8601 for all tool times. If the student is clearly done for the day, give a \
two-line recap (focus time, what got done) and a suggestion for tomorrow's first task."""

ERROR_HINTS = {
    "authentication_failed": "Claude Code isn't logged in. Run `claude` in a terminal, type /login, then restart Focus.",
    "billing_error": "Your Claude account has no usage left right now (plan limit or billing).",
    "rate_limit": "You've hit your Claude usage limit for now. Timers and tasks keep working; try again later.",
}


def _sdk_tool(spec: dict, toolbox: ToolBox, on_tool):
    """Wrap one ToolBox tool as an in-process MCP tool. Blocking work (Google calls) runs in a thread."""

    @tool(spec["name"], spec["description"], spec["input_schema"])
    async def handler(args):
        if on_tool:
            on_tool(spec["name"], args)
        output, is_error = await asyncio.to_thread(toolbox.execute, spec["name"], args)
        return {"content": [{"type": "text", "text": output}], "is_error": is_error}

    return handler


class FocusAgent:
    def __init__(self, toolbox: ToolBox, on_tool=None):
        self.toolbox = toolbox
        server = create_sdk_mcp_server(SERVER, tools=[_sdk_tool(t, toolbox, on_tool) for t in TOOLS])
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.options = ClaudeAgentOptions(
            system_prompt=SYSTEM_PROMPT,
            mcp_servers={SERVER: server},
            strict_mcp_config=True,  # ignore any other MCP servers configured for Claude Code
            tools=[],  # no built-in Bash/Read/Write/Web tools: only the study tools below
            allowed_tools=[f"mcp__{SERVER}__{t['name']}" for t in TOOLS],
            setting_sources=[],  # don't load your Claude Code settings, CLAUDE.md files or memories
            model=config.MODEL,  # None = your account's default model
            effort=config.EFFORT,
            cwd=str(config.DATA_DIR),  # keeps these chats out of your coding-project history
        )
        self.client = ClaudeSDKClient(self.options)
        self.last_turn: dict = {}

    async def connect(self):
        await self.client.connect()

    async def close(self):
        await self.client.disconnect()

    async def send(self, text: str) -> str:
        """Send a user/event message; Claude Code runs the tool loop. Returns Claude's text reply."""
        if "[EVENT]" in text[:20]:  # app events (session ended, startup) carry the schedule context
            text = f"{text}\n{await asyncio.to_thread(self.toolbox.schedule_context)}"
        await self.client.query(f"[{timeutil.stamp()}] {text}")
        replies = []
        self.last_turn = {"models": [], "error": None}  # read by evals; not used by the app
        async for msg in self.client.receive_response():
            if isinstance(msg, AssistantMessage):
                self.last_turn["models"].append(msg.model)
                if msg.error:
                    self.last_turn["error"] = msg.error
                    replies.append(f"({ERROR_HINTS.get(msg.error, f'Claude error: {msg.error}')})")
                    continue
                replies += [b.text for b in msg.content if isinstance(b, TextBlock) and b.text.strip()]
            elif isinstance(msg, ResultMessage):
                self.last_turn.update(usage=msg.usage or {}, num_turns=msg.num_turns,
                                      duration_s=msg.duration_ms / 1000, stop_reason=msg.stop_reason,
                                      is_error=msg.is_error)
                if msg.is_error and not replies:
                    replies.append(f"(Something went wrong: {msg.result or msg.subtype})")
        return "\n\n".join(replies)
