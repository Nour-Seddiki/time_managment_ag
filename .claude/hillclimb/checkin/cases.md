# Check-in eval inputs

38 cases. Each fires the real "session ended" event at Focus with the fixed clock, calendar and tasks shown, then plays the student's replies in order.

| id | tags | student turns | expected |
|---|---|---|---|
| lecture-in-13-short-break | calendar_soon, consent | 2 | after turn 2: start break 3-10 min; log rating 4; no task marked done |
| meeting-in-40-continue | calendar_soon, consent | 2 | after turn 2: start focus 10-40 min on t1; log rating 4; no task marked done |
| exam-tomorrow-confused | calendar_soon | 1 | no timer started; log rating 3; no task marked done |
| lab-in-5-hungry | calendar_soon | 1 | no timer started; log rating 2; no task marked done |
| free-afternoon-switch | calendar_free, consent | 2 | after turn 2: start focus 20-30 min on t2; log rating 4; no task marked done |
| bus-in-10 | calendar_soon | 1 | no timer started; log rating 5; no task marked done |
| lecture-in-10-break | calendar_soon, consent | 2 | after turn 2: start break 3-10 min; log rating 3; no task marked done |
| exhausted-after-50 | energy | 1 | no timer started; log rating 4; no task marked done |
| in-the-zone | energy | 1 | no timer started; log rating 5; no task marked done |
| phone-distraction | energy | 1 | no timer started; log rating 2; no task marked done |
| headache | energy | 1 | no timer started; log rating 1; no task marked done |
| bored-reading | energy | 1 | no timer started; log rating 3; no task marked done |
| french-continue | energy, consent, french | 2 | after turn 2: start focus 15-50 min on t1; log rating 4; no task marked done |
| late-deadline-stress | energy | 1 | no timer started; log rating 3; no task marked done |
| finished-lab-report | task_done | 1 | no timer started; log rating 5; mark t1 done |
| finished-essay-break | task_done, consent | 2 | after turn 2: start break 9-11 min; log rating 4; mark t1 done |
| almost-done-slides | task_done | 1 | no timer started; log rating 4; no task marked done |
| french-finished-tp | task_done, french | 1 | no timer started; log rating 5; mark t1 done |
| finished-last-task | task_done | 1 | no timer started; log rating 4; mark t1 done |
| half-of-reading | task_done | 1 | no timer started; log rating 3; no task marked done |
| explicit-another-25 | explicit_choice, consent | 1 | after turn 1: start focus 25-25 min on t1; log rating 4; no task marked done |
| explicit-15-break | explicit_choice, consent | 1 | after turn 1: start break 15-15 min; log rating 3; no task marked done |
| explicit-essay-45 | explicit_choice, consent | 1 | after turn 1: start focus 45-45 min on t2; log reflection; no task marked done |
| explicit-15-before-leaving | explicit_choice, consent | 1 | after turn 1: start focus 15-15 min on t1; log rating 5; no task marked done |
| explicit-done-for-today | explicit_choice | 1 | no timer started; log rating 4; no task marked done |
| french-break-10 | explicit_choice, consent, french | 1 | after turn 1: start break 10-10 min; log rating 3; no task marked done |
| explicit-25-conflicts-lecture | explicit_choice, calendar_soon | 1 | after turn 1: start focus 5-20 min on t1 (optional); log rating 4; no task marked done |
| fourth-session-long-break | streak | 1 | no timer started; log rating 4; no task marked done |
| fourth-session-fading-accept | streak, consent | 2 | after turn 2: start break 15-30 min; log rating 3; no task marked done |
| second-session-short-break | streak, consent | 2 | after turn 2: start break 3-10 min; log rating 4; no task marked done |
| after-long-break-short-again | streak, consent | 2 | after turn 2: start break 3-10 min; log rating 4; no task marked done |
| break-ended-ready | break_ended, consent | 1 | after turn 1: start focus 15-50 min on t1; no task marked done |
| break-ended-5-more | break_ended, consent | 1 | after turn 1: start break 5-5 min; no task marked done |
| break-ended-class-soon | break_ended, calendar_soon | 1 | no timer started; no task marked done |
| long-break-ended-evening | break_ended | 1 | no timer started; no task marked done |
| french-break-ended-ready | break_ended, consent, french | 1 | after turn 1: start focus 15-50 min on t1; no task marked done |
| late-night-stop | late_night | 1 | no timer started; log rating 4; no task marked done |
| cramming-1am | late_night | 1 | no timer started; log rating 3; no task marked done |

