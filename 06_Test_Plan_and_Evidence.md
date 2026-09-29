# Test Plan and Evidence — SchoolDiary

This document is the IEEE 829-lite test plan for the SchoolDiary pilot, together with the test designs (equivalence classes, boundary value analysis, decision table) and the test evidence. The plan and test designs (§1–§5) are planned artefacts. The test log, defects and figures in §6 and §7 are **Simulated for the case study**. They are not results from a real deployment.

All times are IST at minute granularity (hh:mm). The rules under test come from the messaging-hours and approval rules of FR-08 (teacher sending window 07:00–19:59; parents may send at any time; school-level notices need school-admin approval).

## 1. Test plan (IEEE 829-lite)

**1.1 Identifier:** TP-SD-01

**1.2 Test items**

| Module | Requirements covered |
|---|---|
| Accounts and roles (auth/common) | FR-01; NFR-03, NFR-04 |
| Notices and read receipts | FR-02, FR-03 |
| Homework | FR-04 |
| Attendance alerts | FR-05 |
| Fee reminders | FR-06 |
| Messaging with time limits (messaging-hours rule) | FR-07, FR-08 |
| Admin panel | FR-09 |
| Records and reports | FR-10 |

**1.3 Features to be tested**
- Role scoping for parent, teacher, school admin and management (FR-01)
- Class-level and school-level notices, with school-admin approval before publishing (FR-02)
- Delivered/read receipts, read % and the unread list (FR-03)
- Homework per class and subject, due date and parent acknowledgement (FR-04)
- Absence alerts within 15 min of roll call (FR-05)
- Fee reminders at 7 days and 1 day before the due date, with no payment function (FR-06)
- Parent ↔ teacher thread per student (FR-07)
- The messaging-hours rule and principal-approval flow: BVA (§4) and decision table (§5)
- Bulk CSV import, teacher–class mapping and the approval queue (FR-09)
- Audit log search and the two management reports (FR-10)

**1.4 Features not tested**
- The Could items C-01 to C-03 and the Won't items (online payment, video calls, student logins, WhatsApp integration)
- Real push-gateway and mobile-operator behaviour beyond the load test (a gateway simulator stands in during system tests)
- iOS (not in the pilot)

**1.5 Approach**

| Level | Technique |
|---|---|
| Unit | Equivalence partitioning (§3), BVA on message time (§4), decision table (§5) for the rule engine |
| Integration | Notice service → approval queue → publisher → push gateway simulator; message service → time-rule engine → scheduler queue (success, failure, retry, duplicate job) |
| System | One case per FR (TC-01 to TC-10), end to end on the Android app and the web admin panel |
| UAT | Pilot users (teachers, school admins, parents) run the task scripts on synthetic data |

**1.6 Entry criteria**
- Feature freeze reached (milestone M2, day 18): all features built.
- The build is deployed to the test environment, with the synthetic roster of 2 schools loaded.
- The messaging-hours rules (§5 of the facts, restated in §5 here) are agreed as the test oracle.

**1.7 Exit criteria**
- 100% of planned cases executed.
- 0 open critical or high defects at test exit (M3, day 22, pilot go/no-go).
- DRE target ≥ 90%. The target is **confirmed after the 2-week pilot window**, not at test exit, because DRE needs the post-release defect count.

**1.8 Test environment:** synthetic parents, teachers and students only, no real personal data. An Android 8 phone with 2 GB RAM plus two newer handsets, the web admin panel in a desktop browser, and a push-gateway simulator with a controllable clock so that time-based rules can be tested at exact minutes.

**1.9 Schedule:** Task G (Testing, 12 person-days with 3 people = 4 days) is planned for **days 18–22**, after B, C, D and E finish (it is on the critical path A → B → G → H). Days 16–18 are used to prepare cases and data. Test exit and go/no-go is milestone M3 on day 22.

**1.10 Roles**

