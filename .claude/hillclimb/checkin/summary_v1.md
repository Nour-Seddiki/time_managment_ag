# Check-in eval - `v1`

Change: Attach a "coming up" note (next events, deadlines with weekdays) to app events and size check-in suggestions to it

**train** 71% ± 19% (21 cases) · **test** 79% ± 19% (17 cases)

38 cases × 2 rep(s); 0 attempt(s) not scored (see errors.jsonl). Model: ['claude-sonnet-5']; judge: ["['claude-sonnet-5-5']"].

Scores are the share of cases passing (per case: mean over reps), with a 95% interval. n/a cases are left out of that metric.

| metric | score | 95% CI | n |
|---|---|---|---|
| **checkin_ok** | 75% | ±14% | 38 |
| no_early_timer | 100% | ±0% | 38 |
| acts_on_choice | 80% | ±18% | 20 |
| reflection | 97% | ±6% | 33 |
| task_status | 97% | ±5% | 38 |
| no_cal_writes | 100% | ±0% | 38 |
| concise | 100% | ±0% | 38 |
| check_in_q | 100% | ±0% | 38 |
| next_step | 92% | ±9% | 38 |
| context_fit | 91% | ±9% | 38 |
| tone | 99% | ±4% | 38 |

## By scenario type (checkin_ok)

| tag | score | n |
|---|---|---|
| break_ended | 40% | 5 |
| calendar_free | 100% | 1 |
| calendar_soon | 58% | 6 |
| energy | 93% | 7 |
| explicit_choice | 79% | 7 |
| late_night | 50% | 2 |
| streak | 75% | 4 |
| task_done | 100% | 6 |

## Cases

