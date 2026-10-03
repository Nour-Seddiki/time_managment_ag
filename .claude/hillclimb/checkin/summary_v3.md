# Check-in eval - `v3`

Change: Fix the "coming up" note's dates: say today/tomorrow or give the full date, so far-off deadlines don't read as tonight

**train** 95% ± 9% (21 cases) · **test** 82% ± 18% (17 cases)

38 cases × 2 rep(s); 0 attempt(s) not scored (see errors.jsonl). Model: ['claude-sonnet-5']; judge: ["['claude-sonnet-5-5']"].

Scores are the share of cases passing (per case: mean over reps), with a 95% interval. n/a cases are left out of that metric.

| metric | score | 95% CI | n |
|---|---|---|---|
| **checkin_ok** | 89% | ±10% | 38 |
| no_early_timer | 100% | ±0% | 38 |
| acts_on_choice | 100% | ±0% | 20 |
| reflection | 97% | ±6% | 33 |
| task_status | 100% | ±0% | 38 |
| no_cal_writes | 100% | ±0% | 38 |
| concise | 100% | ±0% | 38 |
| check_in_q | 100% | ±0% | 38 |
| next_step | 96% | ±6% | 38 |
| context_fit | 95% | ±7% | 38 |
| tone | 100% | ±0% | 38 |

## By scenario type (checkin_ok)

| tag | score | n |
|---|---|---|
| break_ended | 100% | 5 |
| calendar_free | 100% | 1 |
| calendar_soon | 83% | 6 |
| energy | 100% | 7 |
| explicit_choice | 86% | 7 |
| late_night | 50% | 2 |
| streak | 75% | 4 |
| task_done | 100% | 6 |

## Cases