| Role | Responsibility |
|---|---|
| QA lead (Developer/QA, P3) | Owns this plan, confirms exit criteria, reports DRE and density |
| Testers (all three team members during G) | Design and execute cases, raise defects |
| Developers (P1, P2) | Fix defects, support unit and integration tests |
| Project manager | Tracks schedule and change requests |
| School admin (pilot schools) | Takes part in UAT of the admin panel and approval queue |
| Principal (pilot schools) | Takes part in UAT of urgent-message approval |
| Teachers and parents (pilot users) | Perform UAT |

**1.11 Deliverables:** this document, the executed test log (§6), the defect log, and the DRE and defect-density report (§7).

## 2. System test cases TC-01 to TC-10

One case per functional requirement, matching the traceability matrix in the SRS.

| ID | FR | Steps | Expected result |
|---|---|---|---|
| TC-01 | FR-01 | 1. Create one user for each role: parent, teacher, school admin, management. 2. Log in as each. 3. As the teacher of class 5A, open class 5B. 4. As a parent of child X, open the data of child Y. | Each role sees only its own scope (school / class / child). The 5B and child Y accesses are denied. |
| TC-02 | FR-02 | 1. As a class teacher, publish a class notice with a PDF attachment at 10:30. 2. As a teacher, submit a school-level notice. 3. Check that it is not visible to parents. 4. As school admin, approve it. | The class notice is published at once with its attachment. The school-level notice waits in the approval queue and is published only after approval. |
| TC-03 | FR-03 | 1. Publish a notice to a class of 10 test parents. 2. Open it as 6 of them. 3. As the sender, open the notice report. | Delivered and read are recorded per parent. Read % = 60% and the list shows the 4 unread parents. Receipts appear within 60 s of opening (NFR-02). |
| TC-04 | FR-04 | 1. Post homework for class 5A, subject Maths, with a due date. 2. As a parent, open it and press Acknowledge. | The homework shows class, subject and due date. The acknowledgement is stored against that parent and child. |
| TC-05 | FR-05 | 1. Mark student S absent at roll call (time t). 2. Record when the parent receives the alert. 3. Mark a present student. | The parent of S gets the alert within 15 min of t. No alert is sent for the present student. |
| TC-06 | FR-06 | 1. Load a fee due date of D from the school fee records. 2. Advance the test clock to D − 7 days and D − 1 day. 3. Look for any payment option in the app. | One reminder is sent at D − 7 days and one at D − 1 day. There is no payment function anywhere in the app. |
| TC-07 | FR-07 | 1. As a parent, open the thread for child X with the class teacher. 2. Send a message at 10:30. 3. The teacher replies at 10:40. | A single thread per student holds both messages. Both parties see them. Phone numbers are masked (NFR-04). |
| TC-08 | FR-08 | Execute TC-BVA-01 to TC-BVA-18 (§4) and TC-DT-R1 to TC-DT-R12 (§5). | Each result matches the expected outcome in those tables: allowed, queued for 07:00, approval requested, or hold with auto-reply. |
| TC-09 | FR-09 | 1. In the admin panel, bulk-import a CSV of 100 students with 1 bad row. 2. Map a teacher to two classes. 3. Open the approval queue. | 99 rows are imported and the bad row is reported with its line number. The mapping is saved and the teacher sees both classes. The queue lists pending school-level notices and urgent-message requests. |
| TC-10 | FR-10 | 1. Send a set of notices and messages. 2. Search the audit log by sender, date and keyword. 3. Run the monthly-active-parents report and the teacher after-8 p.m. report. | The log finds every item sent. The reports show monthly active parents against the 90% target and teacher messages after 20:00 (target 0), with approved urgent ones listed separately. |

## 3. Equivalence classes

**3.1 Message time (teacher sender, routine message)**

| Class | Range | Valid? | Expected result | Representative value |
|---|---|---|---|---:|
| EC-T1 | 07:00 ≤ t ≤ 19:59 | Yes | In window: sent now | 13:30 |
| EC-T2 | 00:00 ≤ t < 07:00 | Yes | Before the window: queued for 07:00 | 03:15 |
| EC-T3 | 20:00 ≤ t ≤ 23:59 | Yes | From 20:00: queued for the next school day 07:00 | 21:45 |
| EC-T4 | not a valid time (hour > 23, minute > 59, empty) | No | Rejected as invalid input, nothing sent or queued | 25:10 |

