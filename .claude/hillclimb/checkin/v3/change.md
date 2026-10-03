# Fix the "coming up" note's dates: say today/tomorrow or give the full date, so far-off deadlines don't read as tonight

**Target:** checkin_ok via context_fit (6 of 12 failing train rows after v1 involve a wrong
deadline day). Guardrails unchanged. **[REQUIRED]**: this fixes a bug that v1 introduced.

**Behaviour:** v1's note printed any deadline that wasn't today as weekday + time ("Mon 23:59"). When
today is also Monday, a deadline a week away reads as tonight, and Focus repeats it as false urgency
and mis-prioritises. Train evidence (v1 traces, judge reasons):

- exam-tomorrow-confused rep0/rep1: "wrongly said the essay is due tonight at 11:59 when it is due
  2026-10-12" and offered switching to it the night before the calculus exam.
- long-break-ended-evening rep0/rep1 (v2 trace): "That English essay is due tonight at 23:59, so
  that's the priority" over Thursday's biochemistry exam revision.
- break-ended-ready rep0/rep1: "Sociology reading was due tonight, but it is due 2026-10-12".

**Change:** `schedule_context().when()` now writes "HH:MM, in N min" under 2h, "today HH:MM, in XhYY",
"tomorrow Tue HH:MM, in XhYY", and otherwise the full date with a day count ("Mon 12 Oct 23:59, in 7 days").
No prompt change.

Expected movers: context_fit in break_ended and calendar_soon/exam cases. Risk: none expected; the
note only gets more explicit.
