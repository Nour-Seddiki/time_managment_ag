# Check-in eval - `v2`

Change: Treat the student's choice as the go-ahead: start the timer in the same reply instead of re-confirming

**train** 81% ± 17% (21 cases) · **test** 85% ± 17% (17 cases)

38 cases × 2 rep(s); 0 attempt(s) not scored (see errors.jsonl). Model: ['claude-sonnet-5']; judge: ["['claude-sonnet-5-5']"].

Scores are the share of cases passing (per case: mean over reps), with a 95% interval. n/a cases are left out of that metric.

| metric | score | 95% CI | n |
|---|---|---|---|
| **checkin_ok** | 83% | ±12% | 38 |
| no_early_timer | 100% | ±0% | 38 |
| acts_on_choice | 100% | ±0% | 20 |
| reflection | 100% | ±0% | 33 |
| task_status | 99% | ±4% | 38 |
| no_cal_writes | 100% | ±0% | 38 |
| concise | 100% | ±0% | 38 |
| check_in_q | 99% | ±4% | 38 |
| next_step | 96% | ±6% | 38 |
| context_fit | 89% | ±10% | 38 |
| tone | 99% | ±4% | 38 |

## By scenario type (checkin_ok)

| tag | score | n |
|---|---|---|
| break_ended | 60% | 5 |
| calendar_free | 100% | 1 |
| calendar_soon | 75% | 6 |
| energy | 100% | 7 |
| explicit_choice | 93% | 7 |
| late_night | 25% | 2 |
| streak | 75% | 4 |
| task_done | 100% | 6 |

## Cases