**3.2 Other inputs**

| Input | Classes | Representative values and expected handling |
|---|---|---|
| Sender role | Teacher; parent; admin | Teacher: window rules apply. Parent: no time restriction, but out-of-window messages are held with an auto-reply. Admin: sends school-level notices only. |
| Urgency (teacher, outside window) | Routine; urgent | Routine: queue for 07:00. Urgent: needs principal approval. |
| Approval state (urgent, outside window) | Pending; approved; rejected or no decision by 07:00 | Pending: request raised. Approved: sent immediately. Rejected or 07:00 reached: sent at 07:00. |
| Notice scope | Class-level; school-level | Class-level by the class teacher: publish now if in window, otherwise queue. School-level: always to school-admin approval. |

| Case | Combination | Expected | Covered by |
|---|---|---|---|
| TC-EC-01 | Teacher, routine, 13:30 | Send now | TC-DT-R1 |
| TC-EC-02 | Teacher, routine, 03:15 | Queue for 07:00 | TC-DT-R2 |
| TC-EC-03 | Teacher, routine, 21:45 | Queue for next-day 07:00 | TC-DT-R2 |
| TC-EC-04 | Teacher, routine, 25:10 | Rejected as invalid time | input validation |
| TC-EC-05 | Parent, 13:30 | Delivered to the teacher | TC-DT-R6 |
| TC-EC-06 | Parent, 21:45 | Auto-reply, held until 07:00 | TC-DT-R7 |
| TC-EC-07 | Teacher, urgent, 21:45, approval pending | Request approval | TC-DT-R3 |
| TC-EC-08 | Teacher, urgent, 21:45, approved | Send now | TC-DT-R4 |
| TC-EC-09 | Teacher, urgent, 21:45, rejected | Sent at 07:00 | TC-DT-R5 |
| TC-EC-10 | Class notice at 10:30 / at 21:45 | Publish now / queue | TC-DT-R8, R9 |
| TC-EC-11 | School-level notice by a teacher | Send to admin approval | TC-DT-R10 |

## 4. Boundary value analysis around 8 p.m. and 07:00

Boundaries: 07:00 (start) and 19:59 (last minute) of the window, plus the midnight rollover. Two boundary values for each edge (one each side) and the neighbours are tested, for a routine teacher message and for a parent message. Expected queue time for out-of-window teacher messages: the next school day 07:00.

| ID | Sender | Time | Expected outcome |
|---|---|---|---|
| TC-BVA-01 | Teacher (routine) | 06:59 | Blocked and queued for 07:00. Teacher sees "Queued for 07:00". |
| TC-BVA-02 | Teacher (routine) | 07:00 | Allowed, sent now |
| TC-BVA-03 | Teacher (routine) | 07:01 | Allowed, sent now |
| TC-BVA-04 | Teacher (routine) | 19:58 | Allowed, sent now |
| TC-BVA-05 | Teacher (routine) | 19:59 | Allowed, sent now |
| TC-BVA-06 | Teacher (routine) | 20:00 | Queued for next-day 07:00 |
| TC-BVA-07 | Teacher (routine) | 20:01 | Queued for next-day 07:00 |
| TC-BVA-08 | Teacher (routine) | 23:59 | Queued for next-day 07:00 (day D + 1) |
| TC-BVA-09 | Teacher (routine) | 00:00 (across midnight, day D + 1) | Queued for the same 07:00 of day D + 1. Exactly one queue entry, no duplicate against TC-BVA-08. |
| TC-BVA-10 | Parent | 06:59 | Held and shown to the teacher at 07:00. Parent gets the instant auto-reply. |
| TC-BVA-11 | Parent | 07:00 | Allowed, delivered to the teacher at once, no auto-reply |
| TC-BVA-12 | Parent | 07:01 | Allowed, delivered to the teacher at once |
| TC-BVA-13 | Parent | 19:58 | Allowed, delivered to the teacher at once |
| TC-BVA-14 | Parent | 19:59 | Allowed, delivered to the teacher at once |
| TC-BVA-15 | Parent | 20:00 | Held until 07:00 next day. Auto-reply sent instantly. |
| TC-BVA-16 | Parent | 20:01 | Held until 07:00 next day. Auto-reply sent instantly. |
| TC-BVA-17 | Parent | 23:59 | Held until 07:00 of day D + 1. Auto-reply sent instantly. |
| TC-BVA-18 | Parent | 00:00 (day D + 1) | Held until the same 07:00 of day D + 1, once only. Auto-reply sent instantly. |

