# Attach a "coming up" note (next events, deadlines with weekdays) to app events and size check-in suggestions to it

**Target:** checkin_ok, via context_fit (8 of 14 failing train rows). Guardrails: no_early_timer,
no_cal_writes, concise, tone, reflection, task_status.

**Behaviour:** at check-in Focus usually doesn't look at what's coming up, so it suggests blocks
that collide with the next commitment or ignore the hour. In the train traces:

- `baseline/traces/lab-in-5-hungry_rep0.json`: lab at 13:00, now 12:55; no calendar call. Focus says
  "Want to take a proper lunch break and pick this back up after?"
- `baseline/traces/lecture-in-13-short-break_rep1.json`: lecture at 11:00, now 10:47; no calendar
  call. Focus offers "keep rolling on the lab report (next up: methods?)".
- `baseline/traces/cramming-1am_rep0.json`: it did call `list_calendar_events` but only for
  01:10-03:00, missed the 09:00 exam and said "Clear calendar, nothing rushing you. Another 25 on genetics...?"
- Weekday errors (long-break-ended-evening rep1: "due Friday" for a Thursday exam) come from the
  model working out weekdays itself.

**Change (one hypothesis: the check-in lacks time context):**
1. `ToolBox.schedule_context()` builds a short note: the next 3 calendar events in the next 18h with
   minutes until each, and the 3 nearest deadlines with weekday names. `FocusAgent.send` appends it
   to every `[EVENT]` message (session ended, break ended, app start), in the app and in the eval alike.
2. Prompt step 2 of the check-in now says to size suggestions to that note: end 5+ min before the
   next event, under 15 min left means break or get ready, after 23:00 recommend sleep, and use the
   note's weekdays.

Cases expected to move: the calendar_soon and late_night failures. Possible regression: in-the-zone
and other free-time cases, if Focus starts over-weighting far-off events. Watch context_fit there.
Not visible in traces: the note is added inside `FocusAgent.send`, so trace user turns show only the event text.
