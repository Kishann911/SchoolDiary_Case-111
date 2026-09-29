# Software Requirements Specification: SchoolDiary

**Case:** 111 · **Student:** Kishan Ojha · **Style:** IEEE 830-style student SRS · **Version:** 1.1 · **Date:** 2026-09-29  
**System boundary:** notices, homework, attendance alerts, fee reminders and two-way parent–teacher messaging within school hours, for a group of 12 schools (pilot: 2 schools).

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-27 | Initial SRS: FR-01 to FR-10, NFR-01 to NFR-06 |
| 1.1 | 2026-09-29 | Added messaging-hours rules (section 3.5), traceability matrix, MoSCoW and Could backlog, elicitation appendix (simulated) |

---

## 1 Introduction

### 1.1 Purpose

This SRS specifies SchoolDiary for developers, testers, school admins, teachers, the principal and the group management who approve it. It is the baseline for the UML design, the project plan, the test plan and the pilot.

### 1.2 Scope

A group of 12 schools reaches parents through paper diaries, circulars and dozens of teacher-run WhatsApp groups. Parents miss notices, teachers receive messages late at night, and management has no record of what was communicated. SchoolDiary is an Android app for parents and teachers plus a web admin panel. It carries notices, homework, attendance alerts, fee reminders and two-way messages, and it enforces messaging hours.

Project data used in this SRS:

- 14,000 parents and 650 teachers across 12 schools.
- Pilot at 2 schools with 2,300 parents, which is 2,300 ÷ 14,000 = 16.4% of all parents (about 107 teachers, assuming proportionality).
- Targets: 90% of parents active monthly (pilot: 0.9 × 2,300 = 2,070 parents; full rollout: 12,600), and teacher messages after 8 p.m. reduced to zero.

Out of scope for this release: online fee payment, video calls, student logins and WhatsApp integration (section 3.7).

### 1.3 Definitions and acronyms

| Term | Meaning |
|---|---|
| IST | Indian Standard Time (UTC+05:30); all times in this SRS are IST at hh:mm granularity |
| Sending window | 07:00–19:59 inclusive, when teachers may send messages |
| Routine message | A teacher message with no urgency flag |
| Urgent message | A teacher message flagged urgent; outside the window it needs principal approval |
| Queued | Held by the system and auto-scheduled for 07:00 the next school day |
| Read receipt | Per-parent record of delivered and read for a notice |
| School admin | School-level administrator who approves school-level notices and manages rosters |
| Management | Group-level staff who view reports across schools |
| Push gateway | External service (for example FCM) that delivers push notifications to Android devices |
| MoSCoW | Must, Should, Could, Won't priority classes |
| FR / NFR | Functional / non-functional requirement |
| BVA, EP, DT | Boundary value analysis, equivalence partitioning, decision table |
| TLS, AES | Transport Layer Security; Advanced Encryption Standard |
| CSV | Comma-separated values file used for bulk import |

### 1.4 References

1. Case 111 brief, SchoolDiary (source of all population, effort and target figures).
2. IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*.
3. `02_UML_Design.md`: diagrams that realise these requirements.
4. `06_Test_Plan_and_Evidence.md`: test cases named in section 4.
5. `07_Risk_Register_and_Issue_Log.md`: risks referred to in this SRS (R1 to R8).

### 1.5 Overview

Section 2 describes the product, functions, users, constraints and assumptions. Section 3 gives the interfaces, 10 functional requirements, 6 non-functional requirements, the messaging-hours rules, and MoSCoW priorities. Section 4 is the traceability matrix. Appendix A records how the requirements were elicited (simulated).

---

## 2 Overall description

### 2.1 Product perspective

SchoolDiary replaces three channels used today: the paper diary that children carry, printed circulars, and WhatsApp groups run by individual teachers. Those channels have no delivery proof, no time limits and no central record. SchoolDiary is a new self-contained system with a central server, an Android app (parents and teachers) and a web admin panel. It depends on two external items: a push gateway for notifications and school rosters and fee records supplied by each school. It does not process payments.

