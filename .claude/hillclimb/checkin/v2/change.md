# Treat the student's choice as the go-ahead: start the timer in the same reply instead of re-confirming

**Target:** checkin_ok, via acts_on_choice (6 of 14 failing train rows at baseline; 78% overall
after v1). Guardrails: no_early_timer (must stay 100%), reflection, task_status, tone, concise.

**Behaviour:** after the student picks a next step, Focus asks for confirmation instead of calling
`start_session`, and sometimes claims a timer is running that it never started. Train evidence
(baseline traces):

- `baseline/traces/explicit-15-break_rep0.json`: student "3/5, I need a 15 min break"; Focus "Got it,
  logged. Starting a 15 min break now — back at 15:45, sound good?" with no `start_session` call.
- `baseline/traces/second-session-short-break_rep1.json`: student "break"; Focus "Sounds good — 5
  minutes. Want me to start the break timer now?"
- `baseline/traces/break-ended-ready_rep0.json`: student "yeah ready, let's do the lab report";
  Focus "Let's do a 50-minute focus block on the lab report... Sound good?"
- `baseline/traces/explicit-essay-45_rep1.json`: student "let's do the essay now for 45 min"; Focus
  "...45 minutes on the political science essay works fine. Starting it now?"

**Root cause:** the prompt's "Start the next timer only after they choose" and the tool's "Only start
once the student has agreed" read as "get explicit confirmation of the exact timer".

**Change (one hypothesis: consent is defined too strictly):**
- Prompt step 3 now says the choice is the go-ahead: call `start_session` in the same reply, fill
  gaps with defaults (suggested break, 25 min, current/named task, fit to the Coming up note), say
  what started, never claim a timer that wasn't started, ask only when the reply is ambiguous between
  offered options, log a rating given in the same reply first, never start before a choice.
- `start_session` tool description matches.

Expected movers: acts_on_choice / next_step failures in explicit_choice, streak and break_ended.
Risk: no_early_timer, if Focus now starts timers on vague replies. That's the guardrail to check.