The auto-reply text is: "Teachers reply between 07:00 and 20:00. For emergencies call the school office." The queue for a Friday-night or pre-holiday message is scheduled for 07:00 on the next school day.

TC-BVA-08 and TC-BVA-09 together check the midnight rollover: both must resolve to the same single 07:00 delivery. A defect on exactly this case escaped to the pilot (DEF-35, §6).

## 5. Decision table for messaging-hours and approval rules

**Conditions**
- C1 Sender role: T = teacher, P = parent, A = school admin
- C2 Inside window (07:00–19:59)
- C3 Urgent (teacher message outside the window)
- C4 Principal approved
- C5 Notice scope: Cl = class-level notice, Sc = school-level notice, – = an ordinary message (not a notice)
- C6 Decision final (rejected, or 07:00 reached with no decision). This helper condition separates a pending request (R3) from a closed one (R5).

**Actions**
- A1 Send now
- A2 Queue for 07:00
- A3 Request approval (from the principal)
- A4 Auto-reply to parent and hold
- A5 Publish now
- A6 Send to admin approval

| Rule | C1 Role | C2 In window | C3 Urgent | C4 Principal approved | C5 Scope | C6 Decision final | Action |
|---|---|---|---|---|---|---|---|
| R1 | T | Y | – | – | – | – | A1 Send now |
| R2 | T | N | N | – | – | – | A2 Queue for 07:00 |
| R3 | T | N | Y | N | – | N | A3 Request approval |
| R4 | T | N | Y | Y | – | – | A1 Send now (immediately) |
| R5 | T | N | Y | N | – | Y | A2 Queue for 07:00 (sent at 07:00) |
| R6 | P | Y | – | – | – | – | A1 Send now (delivered to the teacher) |
| R7 | P | N | – | – | – | – | A4 Auto-reply and hold until 07:00 |
| R8 | T | Y | – | – | Cl | – | A5 Publish now |
| R9 | T | N | – | – | Cl | – | A2 Queue for 07:00 |
| R10 | T | – | – | – | Sc | – | A6 Send to admin approval |
| R11 | A | Y | – | – | Sc | – | A5 Publish now |
| R12 | A | N | – | – | Sc | – | A2 Queue for 07:00 |

Notes on the table:
- Once an admin approves a teacher's school-level notice (R10), the window check applies in the same way as R11 and R12: published now inside the window, otherwise queued for 07:00. This is an assumption made so that a school-level notice cannot bypass the sending window.
- An urgent flag on a notice is not defined in the rules, so urgency is "–" for notices.

**Test cases from the table**

| ID | Rule | Input | Expected |
|---|---|---|---|
| TC-DT-R1 | R1 | Teacher sends a routine message at 10:30 | Sent now |
| TC-DT-R2 | R2 | Teacher sends a routine message at 21:15 | Queued for next-day 07:00. Teacher sees "Queued for 07:00". |
| TC-DT-R3 | R3 | Teacher sends an urgent message at 21:15 with no decision yet | Approval request goes to the principal. Nothing is delivered yet. |
| TC-DT-R4 | R4 | Same as R3, the principal approves at 21:20 | Sent immediately at 21:20. Counted in the separate urgent-approved report. |
| TC-DT-R5 | R5 | Same as R3, the principal rejects (or no decision by 07:00) | Sent at 07:00. The 21:20 delivery must not happen. |
| TC-DT-R6 | R6 | Parent messages at 10:30 | Delivered to the teacher at once |
| TC-DT-R7 | R7 | Parent messages at 22:05 | Instant auto-reply. Message held and shown to the teacher at 07:00. |
| TC-DT-R8 | R8 | Class teacher posts a class notice at 10:30 | Published now |
| TC-DT-R9 | R9 | Class teacher posts a class notice at 21:15 | Queued for next-day 07:00 |
| TC-DT-R10 | R10 | Teacher submits a school-level notice at 10:30 | Goes to school-admin approval. Not visible to parents. |
| TC-DT-R11 | R11 | School admin posts a school-level notice at 10:30 | Published now |
| TC-DT-R12 | R12 | School admin posts a school-level notice at 21:15 | Queued for next-day 07:00 |