### 2.2 Product functions (summary)

- Manage accounts and roles scoped to school, class and child (FR-01).
- Publish class-level and school-level notices with attachments and an approval step (FR-02), and track delivery and read status (FR-03).
- Post and acknowledge homework (FR-04).
- Alert parents of absences within 15 minutes of roll call (FR-05).
- Send fee reminders at 7 days and 1 day before the due date (FR-06).
- Provide parent ↔ teacher threads (FR-07) governed by messaging hours (FR-08).
- Administer schools, classes, rosters and approvals (FR-09).
- Keep a searchable communication record and management reports (FR-10).

### 2.3 User classes and personas

| User class | Need | Access boundary |
|---|---|---|
| Parent | Receive notices, homework, alerts and reminders; message the teacher | Only their own child's data (NFR-03) |
| Teacher | Post notices and homework, mark attendance, message parents without late-night pressure | Only mapped classes |
| School admin | Approve school-level notices, manage rosters and mappings | Own school |
| Management | View group-wide reports and the audit log | Read-only across schools |
| Principal | Approve urgent out-of-window teacher messages | Own school |

**Personas** (Simulated for the case study):

- **Meena Kulkarni, parent, 34.** Works shifts as a nurse; has one child in Class 4 and an Android phone with 2 GB RAM. Wants to see a notice once and know that the teacher saw her reply. Reads Hindi and English at a basic level.
- **Rahul Deshmukh, Class 7 teacher, 41.** Teaches 40 students and runs three WhatsApp groups that ping him until 11 p.m. Wants a clear stop time and a queue, not more messages.
- **Sunita Rao, school admin, 48.** Runs the school office and the paper circular register. Needs a bulk CSV import and one screen to approve school notices.
- **Dr. Anil Menon, group management, 55.** Cannot currently prove what was communicated to parents. Wants a monthly active-parent figure and an after-8 p.m. report he can trust.

### 2.4 Constraints

- **School hours and messaging window:** teachers send between 07:00 and 19:59 IST (section 3.5). Service availability is measured 06:30–21:00 IST (NFR-06).
- **Time zone:** all schedules, queues and reports use IST, with minute granularity.
- **Platforms:** Android 8+ phones with 2 GB RAM, and a web admin panel. There is no iOS app in the pilot.
- **No payment:** fee reminders are read-only reminders from the school's fee records; no payment is taken in the app.
- **Language:** English UI in the pilot.
- **Data protection:** parent, child and teacher data are personal data (NFR-03, NFR-04).
- **Team and budget:** a team of 3 with 68 person-days of bottom-up effort (see `04_Estimation_Sheet.md`).

### 2.5 Assumptions and dependencies

1. **Push gateway.** A third-party push gateway (for example FCM) is available and returns an "accepted" status per message. NFR-01 timing is measured to the point of push acceptance; handset delay after that is outside SchoolDiary's control (see risk R2, issue I-03).
2. **School rosters.** Each school supplies class rosters, student–parent links, parent contact details and fee due dates in CSV. Data quality is the school's responsibility; import errors are reported row by row (risk R6).
3. **Attendance source.** Class teachers mark attendance in SchoolDiary at roll call; "roll call" time is the time the register is submitted.
4. Parents have a smartphone and mobile data. Those without are out of scope until the SMS fallback (C-02).
5. The principal or a named deputy is reachable to decide urgent messages. If there is no decision by 07:00, the message is sent at 07:00.
6. Pilot teacher count (about 107) is proportional to the parent share (650 × 16.4%).

---

## 3 Specific requirements

### 3.1 External interfaces

