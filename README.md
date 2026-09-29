# SchoolDiary — Case 111 (SE&PM)

**Software Engineering & Project Management · Case #111 · Kishan Ojha**

This folder holds the Software Engineering and Project Management deliverables for **SchoolDiary**, a parent–teacher communication app for a group of 12 schools. It is a documentation package: requirements, design, plan, estimates, tests and risk. It is not a deployed application.

## Problem statement

A group of 12 schools talks to parents through paper diaries, printed circulars and dozens of teacher-run WhatsApp groups. This causes three problems:

- Parents miss notices.
- Teachers receive messages late at night.
- Management has no record of what was communicated.

The group wants one app for notices, homework, attendance alerts, fee reminders, and two-way messages within school hours. Teachers want limits on messaging, while parents want instant replies.

## Deliverables

| # | Document | What it covers |
|---|---|---|
| 01 | [SRS and priorities](01_SRS_and_Priorities.md) | IEEE 830-style SRS with 10 functional and 6 measurable non-functional requirements covering delivery reliability, privacy and usability. Also covers the messaging-hours rules, MoSCoW priorities, an **FR → test-case traceability matrix**, and requirements elicitation through interviews and direct observation. |
| 02 | [UML design](02_UML_Design.md) | Use-case, class, sequence (*send a notice and track read receipts*), activity, and message-state diagrams. Includes the cohesion/coupling rationale and how messaging and notices stay loosely coupled. |
| 03 | [Project plan](03_Project_Plan.md) | WBS, dependency network with the critical path, forward/backward pass, float, a Gantt chart with milestones, and resource allocation. |
| 04 | [Estimation sheet](04_Estimation_Sheet.md) | Pilot share, total effort, ideal and scheduled duration, utilisation, activity targets and confidence level. Every formula is shown, plus a section on why an estimate is not a promise. |
| 05 | [Scope management](05_Scope_Management.md) | Pilot scope versus later release versus out of scope, with the effect on time, cost and quality, and change control. |
| 06 | [Test plan and evidence](06_Test_Plan_and_Evidence.md) | Test plan and system test cases. Equivalence classes and boundary values around the 8 p.m. limit, a decision table for the messaging-hours and approval rules, the test log, DRE and defect density. |
| 07 | [Risk register and issue log](07_Risk_Register_and_Issue_Log.md) | Probability × impact matrix and an exposure-ranked register that includes low parent adoption. RMMM plans for the top three risks, and a separate issue log. |
| 08 | [Closure note and lessons learned](08_Closure_and_Lessons_Learned.md) | Pilot results against targets, quality summary, sign-off, and a lessons-learned page. |

## Key figures (from the case data)

| Quantity | Working | Result |
|---|---|---|
| Pilot share of parents | 2,300 ÷ 14,000 | **16.4%** |
| Total effort | 8 + 10 + 6 + 5 + 12 + 10 + 12 + 5 | **68 person-days** |
| Ideal duration (team of 3) | 68 ÷ 3 | **22.67 ≈ 23 working days** |
| Scheduled duration (critical path A → B → G → H) | 8 + 10 + 4 + 5 | **27 working days** |
| Team utilisation | 68 ÷ (3 × 27) | **84%** |
| Monthly-active target (pilot) | 0.90 × 2,300 | **2,070 parents** |
| Teacher sending window | Rule for FR-08 | **07:00–19:59 IST**; target of 0 teacher messages after 8 p.m. |
| Defect removal efficiency | 34 ÷ (34 + 2) | **94.4%** |

## How to read the diagrams

All diagrams are written in Mermaid and render directly on GitHub and in most Markdown viewers. Every diagram block has been checked with the Mermaid parser.

## Scope and honesty note

The brief's own figures are used exactly as given: 14,000 parents, 650 teachers, a 2,300-parent pilot, the effort table, a team of 3 and the two targets. Any other value is labelled as an assumption. Examples are the task dependencies, the 07:00 window start, and the module sizes.

Some content is **simulated for the case study**, because no real implementation, interviews, tests or pilot took place. This covers:

- the interview and observation findings
- the test log and defects
- the issue log
- the pilot results and actual durations

Each simulated section is labelled.
