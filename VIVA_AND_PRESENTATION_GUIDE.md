# SchoolDiary (Case 111) — Presentation & Viva Preparation Guide

**Subject:** Software Engineering & Project Management (SE&PM)  
**Academic Programme:** B.Tech CSE (2025–29), Semester III  
**Candidate Author:** Kishan Ojha ([@Kishann911](https://github.com/Kishann911))

---

## 🎯 1. The 60-Second Elevator Pitch

> *"SchoolDiary is a centralized parent–teacher communication platform designed for a group of 12 schools with 14,000 parents and 650 teachers. Currently, communication relies on physical student diaries, paper circulars, and unmonitored WhatsApp groups. This creates three critical failures: parents miss notices, teachers face intrusive late-night messaging, and school management has zero audit record of what was communicated.*
>
> *We engineered an Android client and web administration console covering notices with read receipts, homework tracking, 15-minute attendance alerts, fee reminders (without payment liability), and time-restricted messaging governed by an automated 07:00–19:59 IST window. We piloted the system across 2 schools (2,300 parents, 16.43% group share) using a 3-person team with 68 person-days of bottom-up effort. Scheduled via Critical Path Method over 27 working days (84% utilisation), the pilot achieved zero late teacher messages, 99.3% delivery reliability, and a 94.4% Defect Removal Efficiency."*

---

## 🔢 2. The Numerical Cheat Sheet (Memorize These Exact Figures)

Never invent or approximate these numbers; they are derived from the case brief and project calculations:

| Metric | Exact Value | Mathematical Derivation / Basis |
|---|---|---|
| **Total Parents** | `14,000` | Given group population across 12 institutions |
| **Total Teachers** | `650` | Given faculty count |
| **Pilot Schools** | `2` | Initial pilot institutional boundary |
| **Pilot Parents** | `2,300` | Given pilot parent cohort |
| **Pilot Share of Parents** | `16.43% (≈ 16.4%)` | `2,300 ÷ 14,000 = 0.1642857...` |
| **Pilot Teachers** | `~107` | `650 × (2,300 ÷ 14,000) = 106.78 ≈ 107` |
| **Total Bottom-Up Effort** | `68 person-days` | Notices(8) + Homework(10) + Attendance(6) + Fee Reminders(5) + Messaging(12) + Admin(10) + Testing(12) + Training(5) |
| **Engineering Headcount** | `3 developers` | P1 (Lead), P2 (Frontend/Trainer), P3 (Backend/QA) |
| **Theoretical Ideal Duration** | `22.67 ≈ 23 working days` | `68 ÷ 3 = 22.67 days` (assumes 100% unconstrained parallelism) |
| **Scheduled CPM Duration** | `27 working days` | Critical Path: Task A (8d) + Task B (10d) + Task G (4d) + Task H (5d) = 27d |
| **Available Capacity** | `81 person-days` | `3 developers × 27 working days = 81 person-days` |
| **Resource Utilisation** | `83.95% ≈ 84%` | `68 person-days ÷ 81 person-days capacity` |
| **Schedule Stretch** | `4 working days` | `27 scheduled days − 23 ideal days = 4 days` |
| **Pilot Monthly Active Target** | `2,070 parents` | `90% × 2,300 pilot parents` |
| **Group Monthly Active Target** | `12,600 parents` | `90% × 14,000 group parents` |
| **Late Messaging Target** | `0 messages` | Routine messages delivered after 20:00 IST reduced to zero |
| **Pre-Release Defects (E)** | `34 defects` | Req Review(4) + Design(3) + Unit(11) + Integ(7) + System(6) + UAT(3) |
| **Post-Release Defects (D)** | `2 defects` | Pilot W1 rollover bug (DEF-35) + W2 UI display bug (DEF-36) |
| **Defect Removal Efficiency (DRE)**| `94.4%` | `34 ÷ (34 + 2) = 34 ÷ 36 = 0.9444...` (Target: ≥ 90%) |
| **System Defect Density** | `4.00 defects/KLOC` | `36 defects ÷ 9.0 KLOC total codebase` |
| **Highest Density Module** | `Messaging (5.45/KLOC)`| `12 defects ÷ 2.2 KLOC` (36% above system average) |

---

## 🏛️ 3. Core Software Engineering Concepts Explained

### 1. Loose Coupling between Notices and Messaging
- **The Problem:** Notices and Messaging are the two heaviest modules. If they depend directly on each other, changes to messaging hours could break circular publishing.
- **The Design:** NoticeService and MessagingService have **zero direct method calls, zero shared interfaces, and zero cross-module database foreign keys**.
- **How they integrate:** Event-driven architecture.
  - NoticeService emits `NoticePublished` event.
  - MessagingService emits `MessageReady` event.
  - A shared `NotificationDispatcher` asynchronously consumes both events, resolves device push tokens, attaches idempotency keys, and handles exponential retry backoffs.
  - Both query a pure, stateless `MessagingPolicy` rules engine for the 07:00–19:59 IST window.
- **Coupling Type:** Data coupling via asynchronous domain events (the weakest and most maintainable form of coupling).

### 2. Why 27 Days and Not 23 Days?
- **Ideal Duration (23 days):** Simply `68 person-days ÷ 3 people = 22.67 days`. This is a mathematical fantasy assuming perfect parallel execution with zero dependencies.
- **Scheduled Duration (27 days):** Derived via Critical Path Method (CPM):
  1. **Serial Dependency:** Task B (Homework, 10d) directly reuses circular publishing code from Task A (Notices, 8d). Thus, Task B cannot finish before Day 18 (`8 + 10 = 18d`).
  2. **Feature Freeze Gate:** Task G (System Testing, 12 person-days ÷ 3 people = 4 working days) requires all functional modules to be code-complete. It cannot begin before Day 18.
  3. **Single Trainer Constraint:** Task H (Training, 5 working days across 2 schools) is delivered by Developer P2 in person and cannot be divided among multiple people.
  4. **Critical Chain:** `A(8) -> B(10) -> G(4) -> H(5) = 27 working days`.
  5. The **4-day gap (27 − 23)** represents the unavoidable structural cost of software dependencies and single-resource training constraints.

### 3. Boundary Value Analysis (BVA) Around 8 p.m. & Midnight
- Sending window is defined as **07:00 to 19:59 IST inclusive**.
- **Crucial Boundary Cases:**
  - `19:58 IST`: Inside window -> Sent immediately.
  - `19:59 IST`: Last valid minute -> Sent immediately. *(Caught DEF-15: off-by-one error where developer wrote `t <= 19:58`)*.
  - `20:00 IST`: Boundary minute -> Blocked and enqueued for next school day 07:00.
  - `20:01 IST`: After-hours -> Enqueued for 07:00.
  - `23:59 IST`: Enqueued for Day D+1 07:00.
  - `00:00 IST (Day D+1)`: Must resolve to the *exact same* single queue release at 07:00. *(Caught DEF-35: message sent at 23:59 was erroneously re-queued at midnight, delivering duplicate push notifications)*.

### 4. Why Risks and Issues Must Be Kept in Separate Registers
- **A Risk** is an *uncertain future event* with a probability between 0 and 1 ($0 < P < 1$). It is managed proactively using probability-impact scoring ($P \times I$), mitigation actions, monitoring metrics, and contingency thresholds.
- **An Issue** is a *certain, realized event* ($P = 1.0$) currently impacting the project. It requires immediate corrective action, an assigned owner, and a resolution deadline.
- **Why never combine them:**
  1. A realized issue cannot be scored $P \times I$ without distorting the exposure ranking.
  2. Urgent firefighting of current issues inevitably crowds out proactive mitigation of high-impact future risks.
  3. Tracking both separately illustrates the causal transition from risk to issue (e.g., Risk R6 on CSV errors became live Issue I-01 when 186 parent phone numbers were missing).

### 5. Defect Removal Efficiency (DRE)
- **Formula:** $\text{DRE} = \frac{E}{E + D}$
  - $E = 34$ (pre-release defects discovered across inspections, unit, integration, system, and UAT).
  - $D = 2$ (post-release defects discovered during the initial 2 weeks of the pilot).
  - $\text{DRE} = \frac{34}{34 + 2} = \frac{34}{36} = 94.4\%$
- **Significance:** Standard industry benchmark is $\ge 90\%$. SchoolDiary achieved 94.4%, proving that rigorous multi-stage verification caught approximately 17 out of every 18 defects before software reached end users.

---

## 🎤 4. Top 15 Viva / Examiner Questions with Model Answers

### Q1: What is the core problem SchoolDiary solves?
**Answer:**  
*"SchoolDiary replaces fragmented paper circulars, physical student diaries, and ad-hoc WhatsApp groups across 12 schools. WhatsApp groups expose teacher phone numbers, lead to late-night parent messages, and leave management with no centralized audit trail. SchoolDiary centralizes communication into an Android app and web admin portal, providing read receipts, 15-minute absence alerts, and automated time-window enforcement (07:00–19:59 IST) to eliminate late-night messaging."*

### Q2: What is the pilot's share of all parents?
**Answer:**  
*"The pilot takes place at 2 schools with 2,300 parents out of a total population of 14,000 parents across all 12 institutions. The pilot share is computed as $2,300 \div 14,000 = 0.1642857\dots$, which is exactly **16.43% (or approximately 16.4%)**. Proportional teacher staffing is $650 \times 16.43\% \approx 107$ teachers."*

### Q3: What is the total bottom-up effort and scheduled duration?
**Answer:**  
*"The bottom-up effort across the 8 work packages is $8 + 10 + 6 + 5 + 12 + 10 + 12 + 5 = \mathbf{68\text{ person-days}}$. For our team of 3 developers, the ideal duration is $68 \div 3 = 22.67 \approx 23\text{ working days}$. However, the scheduled duration determined by Critical Path Method (CPM) is **27 working days** along the critical chain Task A (Notices, 8d) $\rightarrow$ Task B (Homework, 10d) $\rightarrow$ Task G (Testing, 4d) $\rightarrow$ Task H (Training, 5d)."*

### Q4: Why is the project duration 27 days instead of 23 days?
**Answer:**  
*"23 days assumes 100% unconstrained parallelism, which is impossible due to three physical constraints: First, Task B (Homework) depends on Task A (Notices) because it reuses notice publishing infrastructure, pushing completion to Day 18. Second, Task G (Testing) requires full feature freeze, so it cannot start before Day 18. Third, Task H (Training) is delivered by a single instructor (Developer P2) across 2 campuses over 5 contiguous days. The 4-day stretch ($27 - 23$) is the natural cost of task precedence and single-resource bottlenecks, giving an 84% team utilisation rate."*

### Q5: How did you ensure loose coupling between Notices and Messaging?
**Answer:**  
*"NoticeService and MessagingService have zero direct calls, dependencies, or foreign keys between them. They interact purely through asynchronous domain events: NoticeService emits `NoticePublished` and MessagingService emits `MessageReady`. A shared `NotificationDispatcher` consumes these events, manages idempotency keys, and calls the PushGateway adapter. Both modules share only a stateless, pure rules engine (`MessagingPolicy`) for sending-window evaluations."*

### Q6: What happens if a teacher sends a message at 20:00? At 06:59? At 19:59?
**Answer:**  
*"The sending window is 07:00 to 19:59 IST inclusive:
- At **19:59**: The message is allowed and sent immediately (last minute of the window).
- At **20:00**: The message is outside the window. If routine, it is blocked, transitioned to `QUEUED`, and scheduled for automatic dispatch at 07:00 next school day. The teacher sees 'Queued for 07:00'.
- At **06:59**: It is still outside the window; it is queued and sent 1 minute later at 07:00."*

### Q7: What happens if an urgent message is rejected by the Principal outside school hours?
**Answer:**  
*"Under Decision Table Rule R5, if an urgent message sent outside school hours is rejected by the Principal (or receives no response by 07:00), it is **not discarded and not sent immediately**. Instead, it is transitioned to the `QUEUED` state and released at 07:00 with the regular morning queue. During testing, test case `TC-DT-R5` caught defect `DEF-28`, where a rejected message was erroneously dispatched immediately."*

### Q8: What happens when a parent messages a teacher at 22:00?
**Answer:**  
*"Parents are permitted to send messages 24/7. However, out-of-hours parent messages are not pushed to the teacher's device at night. Under Rule R7, the message is placed in `HELD_FOR_TEACHER` status and released to the teacher's notification inbox at 07:00. The parent receives an instantaneous automated reply stating: 'Teachers reply between 07:00 and 20:00. For emergencies call the school office.' This balances parental peace of mind with faculty evening boundaries."*

### Q9: What are your non-functional requirements and how are they measured?
**Answer:**  
*"We specified 6 measurable NFRs without ambiguous language:
1. **NFR-01 (Timeliness):** $\ge 99\%$ notices reach push gateway within 5 min; attendance alerts reach parents within 15 min of roll call.
2. **NFR-02 (Integrity):** 0 lost or duplicate messages across a 10,000-message retry test with idempotency keys; read receipts stored within 60 s.
3. **NFR-03 (Privacy):** 100% pass on role-boundary penetration tests; zero cross-class or cross-child data leakage.
4. **NFR-04 (Protection):** TLS 1.2+ on 100% of connections; AES-256 at rest; phone numbers masked in UI; data purged 12 months post-exit.
5. **NFR-05 (Usability):** $\ge 90\%$ of 20 test parents read notice and reply in $\le 3$ taps on Android 8+ (2 GB RAM) at Class-5 reading level.
6. **NFR-06 (Availability):** $\ge 99.5\%$ uptime during 06:30–21:00 IST core hours."*

### Q10: What is your Defect Removal Efficiency (DRE) and defect density?
**Answer:**  
*"We recorded 34 pre-release defects ($E$) across reviews, unit, integration, system, and UAT testing, and 2 post-release defects ($D$) during the first 2 pilot weeks. Using the formula $\text{DRE} = \frac{E}{E + D}$, our DRE is $34 \div (34 + 2) = \mathbf{94.4\%}$, exceeding the $\ge 90\%$ target. Across our 9.0 KLOC codebase, overall defect density was **4.00 defects/KLOC**. Messaging was our densest module at **5.45 defects/KLOC** due to complex state-machine edge cases."*

### Q11: Explain defect DEF-15 and defect DEF-35.
**Answer:**  
*"**DEF-15** was an off-by-one unit test failure caught by boundary test `TC-BVA-05`. The developer had coded the window condition as `t <= 19:58`, causing 19:59 (the valid last minute) to be blocked.
**DEF-35** was a high-severity defect that escaped to Week 1 of the pilot. When a message sent at 23:59 crossed midnight into Day D+1 (00:00), the scheduler created a second queue entry, resulting in duplicate delivery at 07:00. This escaped because test cases `TC-BVA-08` and `TC-BVA-09` were executed on static, reset test clocks rather than a continuous clock sweep across midnight."*

### Q12: Why is the estimation an estimate and not a promise?
**Answer:**  
*"An estimate is a probabilistic forecast based on requirements known at a given point in time; a promise is a fixed contractual commitment regardless of newly discovered complexity. Because our estimate was prepared bottom-up prior to architectural design, an honest industry confidence band of $\pm 20\%$ applies ($54.4$ to $81.6\text{ person-days}$). It depends on stated assumptions (such as valid CSV rosters and zero engineer attrition). As work progresses through milestones M1–M4, estimates are re-baselined based on empirical variance."*

### Q13: What was the pilot result against the targets? Was the rollout approved?
**Answer:**  
*"In the pilot:
- **Late messages after 20:00:** Achieved **0 routine messages** ($\text{Target: } 0$, MET). Only 3 principal-approved urgent overrides occurred.
- **Monthly active parents:** Achieved **86.0%** (1,978 of 2,300 parents), missing the 90.0% target by 4.0 percentage points (92 parents short).
- **Rollout Decision:** The steering committee approved a **Conditional Rollout** to the remaining 10 schools. Rollout proceeds on the condition that C-02 SMS Fallback is deployed to reach offline households, and newly onboarded schools must demonstrate $\ge 80\%$ adoption by Week 3."*

### Q14: What is the highest risk in your Risk Register, and how do you monitor it?
**Answer:**  
*"Our highest-exposure risk is **Risk R1: Low Parent Adoption** (Probability 4, Impact 5, **Exposure = 20**, High Band). We mitigate it via teacher-led parent orientation onboarding, in-app circular mirroring, and help desks. We monitor it weekly using the Monthly Active Parent report. Our **trigger metric** is adoption falling below 80% (1,840 parents) by Week 3 or circular 24-hour read rate falling below 75%. If triggered, we immediately fast-track the C-02 SMS Fallback gateway."*

### Q15: Why are Payment, WhatsApp integration, and Student Logins out of scope?
**Answer:**  
*"They were explicitly excluded based on technical risk and scope boundary analysis:
1. **Online Fee Payment:** Excluded to eliminate PCI-DSS compliance, banking gateway integration, merchant fees, and fraud liabilities; the school requested read-only reminders.
2. **WhatsApp Integration:** Excluded because third-party chat bypasses our 20:00 cutoff rule and prevents central audit logging, defeating the project's purpose.
3. **Student Logins:** Excluded to avoid child COPPA/DPDP privacy and consent compliance overhead; primary communication is between teachers and parents."*

---

## 📑 5. Folder & Deliverables Map

When walking through your code repository with an examiner, navigate in this logical sequence:

```
03_SchoolDiary_Case-111/
├── README.md                      <-- Executive overview, key metrics, ASCII diagrams, author info
├── SchoolDiary_Case111_Full_Report.pdf <-- 29-page publication-grade PDF report
├── VIVA_AND_PRESENTATION_GUIDE.md <-- (This document) Viva & presentation defense cheat sheet
├── 01_SRS_and_Priorities.md       <-- IEEE 830 SRS, 10 FRs, 6 NFRs, MoSCoW, RTM, Elicitation notes
├── 02_UML_Design.md              <-- Use Case, Class, Sequence, Activity, Statechart, Loose Coupling
├── 03_Project_Plan.md             <-- WBS, CPM Critical Path, Forward/Backward pass, Gantt, Resources
├── 04_Estimation_Sheet.md         <-- Mathematical formulas, 68 pd, 23d vs 27d, Estimate vs Promise
├── 05_Scope_Management.md         <-- Pilot scope, 16-row In/Out-of-scope matrix, Change control
├── 06_Test_Plan_and_Evidence.md   <-- IEEE 829-lite, TC-01..10, BVA (18), Decision Table (13), DRE 94.4%
├── 07_Risk_Register_and_Issue_Log.md <-- 5x5 heatmap, 8 risks, RMMM plans, separate Issue log (I-01..03)
├── 08_Closure_and_Lessons_Learned.md <-- Pilot actuals (86%), conditional rollout, 6 lessons, sign-off
├── diagrams/                      <-- High-resolution 300-DPI vector diagrams (CPM, Gantt, Architecture, etc.)
├── generate_diagrams.py           <-- Python script generating all 5 matplotlib diagrams
└── generate_pdf.py                <-- Production-grade 2-pass ReportLab PDF compiler with dynamic TOC
```