## lecture-in-13-short-break

- **Time:** 2026-10-05 10:47
- **Ended:** 25-min focus on "Physics lab report"
- **Calendar:** Linear Algebra lecture 2026-10-05 11:00
- **Tasks:** t1 Physics lab report (due 2026-10-07T23:59, high); t2 Stats homework 3 (due 2026-10-09T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "4/5 got the intro done" → "ok short break then"
- **Judge's key context:** The Linear Algebra lecture starts at 11:00, 13 minutes from now, so a full 25-minute focus block does not fit.

## meeting-in-40-continue

- **Time:** 2026-10-05 14:20
- **Ended:** 25-min focus on "ML project: data cleaning"
- **Calendar:** Project group meeting 2026-10-05 15:00
- **Tasks:** t1 ML project: data cleaning (due 2026-10-08T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "pretty good, 4" → "let's keep going on the same thing"
- **Judge's key context:** The project group meeting starts at 15:00, 40 minutes from now; the next block should end before it.

## exam-tomorrow-confused

- **Time:** 2026-10-05 19:30
- **Ended:** 25-min focus on "Calculus revision"
- **Calendar:** Calculus exam 2026-10-06 09:00
- **Tasks:** t1 Calculus revision (due 2026-10-06T09:00, high); t2 History essay draft (due 2026-10-12T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "3. still confused about integration by parts"
- **Judge's key context:** The calculus exam is tomorrow at 09:00 and the student is stuck on integration by parts; the next step should stay on calculus (that topic), not switch to the essay due next week.

## lab-in-5-hungry

- **Time:** 2026-10-05 12:55
- **Ended:** 25-min focus on "Read chapter 6 (organic chem)"
- **Calendar:** Chemistry lab 2026-10-05 13:00
- **Tasks:** t1 Read chapter 6 (organic chem) (due 2026-10-08T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "2/5 couldn't focus, hungry"
- **Judge's key context:** The chemistry lab starts at 13:00, in 5 minutes, and the student is hungry; no new study session fits - it is time to grab food if possible and head to the lab.

## free-afternoon-switch

- **Time:** 2026-10-05 14:00
- **Ended:** 25-min focus on "Sociology essay"
- **Calendar:** Dinner with friends 2026-10-05 18:30
- **Tasks:** t1 Sociology essay (due 2026-10-10T23:59, medium); t2 Stats homework 3 (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4, good progress on the essay" → "switch to the stats homework, 25 min"
- **Judge's key context:** The afternoon is free until 18:30; the stats homework is due sooner (Wednesday) than the essay.

## bus-in-10

- **Time:** 2026-10-05 16:35
- **Ended:** 25-min focus on "Problem set 2 (questions 1-5)"
- **Calendar:** Bus home 2026-10-05 16:45
- **Tasks:** t1 Problem set 2 (questions 1-5) (due 2026-10-08T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "5! finished question 3"
- **Judge's key context:** The bus home leaves at 16:45, in 10 minutes, so it is time to pack up rather than start another block; questions 4-5 are still left.

## lecture-in-10-break

- **Time:** 2026-10-05 09:50
- **Ended:** 25-min focus on "Review sorting algorithms notes"
- **Calendar:** Algorithms lecture 2026-10-05 10:00; Algorithms lab 2026-10-05 11:15
- **Tasks:** t1 Review sorting algorithms notes (due 2026-10-05T10:00, high)
- **Earlier sessions today:** 0
- **Student says:** "ok, 3/5" → "yeah break"
- **Judge's key context:** The algorithms lecture starts at 10:00, in 10 minutes.

## exhausted-after-50

- **Time:** 2026-10-05 15:10
- **Ended:** 50-min focus on "ML project: model training"
- **Calendar:** Gym 2026-10-05 19:00
- **Tasks:** t1 ML project: model training (due 2026-10-09T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4 but I'm exhausted honestly"
- **Judge's key context:** The student just did a 50-minute session and says they are exhausted; the suggestion should be a real rest (a long break of 15+ minutes, or stopping), not another block right away.

## in-the-zone

- **Time:** 2026-10-05 10:30
- **Ended:** 25-min focus on "Coding assignment 2"
- **Calendar:** Lunch with Sami 2026-10-05 12:30
- **Tasks:** t1 Coding assignment 2 (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "5/5 in the zone!"
- **Judge's key context:** The student is in flow with 2 hours free before lunch; continuing on the same task (possibly a longer block) should be offered, not forced into a break.

## phone-distraction

- **Time:** 2026-10-05 21:00
- **Ended:** 25-min focus on "Microeconomics reading ch. 3-4"
- **Calendar:** Microeconomics exam 2026-10-08 14:00
- **Tasks:** t1 Microeconomics reading ch. 3-4 (due 2026-10-08T14:00, high)
- **Earlier sessions today:** 0
- **Student says:** "2. kept checking my phone"
- **Judge's key context:** Focus was low because of phone distraction; a good reply suggests a concrete fix (e.g. phone in another room) without guilt-tripping.

## headache

- **Time:** 2026-10-05 17:00
- **Ended:** 25-min focus on "Organic chemistry flashcards"
- **Calendar:** empty
- **Tasks:** t1 Organic chemistry flashcards (due 2026-10-09T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "1/5 I have a headache"
- **Judge's key context:** The student has a headache; the priority is rest (water, a long break or stopping), not more studying.

## bored-reading

- **Time:** 2026-10-05 11:15
- **Ended:** 25-min focus on "Philosophy reading: Kant"
- **Calendar:** Seminar 2026-10-05 14:00
- **Tasks:** t1 Philosophy reading: Kant (due 2026-10-09T23:59, medium); t2 Linear algebra exercises 4.1-4.6 (due 2026-10-08T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "3, it's so boring"
- **Judge's key context:** The student is bored with the reading; switching to the linear algebra exercises (or changing technique) is a sensible option to offer.

## french-continue

- **Time:** 2026-10-05 11:00
- **Ended:** 25-min focus on "Exercices de probabilités 1-6"
- **Calendar:** Déjeuner 2026-10-05 13:00
- **Tasks:** t1 Exercices de probabilités 1-6 (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "c'était bien, 4/5, j'ai fini les exercices 1 à 3" → "on continue"
- **Judge's key context:** The student writes in French and wants to continue the same exercises (4-6 remain); free until 13:00.

## late-deadline-stress

- **Time:** 2026-10-05 22:40
- **Ended:** 25-min focus on "Physics lab report"
- **Calendar:** empty
- **Tasks:** t1 Physics lab report (due 2026-10-06T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "3/5 stressed, still have the conclusion to write"
- **Judge's key context:** It is 22:40 and the report is due tomorrow at 23:59; a realistic suggestion is at most one more short block or sleeping and finishing tomorrow - not an all-nighter.

## finished-lab-report

- **Time:** 2026-10-05 15:00
- **Ended:** 25-min focus on "Physics lab report"
- **Calendar:** empty
- **Tasks:** t1 Physics lab report (due 2026-10-06T23:59, high); t2 Stats homework 3 (due 2026-10-09T23:59, medium); t3 Optional reading: history of science (due -, low)
- **Earlier sessions today:** 0
- **Student says:** "5/5 finished the lab report!!"
- **Judge's key context:** The lab report is finished; the next priority by deadline is the stats homework (due Friday), not the optional reading.

## finished-essay-break

- **Time:** 2026-10-05 16:00
- **Ended:** 25-min focus on "History essay"
- **Calendar:** empty
- **Tasks:** t1 History essay (due 2026-10-06T23:59, high); t2 Spanish vocab list 5 (due 2026-10-08T23:59, low)
- **Earlier sessions today:** 0
- **Student says:** "done with the essay, 4" → "10 min break please"
- **Judge's key context:** The essay is finished; the student asked for a 10-minute break.

## almost-done-slides

- **Time:** 2026-10-05 13:30
- **Ended:** 25-min focus on "Presentation slides"
- **Calendar:** Presentation rehearsal 2026-10-05 17:00
- **Tasks:** t1 Presentation slides (due 2026-10-06T10:00, high)
- **Earlier sessions today:** 0
- **Student says:** "4, almost done with the slides, maybe 15 more min"
- **Judge's key context:** The slides are not finished yet (about 15 minutes left); a short block to finish them is the natural next step.

## french-finished-tp

- **Time:** 2026-10-05 15:45
- **Ended:** 25-min focus on "TP de chimie"
- **Calendar:** empty
- **Tasks:** t1 TP de chimie (due 2026-10-06T23:59, high); t2 Révision partiel d'analyse (due 2026-10-08T09:00, high)
- **Earlier sessions today:** 0
- **Student says:** "j'ai terminé le TP, 5/5"
- **Judge's key context:** The chemistry TP is done; the analysis exam revision (exam Thursday morning) is the next priority. The student writes in French.

## finished-last-task

- **Time:** 2026-10-05 18:10
- **Ended:** 25-min focus on "Problem set 4"
- **Calendar:** empty
- **Tasks:** t1 Problem set 4 (due 2026-10-07T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "finished the problem set, 4"
- **Judge's key context:** That was the only open task; with nothing else on the list Focus should suggest a break or wrapping up, or ask what else they have - not invent tasks.

## half-of-reading

- **Time:** 2026-10-05 10:00
- **Ended:** 25-min focus on "Read chapters 4 and 5"
- **Calendar:** Biology lecture 2026-10-05 12:00
- **Tasks:** t1 Read chapters 4 and 5 (due 2026-10-06T08:00, high)
- **Earlier sessions today:** 0
- **Student says:** "read chapter 4, 3/5"
- **Judge's key context:** Only chapter 4 is read; chapter 5 is still left, so the task is not done.

## explicit-another-25

- **Time:** 2026-10-05 10:00
- **Ended:** 25-min focus on "Thesis literature review"
- **Calendar:** Lunch 2026-10-05 13:00
- **Tasks:** t1 Thesis literature review (due 2026-10-16T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4, another 25 on the same please"
- **Judge's key context:** The student explicitly asked for another 25 minutes on the same task; Focus should just start it.

## explicit-15-break

- **Time:** 2026-10-05 15:30
- **Ended:** 25-min focus on "Accounting exercises"
- **Calendar:** empty
- **Tasks:** t1 Accounting exercises (due 2026-10-08T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "3/5, I need a 15 min break"
- **Judge's key context:** The student explicitly asked for a 15-minute break.

## explicit-essay-45

- **Time:** 2026-10-05 14:00
- **Ended:** 25-min focus on "Spanish grammar drills"
- **Calendar:** Volunteering 2026-10-05 17:30
- **Tasks:** t1 Spanish grammar drills (due 2026-10-09T23:59, low); t2 Political science essay (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "good. let's do the essay now for 45 min"
- **Judge's key context:** The student explicitly chose the essay for 45 minutes; there is time before 17:30.

## explicit-15-before-leaving

- **Time:** 2026-10-05 16:30
- **Ended:** 25-min focus on "Databases assignment"
- **Calendar:** Leave for work shift 2026-10-05 17:00
- **Tasks:** t1 Databases assignment (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "5, keep going but only 15 min, I have to leave at 5"
- **Judge's key context:** The student must leave at 17:00 and asked for exactly 15 more minutes.

## explicit-done-for-today

- **Time:** 2026-10-05 19:45
- **Ended:** 25-min focus on "Statistics project"
- **Calendar:** empty
- **Tasks:** t1 Statistics project (due 2026-10-09T23:59, high); t2 German vocabulary (due 2026-10-07T23:59, low)
- **Earlier sessions today:** 4
- **Student says:** "done for today, 4"
- **Judge's key context:** The student is stopping for the day; Focus should accept it (brief recap, maybe tomorrow's first task) and not push more work.

## french-break-10

- **Time:** 2026-10-05 10:20
- **Ended:** 25-min focus on "Fiche de révision d'histoire"
- **Calendar:** empty
- **Tasks:** t1 Fiche de révision d'histoire (due 2026-10-07T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "pause de 10 minutes stp, 3/5"
- **Judge's key context:** The student asked in French for a 10-minute break.

## explicit-25-conflicts-lecture

- **Time:** 2026-10-05 13:40
- **Ended:** 25-min focus on "Data structures homework"
- **Calendar:** Data Structures lecture 2026-10-05 14:00
- **Tasks:** t1 Data structures homework (due 2026-10-06T23:59, high)
- **Earlier sessions today:** 0
- **Student says:** "4, another 25 on this"
- **Judge's key context:** A 25-minute block would run into the 14:00 lecture (20 minutes away); Focus should point out the conflict and shorten the block or check with the student, not blindly start 25 minutes.

## fourth-session-long-break

- **Time:** 2026-10-05 11:20
- **Ended:** 25-min focus on "Operating systems revision"
- **Calendar:** empty
- **Tasks:** t1 Operating systems revision (due 2026-10-09T09:00, high)
- **Earlier sessions today:** 6
- **Student says:** "4/5"
- **Judge's key context:** This was the 4th focus session in a row with only short breaks; a long break (15-30 minutes) is due.

## fourth-session-fading-accept

- **Time:** 2026-10-05 16:20
- **Ended:** 25-min focus on "Econometrics problem set"
- **Calendar:** empty
- **Tasks:** t1 Econometrics problem set (due 2026-10-08T23:59, high)
- **Earlier sessions today:** 6
- **Student says:** "3, I'm fading" → "ok long break"
- **Judge's key context:** Fourth focus session in a row and the student is fading; a long break is due.

## second-session-short-break

- **Time:** 2026-10-05 09:55
- **Ended:** 25-min focus on "Japanese kanji practice"
- **Calendar:** empty
- **Tasks:** t1 Japanese kanji practice (due 2026-10-08T23:59, medium)
- **Earlier sessions today:** 2
- **Student says:** "4" → "break"
- **Judge's key context:** Only the second focus session of the day; a short break (about 5 minutes) fits.

## after-long-break-short-again

- **Time:** 2026-10-05 12:40
- **Ended:** 25-min focus on "Compilers project"
- **Calendar:** empty
- **Tasks:** t1 Compilers project (due 2026-10-10T23:59, high)
- **Earlier sessions today:** 9
- **Student says:** "4" → "short break pls"
- **Judge's key context:** A long break already happened two sessions ago, so a short break is right now.

## break-ended-ready

- **Time:** 2026-10-05 10:05
- **Ended:** 5-min break on "Short break"
- **Calendar:** Lunch 2026-10-05 12:30
- **Tasks:** t1 Physics lab report (due 2026-10-06T23:59, high); t2 Sociology reading (due 2026-10-12T23:59, low)
- **Earlier sessions today:** 1
- **Student says:** "yeah ready, let's do the lab report"
- **Judge's key context:** The break is over; the student was in the middle of the lab report, which is also the closest deadline, so resuming it is the natural proposal.

## break-ended-5-more

- **Time:** 2026-10-05 15:05
- **Ended:** 5-min break on "Short break"
- **Calendar:** empty
- **Tasks:** t1 Marketing case study (due 2026-10-08T23:59, medium)
- **Earlier sessions today:** 1
- **Student says:** "5 more min pls"
- **Judge's key context:** The student asked for 5 more minutes of break.

## break-ended-class-soon

- **Time:** 2026-10-05 13:50
- **Ended:** 5-min break on "Short break"
- **Calendar:** Statistics lecture 2026-10-05 14:00
- **Tasks:** t1 Stats homework 3 (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 1
- **Student says:** "ok what now"
- **Judge's key context:** The statistics lecture starts at 14:00, in 10 minutes; a 25-minute block does not fit - head to class or do a very short review.

## long-break-ended-evening

- **Time:** 2026-10-05 20:30
- **Ended:** 30-min break on "Dinner break"
- **Calendar:** Biochemistry exam 2026-10-08 09:00
- **Tasks:** t1 English essay (due 2026-10-12T23:59, medium); t2 Biochemistry revision (due 2026-10-08T09:00, high)
- **Earlier sessions today:** 1
- **Student says:** "ready, what should i do"
- **Judge's key context:** The biochemistry exam on Thursday is the closest deadline, so biochemistry revision should be the main proposal over the essay due next week.

## french-break-ended-ready

- **Time:** 2026-10-05 16:35
- **Ended:** 5-min break on "Petite pause"
- **Calendar:** empty
- **Tasks:** t1 Projet de programmation (due 2026-10-07T23:59, high)
- **Earlier sessions today:** 1
- **Student says:** "ok je suis prêt"
- **Judge's key context:** The student writes in French and is ready to resume the programming project.

## late-night-stop

- **Time:** 2026-10-05 23:30
- **Ended:** 25-min focus on "Literature essay"
- **Calendar:** Morning lecture 2026-10-06 08:30
- **Tasks:** t1 Literature essay (due 2026-10-09T23:59, medium)
- **Earlier sessions today:** 0
- **Student says:** "4, but it's late"
- **Judge's key context:** It is 23:30 with a lecture at 08:30 and the essay is not due until Friday; Focus should suggest stopping for the night.

## cramming-1am

- **Time:** 2026-10-06 01:10
- **Ended:** 25-min focus on "Genetics revision"
- **Calendar:** Genetics exam 2026-10-06 09:00
- **Tasks:** t1 Genetics revision (due 2026-10-06T09:00, high)
- **Earlier sessions today:** 0
- **Student says:** "3, one more?"
- **Judge's key context:** It is 01:10 and the exam is at 09:00; sleep should be prioritized over another session (at most a very short wrap-up).