- **User interfaces:** Android app (parent and teacher home screens, notice list, homework list, message threads, queue status "Queued for 07:00"); browser-based admin panel (rosters, mappings, approval queue, reports).
- **Push gateway interface:** the server sends each notification with an idempotency key and receives an accepted or rejected status; all traffic uses TLS 1.2+.
- **Roster and fee import interface:** CSV upload in the admin panel, validated row by row, with an error report.
- **Data concepts:** School, Class, Student, ParentAccount, TeacherAccount, Notice, ReadReceipt, Homework, AttendanceRecord, FeeReminder, MessageThread, Message, ApprovalRequest, AuditEntry. These are logical concepts, not a mandated schema.
- **Reports:** each rate shows its definition, numerator and denominator.

### 3.2 Functional requirements

Priority uses MoSCoW: **M** Must, **S** Should. Every requirement has an acceptance check that a tester can run.

| ID | Requirement | MoSCoW | Acceptance check |
|---|---|---|---|
| FR-01 | Accounts and roles: parent, teacher, school admin, management, each scoped to school / class / child | M | Create one account per role with a scope; each can open only screens and records inside its scope; an out-of-scope request returns "access denied" (TC-01) |
| FR-02 | Notices: publish class-level or school-level notices with attachments. School-level notices need school-admin approval before publishing | M | A class notice with a PDF attachment is visible to that class's parents; a school-level notice stays "Pending" and is invisible to parents until the school admin approves it (TC-02) |
| FR-03 | Read receipts: record delivered/read per parent for every notice. The sender sees read % and the unread list | M | For a notice to 30 parents where 12 open it, the sender sees 40% read and a list of the 18 unread parents by name (TC-03) |
| FR-04 | Homework: post homework per class and subject with a due date. Parents view and acknowledge it | S | A homework item for Class 5 Maths with a due date appears for the class's parents; after a parent taps Acknowledge, the teacher sees that parent as acknowledged (TC-04) |
| FR-05 | Attendance alerts: when a student is marked absent, their parent is notified within 15 min of roll call | M | Mark a student absent at 09:00 roll call; the parent's device receives the alert by 09:15 (TC-05) |
| FR-06 | Fee reminders: reminders at 7 days and 1 day before each due date, from the school's fee records. **No payment in the app** | S | For a due date of D, reminders are generated at D−7 and D−1 only; the reminder screen has no pay button or payment link (TC-06) |
| FR-07 | Two-way messaging: a parent ↔ class/subject teacher thread per student | M | A parent sends a message about their child to the class teacher; the teacher replies inside the window; both see one thread for that student (TC-07) |
| FR-08 | Messaging-hours rule (see section 3.5) | M | Every case in the BVA table and decision table of section 3.5 gives the stated outcome (TC-08, TC-BVA-*, TC-DT-*) |
| FR-09 | Admin panel: schools, classes, rosters, teacher–class mapping, bulk CSV import, approval queue | M | Import a CSV of 100 students with 3 invalid rows: 97 load, 3 appear in an error report; map a teacher to a class and approve a pending school notice from the queue (TC-09) |
| FR-10 | Communication record and management reports: a searchable audit log of all notices and messages. Monthly-active-parents report (target 90%), and a teacher after-8 p.m. messages report (target 0) | S | Search the log by date, sender and text and find a known notice; the two reports show numerator, denominator and percentage for a seeded month (TC-10) |

### 3.3 Non-functional requirements

Each NFR has a number and a "Measured by" entry.

| ID | Category | Requirement | Measured by |
|---|---|---|---|
| NFR-01 | Delivery reliability: timeliness | At least 99% of notices, homework and attendance alerts reach the device (push accepted) within 5 min of publishing; attendance alerts within 15 min of roll call | Load test with 10,000 synthetic messages, and push gateway logs |
| NFR-02 | Delivery reliability: integrity | 0 duplicate or lost messages in a 10,000-message retry test (idempotency keys). Read receipts are recorded within 60 s of opening | Test harness (retry test and receipt timing) |
| NFR-03 | Privacy: access control | 100% of authorisation tests pass. A parent sees only their own child's data; teachers see only their mapped classes | Automated access tests |
| NFR-04 | Privacy: data protection | TLS 1.2+ on 100% of connections, and AES-256 encryption at rest for personal data. Phone numbers are never shown between parents and teachers (masked in-app). Data is deleted within 12 months after a student leaves | Configuration review and an audit |
| NFR-05 | Usability | In a session with 20 pilot parents, at least 90% read a notice and reply to a teacher without help, in at most 3 taps from the home screen. The app runs on Android 8+ phones with 2 GB RAM. Text is at Class-5 reading level | Usability test with 20 pilot parents |
| NFR-06 | Availability | At least 99.5% monthly availability during 06:30–21:00 IST | Synthetic uptime checks |

