# Check-in eval - `baseline`

Change: baseline

**train** 67% ± 20% (21 cases) · **test** 71% ± 22% (17 cases)

38 cases × 2 rep(s); 0 attempt(s) not scored (see errors.jsonl). Model: ['claude-sonnet-5']; judge: ["['claude-sonnet-5-5']"].

Scores are the share of cases passing (per case: mean over reps), with a 95% interval. n/a cases are left out of that metric.

| metric | score | 95% CI | n |
|---|---|---|---|
| **checkin_ok** | 68% | ±15% | 38 |
| no_early_timer | 100% | ±0% | 38 |
| acts_on_choice | 75% | ±19% | 20 |
| reflection | 100% | ±0% | 33 |
| task_status | 100% | ±0% | 38 |
| no_cal_writes | 100% | ±0% | 38 |
| concise | 100% | ±0% | 38 |
| check_in_q | 100% | ±0% | 38 |
| next_step | 88% | ±10% | 38 |
| context_fit | 80% | ±13% | 38 |
| tone | 97% | ±5% | 38 |

## By scenario type (checkin_ok)

| tag | score | n |
|---|---|---|
| break_ended | 30% | 5 |
| calendar_free | 100% | 1 |
| calendar_soon | 8% | 6 |
| energy | 100% | 7 |
| explicit_choice | 86% | 7 |
| late_night | 50% | 2 |
| streak | 88% | 4 |
| task_done | 92% | 6 |

## Cases

