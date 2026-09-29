# Risk Register and Issue Log — SchoolDiary

Risks are things that might happen. Issues are problems that have already happened. This document keeps them apart: the register (§2) and RMMM plans (§3) are planned artefacts, while the issue log (§4) is **Simulated for the case study**.

## 1. Scoring method

Probability (P) and impact (I) each use a 1–5 scale: 1 = very low, 2 = low, 3 = medium, 4 = high, 5 = very high. Exposure = P × I (range 1–25). Risks are ranked by exposure, and ties are broken by the higher impact, then by breadth of affected users (how many parents or teachers the risk touches). R2 (delivery to all parents) ranks above R5, and R6 above R7. Impact considers the adoption target, privacy of children's data, schedule and the trust of parents and teachers. The scores are planning judgments, not measured probabilities.

Bands: exposure ≥ 15 high, 9–14 medium, ≤ 8 low.

### 1.1 Probability × impact matrix

Each cell lists the risk IDs with that probability and impact.

| Impact \ Probability | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| **I5** |  | R4 |  | R1 |  |
| **I4** |  |  | R2, R5 |  |  |
| **I3** |  | R8 | R6, R7 | R3 |  |
| **I2** |  |  |  |  |  |
| **I1** |  |  |  |  |  |

## 2. Risk register