### 3.4 Business targets (not requirements)

These are outcome targets from the brief, monitored through FR-10: 90% of parents active monthly (pilot 2,070 of 2,300), and teacher messages delivered after 20:00 equal to 0. They depend on adoption and are tracked as risks R1 and R3, so they are not written as NFRs.

### 3.5 Messaging-hours and approval rules (basis of FR-08)

**Rule set.** Times are IST at hh:mm granularity.

1. **Teacher sending window: 07:00–19:59 inclusive.** A teacher message inside the window is sent at once.
2. **Routine teacher message outside the window (20:00–06:59)** is not sent. It is queued and auto-scheduled for 07:00 the next school day. The teacher sees "Queued for 07:00".
3. **Urgent teacher message outside the window** needs principal approval. Approved: sent immediately. Rejected, or no decision by 07:00: sent at 07:00.
4. **Parents may send at any time.** A parent message received outside the window is held and shown to the teacher at 07:00. The parent gets an instant auto-reply: "Teachers reply between 07:00 and 20:00. For emergencies call the school office."
5. **Notice approval.** A class-level notice by the class teacher publishes immediately if inside the window; outside it, it is queued like a routine message. A school-level notice always needs school-admin approval.
6. **Target.** Teacher messages delivered after 20:00 = 0. The only exceptions are urgent messages with principal approval, which are reported separately.

**Boundary values for the message time** (test ids TC-BVA-01 to TC-BVA-09):

| Send time | Expected outcome |
|---|---|
| 06:59 | Blocked; queued for 07:00 |
| 07:00 | Allowed; sent |
| 07:01 | Allowed; sent |
| 19:58 | Allowed; sent |
| 19:59 | Allowed; sent |
| 20:00 | Queued for 07:00 next school day |
| 20:01 | Queued for 07:00 next school day |
| 23:59 | Queued; scheduled for the next-day 07:00 |
| 00:00 (next calendar day) | Queued; scheduled for the same next-day 07:00 (no double queueing across midnight) |

**Equivalence classes** (TC-EP-*): valid inside-window (07:00–19:59), invalid before window (00:00–06:59), invalid after window (20:00–23:59); sender class (teacher, parent); message class (routine, urgent).

**Decision table** (TC-DT-01 to TC-DT-*; Y = yes, N = no):

| Condition / action | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|
| Sender is a teacher | Y | Y | Y | Y | Y | N (parent) | N (parent) |
| Time inside 07:00–19:59 | Y | N | N | N | N | Y | N |
| Urgent flag | – | N | Y | Y | Y | – | – |
| Principal decision | – | – | Approved | Rejected | None by 07:00 | – | – |
| **Send now** | X | | X | | | X | |
| **Queue for 07:00** | | X | | X | X | | |
| **Hold for teacher at 07:00 and auto-reply** | | | | | | | X |

Notice approval decision table (TC-DT-*, continued):

| Condition / action | N1 | N2 | N3 | N4 |
|---|---|---|---|---|
| Level: school (Y) or class (N) | N | N | Y | Y |
| Time inside window | Y | N | Y | Y |
| Admin decision | – | – | Approved | Rejected or none |
| **Publish now** | X | | X | |
| **Queue for 07:00** | | X | | |
| **Not published (returned to sender)** | | | | X |

Where a school-level notice is approved outside the window, it follows rule 2 and is queued.

### 3.6 MoSCoW priorities