| case | ok | failed checks | trace |
|---|---|---|---|
| break-ended-ready (rep 0) | ✗ | **context_fit**: Focus pushed the sociology reading as "the smart pick" and said it was due tonight, but it is low priority and due 2026-10-12, while the lab report is the closest deadline and the task the student was already working on. | [trace](v2/traces/break-ended-ready_rep0.json) |
| break-ended-ready (rep 1) | ✗ | **context_fit**: Focus's first reply led with the sociology reading and wrongly said it was due tonight (it's due 10-12, and the lab report is due first), which contradicts the key context that resuming the lab report was the natural proposal, even though the final action did match it. | [trace](v2/traces/break-ended-ready_rep1.json) |
| cramming-1am (rep 0) | ✗ | **next_step**: The student asked for "one more?" and Focus offered only one path ("call it and get to bed"). It gave no 2-3 concrete options, such as a 5-minute wrap-up or stopping now, and it ended on an open question without settling a next step. | [trace](v2/traces/cramming-1am_rep0.json) |
| cramming-1am (rep 1) | ✗ | **next_step**: The student asked for one more block, and Focus neither accepted that nor offered 2-3 options such as a 5-minute wrap-up, a quick note for tomorrow, or going to bed. It only pushed one option and ended on a yes/no question. | [trace](v2/traces/cramming-1am_rep1.json) |
| exam-tomorrow-confused (rep 0) | ✗ | **context_fit**: Offering to switch to the history essay goes against the key context to stay on calculus before tomorrow's exam, and it wrongly says the essay is due tonight at 23:59 when it's due 2026-10-12. | [trace](v2/traces/exam-tomorrow-confused_rep0.json) |
| exam-tomorrow-confused (rep 1) | ✗ | **context_fit**: Focus wrongly said the history essay is due tonight (it is due 2026-10-12) and offered switching to it, which goes against the key context of staying on calculus the day before the exam. | [trace](v2/traces/exam-tomorrow-confused_rep1.json) |
| explicit-25-conflicts-lecture (rep 1) | ✗ | **tone**: The tone is warm and direct, but the second message repeats the first almost word for word ("Logging that" then "Logged!", and the same options asked twice), which is padding. | [trace](v2/traces/explicit-25-conflicts-lecture_rep1.json) |
| fourth-session-long-break (rep 0) | ✗ | **context_fit**: A long break (15-30 minutes) is due after four sessions in a row, but Focus offers only a 'short break' and treats continuing as an equal option, so it doesn't steer toward the long break. | [trace](v2/traces/fourth-session-long-break_rep0.json) |
| fourth-session-long-break (rep 1) | ✗ | **next_step**: Focus offered only two options (another 25 or a short break), the student never chose one, and no concrete next step was settled.; **context_fit**: After four sessions with only short breaks, a long break (15-30 minutes) is due, but Focus suggested another 25 or a short break, which contradicts that. | [trace](v2/traces/fourth-session-long-break_rep1.json) |
| late-night-stop (rep 1) | ✗ | **check_in_q**: The first reply asks how the session went, then whether the student made good progress, then "Sound good?" about wrapping up, which makes three separate questions. | [trace](v2/traces/late-night-stop_rep1.json) |
| lecture-in-10-break (rep 0) | ✗ | **task_status**: marked done: ['t1']; expected: none | [trace](v2/traces/lecture-in-10-break_rep0.json) |
| long-break-ended-evening (rep 0) | ✗ | **context_fit**: Focus prioritized the English essay and wrongly said it was due tonight (it's due 2026-10-12), instead of proposing biochemistry revision for the exam on Thursday. | [trace](v2/traces/long-break-ended-evening_rep0.json) |
| long-break-ended-evening (rep 1) | ✗ | **context_fit**: Focus prioritized the English essay, which it wrongly said was due tonight (it's due 2026-10-12), instead of the Thursday biochemistry exam revision, which is the closest deadline. | [trace](v2/traces/long-break-ended-evening_rep1.json) |
| after-long-break-short-again (rep 0) | ✓ | - | [trace](v2/traces/after-long-break-short-again_rep0.json) |
| after-long-break-short-again (rep 1) | ✓ | - | [trace](v2/traces/after-long-break-short-again_rep1.json) |
| almost-done-slides (rep 0) | ✓ | - | [trace](v2/traces/almost-done-slides_rep0.json) |
| almost-done-slides (rep 1) | ✓ | - | [trace](v2/traces/almost-done-slides_rep1.json) |
| bored-reading (rep 0) | ✓ | - | [trace](v2/traces/bored-reading_rep0.json) |
| bored-reading (rep 1) | ✓ | - | [trace](v2/traces/bored-reading_rep1.json) |
| break-ended-5-more (rep 0) | ✓ | - | [trace](v2/traces/break-ended-5-more_rep0.json) |
| break-ended-5-more (rep 1) | ✓ | - | [trace](v2/traces/break-ended-5-more_rep1.json) |
| break-ended-class-soon (rep 0) | ✓ | - | [trace](v2/traces/break-ended-class-soon_rep0.json) |
| break-ended-class-soon (rep 1) | ✓ | - | [trace](v2/traces/break-ended-class-soon_rep1.json) |
| bus-in-10 (rep 0) | ✓ | - | [trace](v2/traces/bus-in-10_rep0.json) |
| bus-in-10 (rep 1) | ✓ | - | [trace](v2/traces/bus-in-10_rep1.json) |
| exhausted-after-50 (rep 0) | ✓ | - | [trace](v2/traces/exhausted-after-50_rep0.json) |
| exhausted-after-50 (rep 1) | ✓ | - | [trace](v2/traces/exhausted-after-50_rep1.json) |
| explicit-15-before-leaving (rep 0) | ✓ | - | [trace](v2/traces/explicit-15-before-leaving_rep0.json) |
| explicit-15-before-leaving (rep 1) | ✓ | - | [trace](v2/traces/explicit-15-before-leaving_rep1.json) |
| explicit-15-break (rep 0) | ✓ | - | [trace](v2/traces/explicit-15-break_rep0.json) |
| explicit-15-break (rep 1) | ✓ | - | [trace](v2/traces/explicit-15-break_rep1.json) |
| explicit-25-conflicts-lecture (rep 0) | ✓ | - | [trace](v2/traces/explicit-25-conflicts-lecture_rep0.json) |
| explicit-another-25 (rep 0) | ✓ | - | [trace](v2/traces/explicit-another-25_rep0.json) |
| explicit-another-25 (rep 1) | ✓ | - | [trace](v2/traces/explicit-another-25_rep1.json) |
| explicit-done-for-today (rep 0) | ✓ | - | [trace](v2/traces/explicit-done-for-today_rep0.json) |
| explicit-done-for-today (rep 1) | ✓ | - | [trace](v2/traces/explicit-done-for-today_rep1.json) |
| explicit-essay-45 (rep 0) | ✓ | - | [trace](v2/traces/explicit-essay-45_rep0.json) |
| explicit-essay-45 (rep 1) | ✓ | - | [trace](v2/traces/explicit-essay-45_rep1.json) |
| finished-essay-break (rep 0) | ✓ | - | [trace](v2/traces/finished-essay-break_rep0.json) |
| finished-essay-break (rep 1) | ✓ | - | [trace](v2/traces/finished-essay-break_rep1.json) |
| finished-lab-report (rep 0) | ✓ | - | [trace](v2/traces/finished-lab-report_rep0.json) |
| finished-lab-report (rep 1) | ✓ | - | [trace](v2/traces/finished-lab-report_rep1.json) |
| finished-last-task (rep 0) | ✓ | - | [trace](v2/traces/finished-last-task_rep0.json) |
| finished-last-task (rep 1) | ✓ | - | [trace](v2/traces/finished-last-task_rep1.json) |
| fourth-session-fading-accept (rep 0) | ✓ | - | [trace](v2/traces/fourth-session-fading-accept_rep0.json) |
| fourth-session-fading-accept (rep 1) | ✓ | - | [trace](v2/traces/fourth-session-fading-accept_rep1.json) |
| free-afternoon-switch (rep 0) | ✓ | - | [trace](v2/traces/free-afternoon-switch_rep0.json) |
| free-afternoon-switch (rep 1) | ✓ | - | [trace](v2/traces/free-afternoon-switch_rep1.json) |
| french-break-10 (rep 0) | ✓ | - | [trace](v2/traces/french-break-10_rep0.json) |
| french-break-10 (rep 1) | ✓ | - | [trace](v2/traces/french-break-10_rep1.json) |
| french-break-ended-ready (rep 0) | ✓ | - | [trace](v2/traces/french-break-ended-ready_rep0.json) |
| french-break-ended-ready (rep 1) | ✓ | - | [trace](v2/traces/french-break-ended-ready_rep1.json) |
| french-continue (rep 0) | ✓ | - | [trace](v2/traces/french-continue_rep0.json) |
| french-continue (rep 1) | ✓ | - | [trace](v2/traces/french-continue_rep1.json) |
| french-finished-tp (rep 0) | ✓ | - | [trace](v2/traces/french-finished-tp_rep0.json) |
| french-finished-tp (rep 1) | ✓ | - | [trace](v2/traces/french-finished-tp_rep1.json) |
| half-of-reading (rep 0) | ✓ | - | [trace](v2/traces/half-of-reading_rep0.json) |
| half-of-reading (rep 1) | ✓ | - | [trace](v2/traces/half-of-reading_rep1.json) |
| headache (rep 0) | ✓ | - | [trace](v2/traces/headache_rep0.json) |
| headache (rep 1) | ✓ | - | [trace](v2/traces/headache_rep1.json) |
| in-the-zone (rep 0) | ✓ | - | [trace](v2/traces/in-the-zone_rep0.json) |
| in-the-zone (rep 1) | ✓ | - | [trace](v2/traces/in-the-zone_rep1.json) |
| lab-in-5-hungry (rep 0) | ✓ | - | [trace](v2/traces/lab-in-5-hungry_rep0.json) |
| lab-in-5-hungry (rep 1) | ✓ | - | [trace](v2/traces/lab-in-5-hungry_rep1.json) |
| late-deadline-stress (rep 0) | ✓ | - | [trace](v2/traces/late-deadline-stress_rep0.json) |
| late-deadline-stress (rep 1) | ✓ | - | [trace](v2/traces/late-deadline-stress_rep1.json) |
| late-night-stop (rep 0) | ✓ | - | [trace](v2/traces/late-night-stop_rep0.json) |
| lecture-in-10-break (rep 1) | ✓ | - | [trace](v2/traces/lecture-in-10-break_rep1.json) |
| lecture-in-13-short-break (rep 0) | ✓ | - | [trace](v2/traces/lecture-in-13-short-break_rep0.json) |
| lecture-in-13-short-break (rep 1) | ✓ | - | [trace](v2/traces/lecture-in-13-short-break_rep1.json) |
| meeting-in-40-continue (rep 0) | ✓ | - | [trace](v2/traces/meeting-in-40-continue_rep0.json) |
| meeting-in-40-continue (rep 1) | ✓ | - | [trace](v2/traces/meeting-in-40-continue_rep1.json) |
| phone-distraction (rep 0) | ✓ | - | [trace](v2/traces/phone-distraction_rep0.json) |
| phone-distraction (rep 1) | ✓ | - | [trace](v2/traces/phone-distraction_rep1.json) |
| second-session-short-break (rep 0) | ✓ | - | [trace](v2/traces/second-session-short-break_rep0.json) |
| second-session-short-break (rep 1) | ✓ | - | [trace](v2/traces/second-session-short-break_rep1.json) |

Tokens (Focus, all cases): input 552, output 23,354, cache read 1,274,689. Runs on your Claude plan, so there's no per-token bill.

Mean latency per conversation: 9.3s.