| Rank | ID | Risk | P | I | Exposure | Response type | Response | Owner (role) |
|---:|---|---|---:|---:|---:|---|---|---|
| 1 | R1 | Low parent adoption (below the 90% monthly-active target) | 4 | 5 | 20 | Mitigate | Onboarding drive through class teachers and parent meetings, simple 3-tap flows, schools stop circulating the same notices on paper for pilot classes, weekly adoption tracking, SMS fallback (C-02) ready for parents without smartphones | Project manager with school management sponsor |
| 2 | R2 | Push delivery failure, or parents without smartphones or mobile data | 3 | 4 | 12 | Mitigate | Test on low-end Android 8 phones, idempotent retries, in-app inbox as a backup to push, battery-saver help text, delivery monitoring, SMS fallback C-02 planned | Developer 1 (technical lead) |
| 3 | R5 | Messaging rule too strict, so genuine urgent messages are delayed | 3 | 4 | 12 | Mitigate | Urgent path with principal approval, a defined 07:00 default, school office phone in the parent auto-reply, review of urgent requests after week 1 | Developer/QA with school principals |
| 4 | R3 | Teachers keep running WhatsApp groups (parallel channels) | 4 | 3 | 12 | Mitigate | Principal circular that official notices go through SchoolDiary, teacher training, the after-8 p.m. report shown to management, easier posting than WhatsApp | School principals |
| 5 | R4 | Privacy breach: a parent sees another child's data, or a phone number leaks | 2 | 5 | 10 | Avoid | Role and child scoping at the service layer, masked numbers, automated access tests (NFR-03), TLS and encryption at rest, no public URLs for attachments | Developer 1 (technical lead) |
| 6 | R6 | Roster and contact import errors | 3 | 3 | 9 | Transfer | Schools sign off their own rosters and contact lists before import. The admin panel gives per-row CSV errors and a dry-run import. | School admins |
| 7 | R7 | Schedule slip in Messaging (the largest work item, 12 pd) | 3 | 3 | 9 | Accept | Messaging (task E) has 6 days of total float, but only 1 day is free, because P3 does D next (D's LF is 18). If E slips by more than 1 day, P1 takes part of D on days 16–18 in place of test preparation. Progress is checked at each milestone, and the plan is re-baselined if float is used. | Project manager |
| 8 | R8 | Management disputes the definition of "active parent" | 2 | 3 | 6 | Avoid | Agree the definition (an active parent is a parent who opens at least one notice or message in the calendar month) in writing before the pilot and build the report to it | Project manager |

Highest exposure is R1 (20), the only high-band risk. R2, R5 and R3 are tied at 12; R3 (impact 3) ranks below R2 and R5 (impact 4), and R2 ranks above R5 by breadth of affected users. Scores must be revisited after the pilot.

## 3. RMMM plans for the top three

### R1 — Low parent adoption (exposure 20)

- **Mitigation:** run an onboarding drive at both pilot schools (QR code sheet in the paper diary, class teacher shows the app at the first parent meeting); keep flows to 3 taps (NFR-05); mirror every circular in the app so parents learn to look there; use a help desk at the school office for the first two weeks.
- **Monitoring:** the report of monthly active parents (FR-10), read weekly. **Trigger metric:** fewer than 80% of the 2,300 pilot parents active by the end of week 3 (that is below 1,840 parents), or the 24-hour notice read rate below 75%.
- **Management/contingency:** if the trigger fires, prioritise the SMS fallback (C-02) and send parents who have not logged in a reminder through the class teacher; assign a helper per class for parents who have not logged in; the steering group decides whether the rollout goes ahead.
- **Owner:** project manager with the school management sponsor.

### R2 — Push delivery failure or parents without smartphones or data (exposure 12)

- **Mitigation:** test on Android 8 phones with 2 GB RAM and with battery saver on; use an idempotent, retrying queue (NFR-02); keep an in-app inbox so a missed push still shows the notice; give help text for battery-saver settings.
- **Monitoring:** delivery within 5 minutes from gateway logs (NFR-01, target ≥ 99%). **Trigger metric:** delivery within 5 min below 99%, or more than 5% of pilot parents with no working push token.
- **Management/contingency:** raise a defect and fix with priority; contact affected parents through the class teacher; bring forward the SMS fallback (C-02) for parents without smartphones or data.
- **Owner:** Developer 1 (technical lead).

### R5 — Messaging rule too strict, delaying genuine urgent messages (exposure 12)

- **Mitigation:** the urgent route with principal approval; rejected or undecided requests go out at 07:00; the parent auto-reply gives the school office number for emergencies; cover the rule with BVA and decision-table tests (TC-BVA, TC-DT).
- **Monitoring:** number of urgent approval requests and time to a decision, plus teacher and parent complaints. **Trigger metric:** more than 2 complaints a week about a delayed genuine urgent message, or any urgent request waiting more than 30 minutes for a decision.
- **Management/contingency:** the principal appoints a deputy to answer approvals; the group revises the window or urgent criteria through change control; approved urgent messages stay reported separately from the zero target.
- **Owner:** Developer/QA with the school principals.

## 4. Issue log (Simulated for the case study)

Problems that have already occurred. Dates are project days (day 0 is the project start).

| ID | Date raised | Description | Impact | Action | Owner | Status | Related risk |
|---|---|---|---|---|---|---|---|
| I-01 | Day 25 | Contact numbers missing for 186 of 2,300 pilot parents (8.1%) at import | 186 parents could not receive alerts or be reached, which limits adoption | School offices collect the missing numbers, chased at the first parent meeting. The admin panel now lists rows with missing contacts. | School admins (with Developer 1 for the report) | Open | R6 (also affects R1) |
| I-02 | Day 23 | A teacher training slot clashed with exams at school 2 | Training for some school 2 teachers moved and reduced their preparation time before go-live | Session rescheduled after exams, short recorded guide sent to the teachers meanwhile | Project manager (trainer: Developer 2) | Closed | R1 |
| I-03 | Day 31 | Push notifications delayed on some low-end phones with battery saver on | Some parents saw notices late, which hurts trust and adoption | Battery-saver help text added to the app, affected phones logged, SMS fallback C-02 prioritised | Developer 1 (technical lead) | Open | R2 |

**Why issues and risks are kept separate.** A risk has a probability and is managed before it happens, with a response and a trigger, while an issue has already happened, so it has no probability and needs an owner, an action and a closing date. If both were in one list, exposure ranking would become meaningless, since a certain problem cannot be scored P × I, and current problems would push out the future risks that the team can still prevent. Keeping two lists also shows how a risk turns into an issue (R6 became I-01 and R2 became I-03) and lets management see how well the risk plan predicted what really happened. Issues are reviewed weekly, while risks are re-scored at each milestone.