**Completeness note.** The three roles are covered for both values of C2. For the teacher outside the window, both urgent values are covered (R2 for routine, R3–R5 for urgent), and for urgent messages the approval outcomes are pending (R3), approved (R4) and rejected or no decision by 07:00 (R5). Inside the window an urgent flag has no effect, so it is collapsed into R1. The parent has no urgency or approval condition, so two rules (R6, R7) cover the role. For notices, class-level and school-level scope are each covered, for a teacher in and out of the window (R8, R9, R10) and for an admin (R11, R12). The remaining combinations are impossible or out of the rules: a parent sending a notice, an admin sending a class-level notice, and admin direct messages, none of which the requirements allow. The rules are mutually exclusive and consistent with the messaging-hours rules of FR-08. Invalid times are rejected before the table is used (EC-T4).

## 6. Test log (Simulated for the case study)

### 6.1 Execution summary by level

| Level | Cases run | Failed = defects | Passed | Pass rate |
|---|---:|---:|---:|---:|
| Unit | 90 | 11 | 79 | 87.8% |
| Integration | 30 | 7 | 23 | 76.7% |
| System | 40 | 6 | 34 | 85.0% |
| UAT | 15 | 3 | 12 | 80.0% |
| **Total** | **175** | **27** | **148** | **84.6%** |

Each failed case is counted as one defect. The 40 system cases include TC-01 to TC-10 plus the BVA, EC and decision-table cases of §3–§5.

### 6.2 Defects by phase

| Phase | Defects | IDs |
|---|---:|---|
| Requirements review | 4 | DEF-01 to DEF-04 |
| Design review | 3 | DEF-05 to DEF-07 |
| Unit test | 11 | DEF-08 to DEF-18 |
| Integration test | 7 | DEF-19 to DEF-25 |
| System test | 6 | DEF-26 to DEF-31 |
| UAT | 3 | DEF-32 to DEF-34 |
| **Pre-release subtotal** | **34** | 4 + 3 + 11 + 7 + 6 + 3 |
| Post-release (first 2 pilot weeks) | 2 | DEF-35, DEF-36 |
| **Total** | **36** | |

### 6.3 Defects by severity

| Phase | Critical | High | Medium | Low | Total |
|---|---:|---:|---:|---:|---:|
| Requirements review | 0 | 1 | 2 | 1 | 4 |
| Design review | 0 | 1 | 1 | 1 | 3 |
| Unit | 0 | 1 | 5 | 5 | 11 |
| Integration | 1 | 2 | 3 | 1 | 7 |
| System | 0 | 1 | 3 | 2 | 6 |
| UAT | 0 | 0 | 1 | 2 | 3 |
| Post-release | 0 | 1 | 1 | 0 | 2 |
| **Total** | **1** | **7** | **16** | **12** | **36** |

### 6.4 Ten representative defects