| case | ok | failed checks | trace |
|---|---|---|---|
| cramming-1am (rep 0) | ✗ | **next_step**: The student asked for one more session. Focus offered no concrete options, such as a 5-minute wrap-up, a stop, or a plan for sleep and the morning. It ended with an open 'can I convince you?' question, so no clear next step was settled. | [trace](v3/traces/cramming-1am_rep0.json) |
| cramming-1am (rep 1) | ✗ | **next_step**: Focus offered no options, such as a very short wrap-up or a quick note of what to review in the morning. It also did not accept the student's 'one more?' and only proposed bed with an open 'Sound okay?'. | [trace](v3/traces/cramming-1am_rep1.json) |
| explicit-25-conflicts-lecture (rep 0) | ✗ | **reflection**: never logged the reflection | [trace](v3/traces/explicit-25-conflicts-lecture_rep0.json) |
| explicit-25-conflicts-lecture (rep 1) | ✗ | **reflection**: never logged the reflection | [trace](v3/traces/explicit-25-conflicts-lecture_rep1.json) |
| fourth-session-long-break (rep 0) | ✗ | **context_fit**: A long break (15-30 min) was due after the 4th session in a row, but Focus offered only a short break or continuing, and never suggested a long break. | [trace](v3/traces/fourth-session-long-break_rep0.json) |
| fourth-session-long-break (rep 1) | ✗ | **next_step**: Focus offered three options (continue, switch task, short break), but the student never chose one, so no next step was settled by the end.; **context_fit**: A 15-30 minute long break was due after four sessions in a row, but Focus offered another 25-minute session, a task switch, or only a short break, which ignores the context. | [trace](v3/traces/fourth-session-long-break_rep1.json) |
| lecture-in-10-break (rep 0) | ✗ | **context_fit**: Focus said to head out for the lecture, then started a 10-minute break that ends exactly at 10:00. That leaves no time to get to class, and calling it "perfect timing" contradicts the key context. A shorter break, or a reminder to leave before it ends, would have fit. | [trace](v3/traces/lecture-in-10-break_rep0.json) |
| lecture-in-10-break (rep 1) | ✗ | **context_fit**: Focus started a 10-minute break with the lecture 10 minutes away, so the timer ends exactly at 10:00 and leaves no time to get to class. That contradicts its own earlier advice to head over now, and calling it "perfect timing" is wrong. | [trace](v3/traces/lecture-in-10-break_rep1.json) |
| after-long-break-short-again (rep 0) | ✓ | - | [trace](v3/traces/after-long-break-short-again_rep0.json) |
| after-long-break-short-again (rep 1) | ✓ | - | [trace](v3/traces/after-long-break-short-again_rep1.json) |
| almost-done-slides (rep 0) | ✓ | - | [trace](v3/traces/almost-done-slides_rep0.json) |
| almost-done-slides (rep 1) | ✓ | - | [trace](v3/traces/almost-done-slides_rep1.json) |
| bored-reading (rep 0) | ✓ | - | [trace](v3/traces/bored-reading_rep0.json) |
| bored-reading (rep 1) | ✓ | - | [trace](v3/traces/bored-reading_rep1.json) |
| break-ended-5-more (rep 0) | ✓ | - | [trace](v3/traces/break-ended-5-more_rep0.json) |
| break-ended-5-more (rep 1) | ✓ | - | [trace](v3/traces/break-ended-5-more_rep1.json) |
| break-ended-class-soon (rep 0) | ✓ | - | [trace](v3/traces/break-ended-class-soon_rep0.json) |
| break-ended-class-soon (rep 1) | ✓ | - | [trace](v3/traces/break-ended-class-soon_rep1.json) |
| break-ended-ready (rep 0) | ✓ | - | [trace](v3/traces/break-ended-ready_rep0.json) |
| break-ended-ready (rep 1) | ✓ | - | [trace](v3/traces/break-ended-ready_rep1.json) |
| bus-in-10 (rep 0) | ✓ | - | [trace](v3/traces/bus-in-10_rep0.json) |
| bus-in-10 (rep 1) | ✓ | - | [trace](v3/traces/bus-in-10_rep1.json) |
| exam-tomorrow-confused (rep 0) | ✓ | - | [trace](v3/traces/exam-tomorrow-confused_rep0.json) |
| exam-tomorrow-confused (rep 1) | ✓ | - | [trace](v3/traces/exam-tomorrow-confused_rep1.json) |
| exhausted-after-50 (rep 0) | ✓ | - | [trace](v3/traces/exhausted-after-50_rep0.json) |
| exhausted-after-50 (rep 1) | ✓ | - | [trace](v3/traces/exhausted-after-50_rep1.json) |
| explicit-15-before-leaving (rep 0) | ✓ | - | [trace](v3/traces/explicit-15-before-leaving_rep0.json) |
| explicit-15-before-leaving (rep 1) | ✓ | - | [trace](v3/traces/explicit-15-before-leaving_rep1.json) |
| explicit-15-break (rep 0) | ✓ | - | [trace](v3/traces/explicit-15-break_rep0.json) |
| explicit-15-break (rep 1) | ✓ | - | [trace](v3/traces/explicit-15-break_rep1.json) |
| explicit-another-25 (rep 0) | ✓ | - | [trace](v3/traces/explicit-another-25_rep0.json) |
| explicit-another-25 (rep 1) | ✓ | - | [trace](v3/traces/explicit-another-25_rep1.json) |
| explicit-done-for-today (rep 0) | ✓ | - | [trace](v3/traces/explicit-done-for-today_rep0.json) |
| explicit-done-for-today (rep 1) | ✓ | - | [trace](v3/traces/explicit-done-for-today_rep1.json) |
| explicit-essay-45 (rep 0) | ✓ | - | [trace](v3/traces/explicit-essay-45_rep0.json) |
| explicit-essay-45 (rep 1) | ✓ | - | [trace](v3/traces/explicit-essay-45_rep1.json) |
| finished-essay-break (rep 0) | ✓ | - | [trace](v3/traces/finished-essay-break_rep0.json) |
| finished-essay-break (rep 1) | ✓ | - | [trace](v3/traces/finished-essay-break_rep1.json) |
| finished-lab-report (rep 0) | ✓ | - | [trace](v3/traces/finished-lab-report_rep0.json) |
| finished-lab-report (rep 1) | ✓ | - | [trace](v3/traces/finished-lab-report_rep1.json) |
| finished-last-task (rep 0) | ✓ | - | [trace](v3/traces/finished-last-task_rep0.json) |
| finished-last-task (rep 1) | ✓ | - | [trace](v3/traces/finished-last-task_rep1.json) |
| fourth-session-fading-accept (rep 0) | ✓ | - | [trace](v3/traces/fourth-session-fading-accept_rep0.json) |
| fourth-session-fading-accept (rep 1) | ✓ | - | [trace](v3/traces/fourth-session-fading-accept_rep1.json) |
| free-afternoon-switch (rep 0) | ✓ | - | [trace](v3/traces/free-afternoon-switch_rep0.json) |
| free-afternoon-switch (rep 1) | ✓ | - | [trace](v3/traces/free-afternoon-switch_rep1.json) |
| french-break-10 (rep 0) | ✓ | - | [trace](v3/traces/french-break-10_rep0.json) |
| french-break-10 (rep 1) | ✓ | - | [trace](v3/traces/french-break-10_rep1.json) |
| french-break-ended-ready (rep 0) | ✓ | - | [trace](v3/traces/french-break-ended-ready_rep0.json) |
| french-break-ended-ready (rep 1) | ✓ | - | [trace](v3/traces/french-break-ended-ready_rep1.json) |
| french-continue (rep 0) | ✓ | - | [trace](v3/traces/french-continue_rep0.json) |
| french-continue (rep 1) | ✓ | - | [trace](v3/traces/french-continue_rep1.json) |
| french-finished-tp (rep 0) | ✓ | - | [trace](v3/traces/french-finished-tp_rep0.json) |
| french-finished-tp (rep 1) | ✓ | - | [trace](v3/traces/french-finished-tp_rep1.json) |
| half-of-reading (rep 0) | ✓ | - | [trace](v3/traces/half-of-reading_rep0.json) |
| half-of-reading (rep 1) | ✓ | - | [trace](v3/traces/half-of-reading_rep1.json) |
| headache (rep 0) | ✓ | - | [trace](v3/traces/headache_rep0.json) |
| headache (rep 1) | ✓ | - | [trace](v3/traces/headache_rep1.json) |
| in-the-zone (rep 0) | ✓ | - | [trace](v3/traces/in-the-zone_rep0.json) |
| in-the-zone (rep 1) | ✓ | - | [trace](v3/traces/in-the-zone_rep1.json) |
| lab-in-5-hungry (rep 0) | ✓ | - | [trace](v3/traces/lab-in-5-hungry_rep0.json) |
| lab-in-5-hungry (rep 1) | ✓ | - | [trace](v3/traces/lab-in-5-hungry_rep1.json) |
| late-deadline-stress (rep 0) | ✓ | - | [trace](v3/traces/late-deadline-stress_rep0.json) |
| late-deadline-stress (rep 1) | ✓ | - | [trace](v3/traces/late-deadline-stress_rep1.json) |
| late-night-stop (rep 0) | ✓ | - | [trace](v3/traces/late-night-stop_rep0.json) |
| late-night-stop (rep 1) | ✓ | - | [trace](v3/traces/late-night-stop_rep1.json) |
| lecture-in-13-short-break (rep 0) | ✓ | - | [trace](v3/traces/lecture-in-13-short-break_rep0.json) |
| lecture-in-13-short-break (rep 1) | ✓ | - | [trace](v3/traces/lecture-in-13-short-break_rep1.json) |
| long-break-ended-evening (rep 0) | ✓ | - | [trace](v3/traces/long-break-ended-evening_rep0.json) |
| long-break-ended-evening (rep 1) | ✓ | - | [trace](v3/traces/long-break-ended-evening_rep1.json) |
| meeting-in-40-continue (rep 0) | ✓ | - | [trace](v3/traces/meeting-in-40-continue_rep0.json) |
| meeting-in-40-continue (rep 1) | ✓ | - | [trace](v3/traces/meeting-in-40-continue_rep1.json) |
| phone-distraction (rep 0) | ✓ | - | [trace](v3/traces/phone-distraction_rep0.json) |
| phone-distraction (rep 1) | ✓ | - | [trace](v3/traces/phone-distraction_rep1.json) |
| second-session-short-break (rep 0) | ✓ | - | [trace](v3/traces/second-session-short-break_rep0.json) |
| second-session-short-break (rep 1) | ✓ | - | [trace](v3/traces/second-session-short-break_rep1.json) |

Tokens (Focus, all cases): input 544, output 22,687, cache read 1,263,407. Runs on your Claude plan, so there's no per-token bill.

Mean latency per conversation: 9.0s.