| Class | Items |
|---|---|
| **Must** | FR-01, FR-02, FR-03, FR-05, FR-07, FR-08, FR-09 |
| **Should** | FR-04, FR-06, FR-10 |
| **Could** (backlog) | C-01 Multilingual UI and messages (English / Hindi / Marathi); C-02 SMS fallback for parents without smartphones; C-03 Parent–teacher meeting slot booking |
| **Won't (this release)** | Online fee payment, video calls, student logins, WhatsApp integration |

Justification: the Musts are what the brief cannot do without: role-scoped access, notices with proof of reading, absence alerts, two-way messages, the time limits that teachers asked for, and the admin panel that loads the data. Should items add value but the pilot works without them for a short time (homework can be posted as a notice; fee reminders can be sent by school office; the log is needed by the pilot review). C-02 is likely to move up if adoption stays below target (risk R1).

### 3.7 Out of scope

Online fee payment (no payment risk and no payment-provider dependency), video calls, student logins (children have no accounts; privacy), and WhatsApp integration (SchoolDiary replaces those groups).

---

## 4 Traceability matrix

Every FR maps to one system test case (TC-01 to TC-10), plus related BVA, EP and decision-table tests. The NFRs map to the measure named in section 3.3. Full test steps are in `06_Test_Plan_and_Evidence.md`.

### 4.1 Functional requirements

| Requirement | System test | Related tests |
|---|---|---|
| FR-01 Accounts and roles | TC-01 | TC-EP-* (sender class) ; NFR-03 access tests |
| FR-02 Notices | TC-02 | TC-DT-* (notice approval N1–N4) |
| FR-03 Read receipts | TC-03 | NFR-02 receipt timing |
| FR-04 Homework | TC-04 | |
| FR-05 Attendance alerts | TC-05 | NFR-01 attendance timing |
| FR-06 Fee reminders | TC-06 | |
| FR-07 Two-way messaging | TC-07 | TC-EP-* (parent vs. teacher sender) |
| FR-08 Messaging-hours rule | TC-08 | TC-BVA-01 to TC-BVA-09; TC-DT-* (messaging rules R1–R7); TC-EP-* |
| FR-09 Admin panel | TC-09 | |
| FR-10 Record and reports | TC-10 | after-8 p.m. report checked against TC-BVA-* runs |

### 4.2 Non-functional requirements

| Requirement | Test or measure |
|---|---|
| NFR-01 Timeliness ≥ 99% within 5 min | 10,000-message load test; push gateway logs |
| NFR-02 0 duplicates or losses; receipts within 60 s | 10,000-message retry test (test harness) |
| NFR-03 100% of authorisation tests pass | Automated access tests |
| NFR-04 TLS 1.2+ on 100%, AES-256, masked numbers, 12-month deletion | Configuration review and audit |
| NFR-05 ≥ 90% of 20 parents, ≤ 3 taps | Usability test, 20 pilot parents |
| NFR-06 ≥ 99.5% availability 06:30–21:00 IST | Synthetic uptime checks |

---

## Appendix A: Requirements elicitation (Simulated for the case study)

The interviews, observations and findings below are invented for the case study to show the method; they are not real field data.

### A.1 Interview plan

| Group | Number | Sampling | Question themes |
|---|---:|---|---|
| Parents | 8 | Both pilot schools; mix of working and home-based parents, one without a smartphone | How do you learn about notices today; what do you miss; when do you want to reach the teacher and how fast; what worries you about sharing your phone number; what device and data you have |
| Teachers | 6 | Primary and secondary, class and subject teachers | How many WhatsApp groups; when do messages arrive; what messages are urgent; what limits would you accept; time spent on attendance and homework posting |
| School admins | 2 | One per pilot school | How circulars are issued and approved; how rosters and fee records are kept; how changes to rosters happen |
| Management | 2 | Group office | What records you need; which figures you review; what "active parent" means to you; who approves urgent after-hours messages |

