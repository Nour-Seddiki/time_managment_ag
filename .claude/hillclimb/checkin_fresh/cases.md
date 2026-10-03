# Check-in eval inputs

20 cases. Each fires the real "session ended" event at Focus with the fixed clock, calendar and tasks shown, then plays the student's replies in order.

| id | tags | student turns | expected |
|---|---|---|---|
| f-tutorial-in-8 | calendar_soon | 1 | no timer started; log rating 3; no task marked done |
| f-call-in-30-continue | calendar_soon, consent | 2 | after turn 2: start focus 10-25 min on t1; log rating 4; no task marked done |
| f-train-in-20 | calendar_soon | 1 | no timer started; log rating 5; no task marked done |
| f-midterm-in-2h | calendar_soon | 2 | no timer started; log rating 4; no task marked done |
| f-anxious | energy | 1 | no timer started; log rating 2; no task marked done |
| f-on-fire-50-more | energy, consent | 1 | after turn 1: start focus 50-50 min on t1; log rating 5; no task marked done |
| f-sleepy-after-lunch | energy | 1 | no timer started; log rating 3; no task marked done |
| f-finished-article | task_done | 1 | no timer started; log rating 4; mark t1 done |
| f-problems-1-to-6 | task_done | 1 | no timer started; log rating 3; no task marked done |
| f-finished-summary-break | task_done, consent | 2 | after turn 2: start break 3-10 min; log rating 5; mark t1 done |
| f-30-more-before-lab | explicit_choice, calendar_soon | 1 | after turn 1: start focus 5-20 min on t1 (optional); log rating 4; no task marked done |
| f-switch-accounting-25 | explicit_choice, consent | 1 | after turn 1: start focus 25-25 min on t2; log rating 4; no task marked done |
| f-enough-for-today | explicit_choice | 1 | no timer started; log rating 3; no task marked done |
| f-fourth-session-plain | streak | 1 | no timer started; log rating 4; no task marked done |
| f-fourth-session-break | streak, consent | 2 | after turn 2: start break 15-30 min; log rating 4; no task marked done |
| f-after-long-break-short | streak, consent | 2 | after turn 2: start break 3-10 min; log rating 3; no task marked done |
| f-break-ended-resume-fr | break_ended, consent, french | 1 | after turn 1: start focus 15-50 min on t1; no task marked done |
| f-break-ended-meeting-soon | break_ended, calendar_soon | 1 | no timer started; no task marked done |
| f-near-midnight | late_night | 1 | no timer started; log rating 4; no task marked done |
| f-free-day-stats-40 | calendar_free, consent | 1 | after turn 1: start focus 40-40 min on t2; log rating 4; no task marked done |

## f-tutorial-in-8

