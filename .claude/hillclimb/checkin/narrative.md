| round | change | test | vs base (paired, 95% CI) | train | guardrails | s/conv | words/reply | tool calls | rows |
|---|---|---|---|---|---|---|---|---|---|
| 0 | baseline | 71% | - | 67% | tone 97% | 9.1 | 25 | 2.2 | 76 |
| 1 | Attach a "coming up" note (next events, deadlines with we... | 79% | +9% ± 26% (noise) | 71% | tone 99%, reflection 97%, task_status 97% | 9.1 | 25 | 1.6 | 76 |
| 2 | Treat the student's choice as the go-ahead: start the tim... | 85% | +15% ± 26% (noise) | 81% | tone 99%, task_status 99% | 9.3 | 24 | 1.7 | 76 |
| 3 | Fix the "coming up" note's dates: say today/tomorrow or g... | 82% | +12% ± 27% (noise) | 95% | reflection 97% | 9.0 | 25 | 1.6 | 76 |
<!-- end table -->

**State of play (after 3 of 4 rounds; stopped: train saturated).** v3 is the current code and the
recommended version. v1 gave Focus a "coming up" note on every app event (next events with minutes
until each, nearest deadlines) and told it to size suggestions to it. That lifted context_fit from
80% to 91% and the class-soon train cases from 17% to 50%. But its weekday-only dates made week-away
deadlines read as "tonight". v2 redefined consent ("your choice is the go-ahead") and lifted
acts_on_choice from 75% to 100% with no early timers (two loose-reply cases were relaxed with the
user's OK and every round regraded). v3 fixed v1's date format ([REQUIRED]), lifting train to 95%
and context_fit to 95%. On held-out test, v3 is 82% against 71% at baseline (+12 ± 27 paired):
positive, but not significant with 17 test cases. Five test cases went from failing to passing
(class/bus/meeting soon, French cases); two regressed in both reps since v1/v2 (a rating given
alongside a calendar-conflicting request isn't logged; the 4th-session long break is no longer
recommended). Those two weren't investigated, to keep the held-out set clean.