| case | ok | failed checks | trace |
|---|---|---|---|
| break-ended-ready (rep 0) | ✗ | **context_fit**: Focus said the Sociology reading was due tonight, but it is due 2026-10-12 and is low priority. It also offered Sociology as an equal option instead of proposing the in-progress, soonest-due lab report, so the suggestion contradicted the context even though the student picked the lab report anyway. | [trace](v1/traces/break-ended-ready_rep0.json) |
| break-ended-ready (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **context_fit**: Focus said the Sociology reading was "due tonight" when it is due 10/12 and the lab report is the nearest deadline, so it presented the two tasks as equals instead of proposing to resume the lab report. | [trace](v1/traces/break-ended-ready_rep1.json) |
| cramming-1am (rep 0) | ✗ | **next_step**: The student asked for one more session, and Focus neither offered 2-3 concrete options (such as a short wrap-up or stopping and sleeping) nor accepted a choice from the student, so it ends on a yes/no question with no settled next step. | [trace](v1/traces/cramming-1am_rep0.json) |
| cramming-1am (rep 1) | ✗ | **next_step**: Focus declined the student's "one more?" and offered only a single yes/no ask to go to bed, with no options such as a very short wrap-up and no firm close, so the next step is left open. | [trace](v1/traces/cramming-1am_rep1.json) |
| exam-tomorrow-confused (rep 0) | ✗ | **context_fit**: The key context says to stay on calculus, but Focus offered switching to the history essay. It also wrongly said the essay is due tonight at 11:59 when it is due 2026-10-12, which creates false urgency. | [trace](v1/traces/exam-tomorrow-confused_rep0.json) |
| exam-tomorrow-confused (rep 1) | ✗ | **context_fit**: Focus wrongly said the essay is due tonight (it's due 2026-10-12) and offered switching to it as a main option, when the next step should stay on calculus before tomorrow's exam. | [trace](v1/traces/exam-tomorrow-confused_rep1.json) |
| explicit-25-conflicts-lecture (rep 0) | ✗ | **reflection**: never logged the reflection | [trace](v1/traces/explicit-25-conflicts-lecture_rep0.json) |
| explicit-25-conflicts-lecture (rep 1) | ✗ | **reflection**: never logged the reflection | [trace](v1/traces/explicit-25-conflicts-lecture_rep1.json) |
| explicit-essay-45 (rep 1) | ✗ | **tone**: The tone is warm and direct with no guilt-tripping, but the final message repeats itself ("starting the essay now for 45 minutes" and then "45 minutes on the essay, starting now"), which is padding. | [trace](v1/traces/explicit-essay-45_rep1.json) |
| fourth-session-long-break (rep 0) | ✗ | **context_fit**: This was the 4th session in a row with only short breaks and a long break was due, but Focus offered continuing, a short break, or switching, and never suggested a long break. | [trace](v1/traces/fourth-session-long-break_rep0.json) |
| french-break-ended-ready (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student answered "ok je suis prêt" to the proposed 25-minute block, but Focus asked "on repart ... pour 25 minutes ?" again instead of starting the session, so it re-asked something already answered. | [trace](v1/traces/french-break-ended-ready_rep0.json) |
| french-break-ended-ready (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student already said they were ready to resume the project, but Focus asked for confirmation again ("On repart... ?") instead of starting the 25-minute session, so it re-asked something already answered. | [trace](v1/traces/french-break-ended-ready_rep1.json) |
| french-continue (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](v1/traces/french-continue_rep1.json) |
| lecture-in-10-break (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session; **task_status**: marked done: ['t1']; expected: none | [trace](v1/traces/lecture-in-10-break_rep0.json) |
| lecture-in-10-break (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **task_status**: marked done: ['t1']; expected: none | [trace](v1/traces/lecture-in-10-break_rep1.json) |
| lecture-in-13-short-break (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](v1/traces/lecture-in-13-short-break_rep1.json) |
| long-break-ended-evening (rep 0) | ✗ | **next_step**: Focus gives only a single proposal with no alternatives, and after the student says "ready" and asks what to do, it asks "Want to start?" again instead of just starting.; **context_fit**: Focus says the essay is due tonight at 23:59, but it's due 2026-10-12. It prioritizes the essay over the biochemistry revision, which is due before the Thursday exam and should have been the main proposal. | [trace](v1/traces/long-break-ended-evening_rep0.json) |
| long-break-ended-evening (rep 1) | ✗ | **next_step**: The student asked "what should i do", and Focus offered only one option (the essay) and repeated the same proposal instead of giving 2-3 concrete options.; **context_fit**: Focus prioritized the English essay and wrongly said it was due tonight (it is due 2026-10-12), when the biochemistry exam on Thursday should have been the main proposal. | [trace](v1/traces/long-break-ended-evening_rep1.json) |
| second-session-short-break (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](v1/traces/second-session-short-break_rep0.json) |
| after-long-break-short-again (rep 0) | ✓ | - | [trace](v1/traces/after-long-break-short-again_rep0.json) |
| after-long-break-short-again (rep 1) | ✓ | - | [trace](v1/traces/after-long-break-short-again_rep1.json) |
| almost-done-slides (rep 0) | ✓ | - | [trace](v1/traces/almost-done-slides_rep0.json) |
| almost-done-slides (rep 1) | ✓ | - | [trace](v1/traces/almost-done-slides_rep1.json) |
| bored-reading (rep 0) | ✓ | - | [trace](v1/traces/bored-reading_rep0.json) |
| bored-reading (rep 1) | ✓ | - | [trace](v1/traces/bored-reading_rep1.json) |
| break-ended-5-more (rep 0) | ✓ | - | [trace](v1/traces/break-ended-5-more_rep0.json) |
| break-ended-5-more (rep 1) | ✓ | - | [trace](v1/traces/break-ended-5-more_rep1.json) |
| break-ended-class-soon (rep 0) | ✓ | - | [trace](v1/traces/break-ended-class-soon_rep0.json) |
| break-ended-class-soon (rep 1) | ✓ | - | [trace](v1/traces/break-ended-class-soon_rep1.json) |
| bus-in-10 (rep 0) | ✓ | - | [trace](v1/traces/bus-in-10_rep0.json) |
| bus-in-10 (rep 1) | ✓ | - | [trace](v1/traces/bus-in-10_rep1.json) |
| exhausted-after-50 (rep 0) | ✓ | - | [trace](v1/traces/exhausted-after-50_rep0.json) |
| exhausted-after-50 (rep 1) | ✓ | - | [trace](v1/traces/exhausted-after-50_rep1.json) |
| explicit-15-before-leaving (rep 0) | ✓ | - | [trace](v1/traces/explicit-15-before-leaving_rep0.json) |
| explicit-15-before-leaving (rep 1) | ✓ | - | [trace](v1/traces/explicit-15-before-leaving_rep1.json) |
| explicit-15-break (rep 0) | ✓ | - | [trace](v1/traces/explicit-15-break_rep0.json) |
| explicit-15-break (rep 1) | ✓ | - | [trace](v1/traces/explicit-15-break_rep1.json) |
| explicit-another-25 (rep 0) | ✓ | - | [trace](v1/traces/explicit-another-25_rep0.json) |
| explicit-another-25 (rep 1) | ✓ | - | [trace](v1/traces/explicit-another-25_rep1.json) |
| explicit-done-for-today (rep 0) | ✓ | - | [trace](v1/traces/explicit-done-for-today_rep0.json) |
| explicit-done-for-today (rep 1) | ✓ | - | [trace](v1/traces/explicit-done-for-today_rep1.json) |
| explicit-essay-45 (rep 0) | ✓ | - | [trace](v1/traces/explicit-essay-45_rep0.json) |
| finished-essay-break (rep 0) | ✓ | - | [trace](v1/traces/finished-essay-break_rep0.json) |
| finished-essay-break (rep 1) | ✓ | - | [trace](v1/traces/finished-essay-break_rep1.json) |
| finished-lab-report (rep 0) | ✓ | - | [trace](v1/traces/finished-lab-report_rep0.json) |
| finished-lab-report (rep 1) | ✓ | - | [trace](v1/traces/finished-lab-report_rep1.json) |
| finished-last-task (rep 0) | ✓ | - | [trace](v1/traces/finished-last-task_rep0.json) |
| finished-last-task (rep 1) | ✓ | - | [trace](v1/traces/finished-last-task_rep1.json) |
| fourth-session-fading-accept (rep 0) | ✓ | - | [trace](v1/traces/fourth-session-fading-accept_rep0.json) |
| fourth-session-fading-accept (rep 1) | ✓ | - | [trace](v1/traces/fourth-session-fading-accept_rep1.json) |
| fourth-session-long-break (rep 1) | ✓ | - | [trace](v1/traces/fourth-session-long-break_rep1.json) |
| free-afternoon-switch (rep 0) | ✓ | - | [trace](v1/traces/free-afternoon-switch_rep0.json) |
| free-afternoon-switch (rep 1) | ✓ | - | [trace](v1/traces/free-afternoon-switch_rep1.json) |
| french-break-10 (rep 0) | ✓ | - | [trace](v1/traces/french-break-10_rep0.json) |
| french-break-10 (rep 1) | ✓ | - | [trace](v1/traces/french-break-10_rep1.json) |
| french-continue (rep 0) | ✓ | - | [trace](v1/traces/french-continue_rep0.json) |
| french-finished-tp (rep 0) | ✓ | - | [trace](v1/traces/french-finished-tp_rep0.json) |
| french-finished-tp (rep 1) | ✓ | - | [trace](v1/traces/french-finished-tp_rep1.json) |
| half-of-reading (rep 0) | ✓ | - | [trace](v1/traces/half-of-reading_rep0.json) |
| half-of-reading (rep 1) | ✓ | - | [trace](v1/traces/half-of-reading_rep1.json) |
| headache (rep 0) | ✓ | - | [trace](v1/traces/headache_rep0.json) |
| headache (rep 1) | ✓ | - | [trace](v1/traces/headache_rep1.json) |
| in-the-zone (rep 0) | ✓ | - | [trace](v1/traces/in-the-zone_rep0.json) |
| in-the-zone (rep 1) | ✓ | - | [trace](v1/traces/in-the-zone_rep1.json) |
| lab-in-5-hungry (rep 0) | ✓ | - | [trace](v1/traces/lab-in-5-hungry_rep0.json) |
| lab-in-5-hungry (rep 1) | ✓ | - | [trace](v1/traces/lab-in-5-hungry_rep1.json) |
| late-deadline-stress (rep 0) | ✓ | - | [trace](v1/traces/late-deadline-stress_rep0.json) |
| late-deadline-stress (rep 1) | ✓ | - | [trace](v1/traces/late-deadline-stress_rep1.json) |
| late-night-stop (rep 0) | ✓ | - | [trace](v1/traces/late-night-stop_rep0.json) |
| late-night-stop (rep 1) | ✓ | - | [trace](v1/traces/late-night-stop_rep1.json) |
| lecture-in-13-short-break (rep 0) | ✓ | - | [trace](v1/traces/lecture-in-13-short-break_rep0.json) |
| meeting-in-40-continue (rep 0) | ✓ | - | [trace](v1/traces/meeting-in-40-continue_rep0.json) |
| meeting-in-40-continue (rep 1) | ✓ | - | [trace](v1/traces/meeting-in-40-continue_rep1.json) |
| phone-distraction (rep 0) | ✓ | - | [trace](v1/traces/phone-distraction_rep0.json) |
| phone-distraction (rep 1) | ✓ | - | [trace](v1/traces/phone-distraction_rep1.json) |
| second-session-short-break (rep 1) | ✓ | - | [trace](v1/traces/second-session-short-break_rep1.json) |

Tokens (Focus, all cases): input 550, output 22,510, cache read 1,214,505. Runs on your Claude plan, so there's no per-token bill.

Mean latency per conversation: 9.1s.