| ID | Phase | Severity | Module | Description | Found by | Status |
|---|---|---|---|---|---|---|
| DEF-02 | Requirements review | High | Messaging | The rule for urgent messages did not say what happens when the principal gives no decision. Clarified: sent at 07:00. | Review | Fixed (spec) |
| DEF-06 | Design review | Medium | Notices | Read-receipt record had no unique key per parent per notice, allowing double counts. | Review | Fixed |
| DEF-11 | Unit | Low | Messaging | Auto-reply text missing the final full stop. | Unit test | Fixed |
| DEF-15 | Unit | High | Messaging | The window check used `< 20:00` on minutes as text, so 19:59 was treated as outside the window. Caught by TC-BVA-05. | Unit test (BVA) | Fixed |
| DEF-21 | Integration | Critical | Admin | The teacher–class mapping was not applied to the message service, so a teacher could open another class's thread. | Integration test | Fixed |
| DEF-24 | Integration | Medium | Attendance | The absence alert was queued twice when roll call was re-saved, creating a duplicate push. | Integration test | Fixed |
| DEF-28 | System | High | Messaging | An urgent message rejected by the principal was still sent immediately at 21:20 as if approved (R5); it should wait until 07:00. Caught by TC-DT-R5. | System test | Fixed |
| DEF-30 | System | Medium | Fee reminders | The 1-day reminder was skipped when the due date fell on a Monday. | System test | Fixed |
| DEF-33 | UAT | Low | Homework | The Acknowledge button label was unclear to a parent. Renamed "Seen". | UAT | Fixed |
| DEF-35 | Post-release | High | Messaging | An after-hours message was queued twice on midnight rollover. A teacher message sent at 23:59 produced a second queue entry at 00:00, so it was delivered twice at 07:00. | Pilot (week 1) | Fixed, patch released |

DEF-36 (post-release, medium) was a display error in the read-percentage figure on a very large notice and is not listed above.

### 6.5 Module size and defect density (assumed KLOC)

| Module | KLOC | Defects | Density (defects/KLOC) |
|---|---:|---:|---:|
| Notices | 1.2 | 5 | 4.17 |
| Homework | 1.4 | 5 | 3.57 |
| Attendance | 0.9 | 4 | 4.44 |
| Fee reminders | 0.8 | 3 | 3.75 |
| Messaging | 2.2 | 12 | 5.45 |
| Admin | 2.5 | 7 | 2.80 |
| **Total** | **9.0** | **36** | **4.0** |

The module sizes are assumptions made for the case study. The 36 defects are counted against the modules in which the fault was found, including review defects.

## 7. Calculations

**7.1 Defect removal efficiency (DRE)**

DRE = E ÷ (E + D), where E = defects found before release and D = defects found after release.

- E = 4 (requirements review) + 3 (design review) + 11 (unit) + 7 (integration) + 6 (system) + 3 (UAT) = 34
- D = 2 (first 2 pilot weeks)
- DRE = 34 ÷ (34 + 2) = 34 ÷ 36 = 0.9444 = **94.4%**

The target of ≥ 90% is met, and it is confirmed only after the 2-week pilot window, when D is known.

**7.2 Test-phase DRE**

This counts only defects found by the four test levels, so it excludes the review defects.

- Test-phase defects found = 11 + 7 + 6 + 3 = 27
- Test-phase DRE = 27 ÷ (27 + 2) = 27 ÷ 29 = 0.9310 = **93.1%**

**7.3 Overall defect density**

Defect density = total defects ÷ size in KLOC.

- Size = 1.2 + 1.4 + 0.9 + 0.8 + 2.2 + 2.5 = 9.0 KLOC
- Density = 36 ÷ 9.0 = **4.0 defects/KLOC**

**7.4 Density per module**

| Module | Substitution | Density |
|---|---|---:|
| Notices | 5 ÷ 1.2 | 4.17 |
| Homework | 5 ÷ 1.4 | 3.57 |
| Attendance | 4 ÷ 0.9 | 4.44 |
| Fee reminders | 3 ÷ 0.8 | 3.75 |
| Messaging | 12 ÷ 2.2 | 5.45 |
| Admin | 7 ÷ 2.5 | 2.80 |

**Interpretation.** Messaging is the densest module at 5.45 defects/KLOC, about 36% above the overall 4.0 (5.45 ÷ 4.0 = 1.36). It holds 12 of the 36 defects (one third) in about a quarter of the code (2.2 of 9.0 KLOC). This fits the risk register: the time rules, queueing and approval flow of Messaging (R5 and R7) were the hardest part to get right. It also includes the one post-release high defect, so extra testing for the 10-school rollout should go to Messaging first, especially time-dependent cases such as the midnight rollover. Admin has the lowest density (2.80) as it is largely standard CRUD screens. A 94.4% DRE means about 1 defect in 18 escaped, and both escapes were in the first 2 weeks. Density and DRE are simulated figures, so they show the method and not measured quality.