- **Time:** 2026-10-14 15:52
- **Ended:** 25-min focus on "Macro problem set"
- **Calendar:** Economics tutorial 2026-10-14 16:00
- **Tasks:** t1 Macro problem set (due 2026-10-16T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "3/5 ok-ish"
- **Judge's key context:** The economics tutorial starts at 16:00, 8 minutes from now; no focus block fits, so a short break or getting ready is the right suggestion.

## f-call-in-30-continue

- **Time:** 2026-10-14 09:30
- **Ended:** 25-min focus on "CV update"
- **Calendar:** Call with internship supervisor 2026-10-14 10:00
- **Tasks:** t1 CV update (due 2026-10-15T12:00, high)
- **Earlier sessions today:** 0
- **Student says:** "4, got the skills section done" → "keep going"
- **Judge's key context:** The supervisor call is at 10:00, 30 minutes away; the next block must end before it.

## f-train-in-20

- **Time:** 2026-10-14 17:40
- **Ended:** 25-min focus on "Read chapter 9"
- **Calendar:** Train to Sousse 2026-10-14 18:00
- **Tasks:** t1 Read chapter 9 (due 2026-10-19T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "5/5 really good"
- **Judge's key context:** The train leaves at 18:00, in 20 minutes; Focus should suggest wrapping up and getting ready rather than a full block.

## f-midterm-in-2h

- **Time:** 2026-10-14 12:00
- **Ended:** 25-min focus on "Stats midterm revision"
- **Calendar:** Statistics midterm 2026-10-14 14:00
- **Tasks:** t1 Stats midterm revision (due 2026-10-14T14:00, high); t2 Novel reading (due 2026-10-21T23:59, low)
- **Earlier sessions today:** 0
- **Student says:** "4, feeling more confident" → "what next?"
- **Judge's key context:** The statistics midterm is at 14:00, two hours away; the next steps should stay on stats revision (with time to eat and arrive), not switch to the novel due next week.

## f-anxious

- **Time:** 2026-10-14 16:10
- **Ended:** 25-min focus on "Thesis outline"
- **Calendar:** empty
- **Tasks:** t1 Thesis outline (due 2026-10-16T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "2/5, anxious about the deadline and can't think straight"
- **Judge's key context:** The student is anxious and can't focus; a good reply suggests a calming break or a smaller next step, without guilt.

## f-on-fire-50-more

- **Time:** 2026-10-14 14:30
- **Ended:** 50-min focus on "Web app project"
- **Calendar:** Football practice 2026-10-14 18:00
- **Tasks:** t1 Web app project (due 2026-10-17T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "5, I'm on fire, keep going 50 more"
- **Judge's key context:** The student explicitly wants 50 more minutes and has time before 18:00; Focus should respect the choice (a brief mention of a break is fine).

## f-sleepy-after-lunch

- **Time:** 2026-10-14 15:00
- **Ended:** 25-min focus on "Biology flashcards"
- **Calendar:** empty
- **Tasks:** t1 Biology flashcards (due 2026-10-16T09:00, medium); t2 Lab report formatting (due 2026-10-17T23:59, low)
- **Earlier sessions today:** 0
- **Student says:** "3, so sleepy after lunch"
- **Judge's key context:** Post-lunch slump; a short active break (walk, water) or a lighter task is a sensible suggestion, not pushing straight into the same work.

## f-finished-article

- **Time:** 2026-10-14 11:00
- **Ended:** 25-min focus on "Read article for seminar"
- **Calendar:** empty
- **Tasks:** t1 Read article for seminar (due 2026-10-14T18:00, high); t2 Chemistry lab worksheet (due 2026-10-15T23:59, medium); t3 Essay plan (due 2026-10-21T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "finished the article! 4"
- **Judge's key context:** The article is done; the chemistry worksheet due tomorrow is the next priority, ahead of the essay plan due next week.

## f-problems-1-to-6

- **Time:** 2026-10-14 10:30
- **Ended:** 25-min focus on "Physics problems 1-10"
- **Calendar:** empty
- **Tasks:** t1 Physics problems 1-10 (due 2026-10-15T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "did 1 to 6, 3/5"
- **Judge's key context:** Problems 7-10 are still left, so the task is not done.

## f-finished-summary-break

- **Time:** 2026-10-14 16:40
- **Ended:** 25-min focus on "Chapter summary"
- **Calendar:** empty
- **Tasks:** t1 Chapter summary (due 2026-10-15T09:00, high); t2 Psychology quiz prep (due 2026-10-16T14:00, medium)
- **Earlier sessions today:** 0
- **Student says:** "done with the summary, 5" → "short break"
- **Judge's key context:** The summary is finished and the student asked for a short break.

## f-30-more-before-lab

- **Time:** 2026-10-14 10:35
- **Ended:** 25-min focus on "Circuits homework"
- **Calendar:** Electronics lab session 2026-10-14 11:00
- **Tasks:** t1 Circuits homework (due 2026-10-15T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4/5, give me another 30"
- **Judge's key context:** 30 more minutes would run into the 11:00 lab (25 minutes away); Focus should point out the conflict and shorten the block or check, not start 30 minutes.

## f-switch-accounting-25

- **Time:** 2026-10-14 13:00
- **Ended:** 25-min focus on "French vocabulary"
- **Calendar:** empty
- **Tasks:** t1 French vocabulary (due 2026-10-16T23:59, low); t2 Accounting case study (due 2026-10-15T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4. switch to the accounting case, 25 min"
- **Judge's key context:** The student explicitly chose 25 minutes on the accounting case.

## f-enough-for-today

- **Time:** 2026-10-14 18:30
- **Ended:** 25-min focus on "Marketing report"
- **Calendar:** empty
- **Tasks:** t1 Marketing report (due 2026-10-17T23:59, medium)
- **Earlier sessions today:** 4
- **Student says:** "that's enough for today, 3"
- **Judge's key context:** The student is done for the day; Focus should accept it with a brief recap and not push more work.

## f-fourth-session-plain

- **Time:** 2026-10-14 15:40
- **Ended:** 25-min focus on "Algorithms assignment"
- **Calendar:** empty
- **Tasks:** t1 Algorithms assignment (due 2026-10-16T23:59, high)
- **Earlier sessions today:** 6
- **Student says:** "4"
- **Judge's key context:** This was the 4th focus session in a row with only short breaks; a long break (15-30 minutes) is due.

## f-fourth-session-break

- **Time:** 2026-10-14 11:40
- **Ended:** 25-min focus on "Anatomy revision"
- **Calendar:** empty
- **Tasks:** t1 Anatomy revision (due 2026-10-17T09:00, high)
- **Earlier sessions today:** 6
- **Student says:** "4/5" → "break"
- **Judge's key context:** Fourth focus session in a row; the break should be a long one (15-30 minutes).

## f-after-long-break-short

- **Time:** 2026-10-14 13:10
- **Ended:** 25-min focus on "Statistics project"
- **Calendar:** empty
- **Tasks:** t1 Statistics project (due 2026-10-18T23:59, medium)
- **Earlier sessions today:** 9
- **Student says:** "3" → "break please"
- **Judge's key context:** A long lunch break already happened two sessions ago, so a short break fits now.

## f-break-ended-resume-fr

- **Time:** 2026-10-14 10:35
- **Ended:** 5-min break on "Petite pause"
- **Calendar:** Déjeuner avec Amira 2026-10-14 12:30
- **Tasks:** t1 Rapport de stage (due 2026-10-16T23:59, high); t2 Lecture d'article (due 2026-10-20T23:59, low)
- **Earlier sessions today:** 1
- **Student says:** "ok je suis prêt, on reprend le rapport"
- **Judge's key context:** The student writes in French and explicitly wants to resume the internship report.

## f-break-ended-meeting-soon

- **Time:** 2026-10-14 14:50
- **Ended:** 5-min break on "Short break"
- **Calendar:** Supervisor meeting 2026-10-14 15:00
- **Tasks:** t1 Thesis chapter 2 (due 2026-10-20T23:59, high)
- **Earlier sessions today:** 1
- **Student says:** "what should I do now?"
- **Judge's key context:** The supervisor meeting starts at 15:00, in 10 minutes; Focus should suggest preparing for it, not a 25-minute block.

## f-near-midnight

- **Time:** 2026-10-14 23:50
- **Ended:** 25-min focus on "Comparative politics essay"
- **Calendar:** Morning lecture 2026-10-15 09:00
- **Tasks:** t1 Comparative politics essay (due 2026-10-17T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "4, should I keep going?"
- **Judge's key context:** It is 23:50 with a 09:00 lecture tomorrow and the essay isn't due for three days; Focus should recommend stopping for the night.

## f-free-day-stats-40

- **Time:** 2026-10-14 10:00
- **Ended:** 25-min focus on "German essay"
- **Calendar:** Dinner at grandma's 2026-10-14 19:00
- **Tasks:** t1 German essay (due 2026-10-19T23:59, medium); t2 Stats homework 5 (due 2026-10-16T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4, now the stats homework for 40 min"
- **Judge's key context:** The student explicitly chose 40 minutes on the stats homework; the day is free until 19:00.