| case | ok | failed checks | trace |
|---|---|---|---|
| break-ended-5-more (rep 0) | ✗ | **tone**: The tone is warm and not guilt-tripping, but the reply is padded: it says the same thing twice ('let's just stretch the break 5 more minutes' and 'Got it, 5 more minutes of break'). | [trace](baseline/traces/break-ended-5-more_rep0.json) |
| break-ended-class-soon (rep 0) | ✗ | **next_step**: The student said "ok what now" and Focus just repeated the 25-minute block suggestion with a vague "switch to something else", so there was no concrete set of options or clear next step.; **context_fit**: The lecture starts in 10 minutes, so a 25-minute block doesn't fit, yet Focus proposed one twice and never mentioned the class. | [trace](baseline/traces/break-ended-class-soon_rep0.json) |
| break-ended-class-soon (rep 1) | ✗ | **next_step**: Focus's only concrete proposal was a 25-minute block that doesn't fit before the lecture, so the student has no workable next step.; **context_fit**: The lecture starts in 10 minutes, yet Focus proposed a 25-minute focus block and never mentioned class or a very short review. | [trace](baseline/traces/break-ended-class-soon_rep1.json) |
| break-ended-ready (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](baseline/traces/break-ended-ready_rep0.json) |
| break-ended-ready (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](baseline/traces/break-ended-ready_rep1.json) |
| bus-in-10 (rep 0) | ✗ | **context_fit**: The bus leaves in 10 minutes and the student should pack up, but Focus suggested continuing on questions 4-5 or taking a break, and never mentioned the bus or suggested wrapping up. | [trace](baseline/traces/bus-in-10_rep0.json) |
| bus-in-10 (rep 1) | ✗ | **next_step**: The final offer is to keep going or take a 5-minute break, and neither fits the bus leaving in 10 minutes. The student gets no workable next step, such as packing up and picking up questions 4-5 later.; **context_fit**: Focus ignored that the bus leaves at 16:45 and it is time to pack up. It suggested starting questions 4-5 now or taking a break, which contradicts the key context. | [trace](baseline/traces/bus-in-10_rep1.json) |
| cramming-1am (rep 0) | ✗ | **context_fit**: At 01:10 with a 09:00 exam, sleep should come first, but Focus said 'nothing rushing you' and offered another full 25-minute genetics session. It did not suggest sleep or a very short wrap-up. | [trace](baseline/traces/cramming-1am_rep0.json) |
| cramming-1am (rep 1) | ✗ | **context_fit**: At 1am with a 9am exam, sleep should come first with at most a very short wrap-up, but Focus offered a full 25-minute round as an equal option and never mentioned the exam or a short wrap-up. | [trace](baseline/traces/cramming-1am_rep1.json) |
| exam-tomorrow-confused (rep 1) | ✗ | **context_fit**: The exam is tomorrow and the student is stuck on integration by parts, yet Focus offered 'switch to something else' as an equal option and never steered toward calculus or a different approach to the sticking point.; **tone**: The tone is warm, but the same three-option question is asked twice in a row, which is padding. | [trace](baseline/traces/exam-tomorrow-confused_rep1.json) |
| explicit-15-break (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](baseline/traces/explicit-15-break_rep0.json) |
| explicit-essay-45 (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student had already said "let's do the essay now for 45 min", but Focus didn't start it and asked "Starting it now?", which re-asks something already answered. | [trace](baseline/traces/explicit-essay-45_rep1.json) |
| french-break-ended-ready (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student said "ok je suis prêt", which accepted the proposal to resume the project, but Focus asked again "On repart... pour 25 minutes ?" instead of starting the session, so it re-asked something already answered. | [trace](baseline/traces/french-break-ended-ready_rep0.json) |
| french-finished-tp (rep 0) | ✗ | **context_fit**: Focus correctly marked the TP done, pointed to analysis revision as next, and replied in French. But it said the revision is due "vendredi", while the key context says the exam is Thursday morning (due 2026-10-08, a Thursday). That misstates the deadline and could make the student think they have an extra day. | [trace](baseline/traces/french-finished-tp_rep0.json) |
| lab-in-5-hungry (rep 0) | ✗ | **next_step**: Focus offered only one vague option, a 'proper lunch break' and picking up afterward. It gave no concrete plan that fits the 13:00 lab, and the conversation ends on an open question.; **context_fit**: The lab starts in 5 minutes, so a 'proper lunch break' doesn't fit. Focus never mentioned the lab or the need to grab food quickly and head over, and it implied more studying right after the break. | [trace](baseline/traces/lab-in-5-hungry_rep0.json) |
| lab-in-5-hungry (rep 1) | ✗ | **next_step**: Focus offered only one yes/no proposal, to eat now and resume chapter 6 in 45-60 minutes, and never mentioned the lab, so the student has no workable plan.; **context_fit**: It ignored that the chemistry lab starts in 5 minutes and runs 13:00-15:00, so resuming in 45-60 minutes lands mid-lab and it never suggests heading to the lab. | [trace](baseline/traces/lab-in-5-hungry_rep1.json) |
| lecture-in-10-break (rep 0) | ✗ | **context_fit**: The lecture starts in 10 minutes, but Focus offered to keep going or switch tasks and never mentioned the lecture or when to head to class. | [trace](baseline/traces/lecture-in-10-break_rep0.json) |
| lecture-in-10-break (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student clearly chose a break with 'yeah break', but Focus asked 'Want me to start it?' instead of starting it, which re-asks something the student had already answered.; **context_fit**: Focus never mentions the lecture starting in 10 minutes, and it offered to keep going or switch tasks even though there was no time for that; the 5-minute break only fits by luck. | [trace](baseline/traces/lecture-in-10-break_rep1.json) |
| lecture-in-13-short-break (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session; **context_fit**: Focus never mentioned the lecture starting in 13 minutes. It offered to keep going on the lab report or switch tasks with no time limit, and it did not say how the break fits before the lecture. | [trace](baseline/traces/lecture-in-13-short-break_rep0.json) |
| lecture-in-13-short-break (rep 1) | ✗ | **context_fit**: Focus never mentioned the 11:00 lecture, 13 minutes away. It offered to keep rolling on the lab report with no time caveat, and it didn't say what to do with the time left after the break. The 5-minute break fits only by chance. | [trace](baseline/traces/lecture-in-13-short-break_rep1.json) |
| long-break-ended-evening (rep 1) | ✗ | **context_fit**: Focus did put biochemistry first, but it said the revision is due Friday when the exam is on Thursday (2026-10-08). That misstates the key deadline. | [trace](baseline/traces/long-break-ended-evening_rep1.json) |
| meeting-in-40-continue (rep 0) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](baseline/traces/meeting-in-40-continue_rep0.json) |
| meeting-in-40-continue (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session | [trace](baseline/traces/meeting-in-40-continue_rep1.json) |
| second-session-short-break (rep 1) | ✗ | **acts_on_choice**: did not start the chosen session; **next_step**: The student had already chosen "break", but Focus asked "Want me to start the break timer now?" instead of starting it, which re-asks a settled choice and leaves the next step unexecuted. | [trace](baseline/traces/second-session-short-break_rep1.json) |
| after-long-break-short-again (rep 0) | ✓ | - | [trace](baseline/traces/after-long-break-short-again_rep0.json) |
| after-long-break-short-again (rep 1) | ✓ | - | [trace](baseline/traces/after-long-break-short-again_rep1.json) |
| almost-done-slides (rep 0) | ✓ | - | [trace](baseline/traces/almost-done-slides_rep0.json) |
| almost-done-slides (rep 1) | ✓ | - | [trace](baseline/traces/almost-done-slides_rep1.json) |
| bored-reading (rep 0) | ✓ | - | [trace](baseline/traces/bored-reading_rep0.json) |
| bored-reading (rep 1) | ✓ | - | [trace](baseline/traces/bored-reading_rep1.json) |
| break-ended-5-more (rep 1) | ✓ | - | [trace](baseline/traces/break-ended-5-more_rep1.json) |
| exam-tomorrow-confused (rep 0) | ✓ | - | [trace](baseline/traces/exam-tomorrow-confused_rep0.json) |
| exhausted-after-50 (rep 0) | ✓ | - | [trace](baseline/traces/exhausted-after-50_rep0.json) |
| exhausted-after-50 (rep 1) | ✓ | - | [trace](baseline/traces/exhausted-after-50_rep1.json) |
| explicit-15-before-leaving (rep 0) | ✓ | - | [trace](baseline/traces/explicit-15-before-leaving_rep0.json) |
| explicit-15-before-leaving (rep 1) | ✓ | - | [trace](baseline/traces/explicit-15-before-leaving_rep1.json) |
| explicit-15-break (rep 1) | ✓ | - | [trace](baseline/traces/explicit-15-break_rep1.json) |
| explicit-25-conflicts-lecture (rep 0) | ✓ | - | [trace](baseline/traces/explicit-25-conflicts-lecture_rep0.json) |
| explicit-25-conflicts-lecture (rep 1) | ✓ | - | [trace](baseline/traces/explicit-25-conflicts-lecture_rep1.json) |
| explicit-another-25 (rep 0) | ✓ | - | [trace](baseline/traces/explicit-another-25_rep0.json) |
| explicit-another-25 (rep 1) | ✓ | - | [trace](baseline/traces/explicit-another-25_rep1.json) |
| explicit-done-for-today (rep 0) | ✓ | - | [trace](baseline/traces/explicit-done-for-today_rep0.json) |
| explicit-done-for-today (rep 1) | ✓ | - | [trace](baseline/traces/explicit-done-for-today_rep1.json) |
| explicit-essay-45 (rep 0) | ✓ | - | [trace](baseline/traces/explicit-essay-45_rep0.json) |
| finished-essay-break (rep 0) | ✓ | - | [trace](baseline/traces/finished-essay-break_rep0.json) |
| finished-essay-break (rep 1) | ✓ | - | [trace](baseline/traces/finished-essay-break_rep1.json) |
| finished-lab-report (rep 0) | ✓ | - | [trace](baseline/traces/finished-lab-report_rep0.json) |
| finished-lab-report (rep 1) | ✓ | - | [trace](baseline/traces/finished-lab-report_rep1.json) |
| finished-last-task (rep 0) | ✓ | - | [trace](baseline/traces/finished-last-task_rep0.json) |
| finished-last-task (rep 1) | ✓ | - | [trace](baseline/traces/finished-last-task_rep1.json) |
| fourth-session-fading-accept (rep 0) | ✓ | - | [trace](baseline/traces/fourth-session-fading-accept_rep0.json) |
| fourth-session-fading-accept (rep 1) | ✓ | - | [trace](baseline/traces/fourth-session-fading-accept_rep1.json) |
| fourth-session-long-break (rep 0) | ✓ | - | [trace](baseline/traces/fourth-session-long-break_rep0.json) |
| fourth-session-long-break (rep 1) | ✓ | - | [trace](baseline/traces/fourth-session-long-break_rep1.json) |
| free-afternoon-switch (rep 0) | ✓ | - | [trace](baseline/traces/free-afternoon-switch_rep0.json) |
| free-afternoon-switch (rep 1) | ✓ | - | [trace](baseline/traces/free-afternoon-switch_rep1.json) |
| french-break-10 (rep 0) | ✓ | - | [trace](baseline/traces/french-break-10_rep0.json) |
| french-break-10 (rep 1) | ✓ | - | [trace](baseline/traces/french-break-10_rep1.json) |
| french-break-ended-ready (rep 1) | ✓ | - | [trace](baseline/traces/french-break-ended-ready_rep1.json) |
| french-continue (rep 0) | ✓ | - | [trace](baseline/traces/french-continue_rep0.json) |
| french-continue (rep 1) | ✓ | - | [trace](baseline/traces/french-continue_rep1.json) |
| french-finished-tp (rep 1) | ✓ | - | [trace](baseline/traces/french-finished-tp_rep1.json) |
| half-of-reading (rep 0) | ✓ | - | [trace](baseline/traces/half-of-reading_rep0.json) |
| half-of-reading (rep 1) | ✓ | - | [trace](baseline/traces/half-of-reading_rep1.json) |
| headache (rep 0) | ✓ | - | [trace](baseline/traces/headache_rep0.json) |
| headache (rep 1) | ✓ | - | [trace](baseline/traces/headache_rep1.json) |
| in-the-zone (rep 0) | ✓ | - | [trace](baseline/traces/in-the-zone_rep0.json) |
| in-the-zone (rep 1) | ✓ | - | [trace](baseline/traces/in-the-zone_rep1.json) |
| late-deadline-stress (rep 0) | ✓ | - | [trace](baseline/traces/late-deadline-stress_rep0.json) |
| late-deadline-stress (rep 1) | ✓ | - | [trace](baseline/traces/late-deadline-stress_rep1.json) |
| late-night-stop (rep 0) | ✓ | - | [trace](baseline/traces/late-night-stop_rep0.json) |
| late-night-stop (rep 1) | ✓ | - | [trace](baseline/traces/late-night-stop_rep1.json) |
| long-break-ended-evening (rep 0) | ✓ | - | [trace](baseline/traces/long-break-ended-evening_rep0.json) |
| phone-distraction (rep 0) | ✓ | - | [trace](baseline/traces/phone-distraction_rep0.json) |
| phone-distraction (rep 1) | ✓ | - | [trace](baseline/traces/phone-distraction_rep1.json) |
| second-session-short-break (rep 0) | ✓ | - | [trace](baseline/traces/second-session-short-break_rep0.json) |

Tokens (Focus, all cases): input 562, output 23,985, cache read 1,211,935. Runs on your Claude plan, so there's no per-token bill.

Mean latency per conversation: 9.1s.