Total: 18 interviews of about 30 minutes each. Each interview used the same themes, and answers were recorded as findings with the requirement they led to.

### A.2 Direct observation notes

**School office (2 hours, morning, school 1).**
- Circulars are typed, photocopied and sent home in diaries; the admin then phones parents who did not return the signed slip.
- The admin keeps parent phone numbers in a paper register and an Excel sheet that disagree for some students.
- Fee due dates sit in a separate accounts register; the accountant calls parents by hand before the due date.
- Roll call is on paper; absences are phoned to parents only when the teacher has time.

**Teacher's evening phone use (one evening, 19:30–22:30, one teacher).**
- 27 WhatsApp messages from parents arrived after 20:00 across three class groups, and 9 of them needed replies the next morning.
- The teacher replied to 6 of them before 22:30 because the group showed "seen" ticks.
- Two messages were urgent (a child unwell; a bus change); the rest were routine homework questions.
- Parents' phone numbers were visible to all members in each group.

### A.3 Findings to requirements

| # | Finding | Source | Requirement |
|---|---|---|---|
| 1 | "Teachers get messages late at night" (27 messages after 20:00 in one evening) | Teachers, observation | FR-08 (sending window and queue), FR-10 (after-8 p.m. report) |
| 2 | "Parents want instant replies" | Parents | FR-08 auto-reply to parent messages outside the window; FR-07 |
| 3 | Parents miss notices in the diary; admin phones the ones who did not sign | Parents, school admin | FR-02, FR-03 (delivered/read, unread list) |
| 4 | Management cannot prove what was communicated | Management | FR-10 (audit log), FR-03 |
| 5 | Circulars for the whole school need the principal's or admin's sign-off | School admin | FR-02 (school-level approval), FR-09 (approval queue) |
| 6 | Parents do not want teachers or other parents to see phone numbers | Parents, observation | NFR-04 (masked numbers) |
| 7 | Absence is phoned only when time permits | Teachers, observation | FR-05 (15-minute alert) |
| 8 | Fee due dates are chased by phone by the accountant; school does not want an online payment | School admin, management | FR-06 (7-day and 1-day reminders), Won't: payment |
| 9 | Rosters and phone numbers disagree across registers | School admin, observation | FR-09 (bulk CSV import with error report) |
| 10 | Parents are not comfortable with long text; some use budget phones | Parents | NFR-05 (Class-5 level, ≤ 3 taps, Android 8+ with 2 GB) |
| 11 | A teacher must not see another teacher's class, nor a parent another child | Management, school admin | FR-01, NFR-03 |
| 12 | Parents ask for Hindi and Marathi, and one has no smartphone | Parents | Could C-01, C-02 |
| 13 | Urgent matters (illness, bus change) cannot wait for 07:00 | Teachers, parents | FR-08 (urgent path with principal approval) |
| 14 | Homework is copied on the board and often missed by absent children | Parents, teachers | FR-04 |

### A.4 Conflict and resolution

**Conflict:** teachers wanted limits on when they can be messaged; parents wanted instant replies at any time. If the limit applied to parents, it would remove what they asked for; if replies were instant, teachers would stay tied to the phone.

**Resolution (recorded in section 3.5):**

1. The limit applies to **teacher sending**, not to parent sending. Parents can write at any time.
2. "Instant" is met by an **instant auto-reply** that sets the expectation ("Teachers reply between 07:00 and 20:00. For emergencies call the school office.") and by holding the message for the teacher at 07:00.
3. Real emergencies keep a route: an **urgent** teacher message outside the window is possible with **principal approval**, and is reported separately so management can see how often it is used.
4. The window (07:00–19:59) was agreed with both sides in a joint review with 2 teachers, 2 parents and a school admin; the end time of 20:00 is the figure in the brief.
5. Both sides accepted the compromise because each keeps its main need: teachers get quiet evenings, and parents get an immediate acknowledgement and a guaranteed morning reading. The risk that the rule is too strict is tracked as R5.
