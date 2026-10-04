# SchoolDiary — Parent–Teacher Communication Platform (Case 111)

**B.Tech CSE (2025–29) · Semester III · Software Engineering & Project Management**  
**Sole Author & Maintainer:** Kishan Ojha ([@Kishann911](https://github.com/Kishann911))

---

## 📌 Executive Summary & Problem Definition

A group of 12 schools communicates with 14,000 parents through paper diaries, circulars, and dozens of teacher-run WhatsApp groups. This legacy workflow introduces three systemic failures:

1. **Missed Circulars:** Paper slips and ad-hoc chat channels lack receipt tracking or guaranteed delivery.
2. **Late-Night Faculty Fatigue:** Teachers receive messages at all hours with no boundary enforcement.
3. **Zero Governance Record:** Management has no central, searchable communication log for institutional compliance.

**The Solution:** SchoolDiary is an Android app for parents and faculty paired with a secure web administration portal. It centralizes circulars, homework distribution, 15-minute absence alerts, fee reminders, and two-way messaging strictly constrained within school hours (07:00–19:59 IST).

---

## 📄 Publication-Grade PDF Report

The comprehensive, 29-page publication-grade PDF report is generated and available directly in this repository:

👉 **[Download SchoolDiary_Case111_Full_Report.pdf](SchoolDiary_Case111_Full_Report.pdf)**

- **Style:** Clean minimalist theme with slate navy headers (`#1B2A4A`), coral critical-path highlights (`#E05A4E`), and muted teal data tables (`#2D7D8E`).
- **Features:** Dynamic two-pass Table of Contents with exact page references, 44 structural anchors, and embedded 300-DPI vector diagrams.
- **Coverage:** Complete IEEE 830 SRS, UML design suite, CPM project plan, estimation proofs, scope boundary matrix, IEEE 829 test plan with empirical evidence, risk register, and retrospective lessons learned.

---

## 📊 Key Case Baseline Data & Computed Metrics

All figures are derived strictly from the Case 111 problem statement:

```
+------------------------------------------------------------------------------------+
|                                 CASE 111 METRICS                                   |
+------------------------------------+-----------------------------------------------+
| Total Parent Cohort                | 14,000 parents across 12 institutions         |
| Total Faculty Base                 | 650 teachers                                  |
| Pilot Scope (2 Schools)            | 2,300 parents (16.43% group share), ~107 staff |
| Bottom-Up Effort Budget            | 68 person-days across 8 work packages         |
| Team Allocation                    | 3 full-stack software engineers               |
| Theoretical Ideal Duration         | 68 ÷ 3 = 22.67 ≈ 23 working days              |
| Scheduled Duration (CPM)           | 27 working days (Critical Path A -> B -> G -> H)|
| Team Capacity & Utilisation        | 3 × 27 = 81 person-days (84% utilisation)     |
| Monthly Active Parent Target       | 90% (2,070 parents pilot; 12,600 group)       |
| Faculty Messaging SLA Target       | Zero teacher messages delivered after 20:00   |
| Measured Defect Removal Efficiency | 34 ÷ (34 + 2) = 94.4% (Target: ≥ 90%)         |
+------------------------------------+-----------------------------------------------+
```

---

## 🏗️ Architecture & Critical Path

```
CPM CRITICAL PATH (27 WORKING DAYS):
======================================================================================
[ Task A: Notices ] ---> [ Task B: Homework ] ---> [ Task G: Testing ] ---> [ Task H: Training ]
      (8 Days)                 (10 Days)                 (4 Days)                 (5 Days)
      ES:0, EF:8               ES:8, EF:18              ES:18, EF:22             ES:22, EF:27
      Float: 0d                Float: 0d                 Float: 0d                Float: 0d
======================================================================================
NON-CRITICAL TASKS (ABSORBED BY FLOAT):
- Task F: Admin Console  (10d, Float: 2d, Ends Day 10 -> Milestones M1)
- Task C: Attendance     (6d,  Float: 2d, Runs Days 10–16)
- Task D: Fee Reminders  (5d,  Float: 3d, Runs Days 12–17)
- Task E: Messaging      (12d, Float: 6d, Runs Days 0–12)
```

```
LOOSE COUPLING DOMAIN ARCHITECTURE:
======================================================================================
  +------------------+                    +-----------------------+
  |  NoticeService   |---NoticePublished->|                       |
  | (Circulars & WF) |                    | NotificationDispatcher|---> [PushGateway]
  +------------------+                    | (Idempotency, Retries,|          |
           |                              |  Fan-out Queue)       |          v
     canSendNow()                         +-----------------------+     [Parent Client]
           v                                          ^
  +------------------+                                |
  | MessagingPolicy  |                                |
  |  (Pure Rules)    |                                |
  +------------------+                                |
           ^                                          |
     canSendNow()                                     |
           |                                          |
  +------------------+                    +-----------+-----------+
  | MessagingService |----MessageReady----+
  | (Threads & Hours)|
  +------------------+
  [ZERO DIRECT CALLS OR DEPENDENCIES BETWEEN NOTICESERVICE AND MESSAGINGSERVICE]
======================================================================================
```

---

## 📂 Deliverables Index

| # | Document File | Topic & Key Contents |
|---|---|---|
| **01** | [`01_SRS_and_Priorities.md`](01_SRS_and_Priorities.md) | **IEEE 830 SRS:** 10 Functional Requirements (FR-01 to 10), 6 measurable NFRs (NFR-01 to 06), 07:00–19:59 IST messaging oracle, MoSCoW prioritization, and complete Requirements Traceability Matrix (RTM). |
| **02** | [`02_UML_Design.md`](02_UML_Design.md) | **UML Design Package:** Use-Case diagram, Class diagram, Sequence diagram (*Send notice and track read receipts*), Activity diagram, and 12-state Message lifecycle statechart with loose coupling rationale. |
| **03** | [`03_Project_Plan.md`](03_Project_Plan.md) | **Project Plan:** Work Breakdown Structure (WBS), CPM Network Diagram, Forward/Backward pass table, Float analysis, Gantt chart with milestones (M1–M4), and resource allocation table. |
| **04** | [`04_Estimation_Sheet.md`](04_Estimation_Sheet.md) | **Estimation Sheet:** Bottom-up formula working for 68 person-days, 23d ideal vs 27d scheduled duration, 84% utilisation, ±20% confidence limits, and rationale on why an estimate is not a promise. |
| **05** | [`05_Scope_Management.md`](05_Scope_Management.md) | **Scope Management:** Pilot scope vs Phase 2 rollout, comprehensive 16-row In-Scope / Out-of-Scope boundary impact table (Time, Cost, Quality), and 5-step Change Control Procedure. |
| **06** | [`06_Test_Plan_and_Evidence.md`](06_Test_Plan_and_Evidence.md) | **Test Plan & Evidence (IEEE 829-lite):** System test cases (TC-01 to 10), Equivalence Classes, Boundary Value Analysis around 8 p.m. (18 cases), Decision Table (13 rules), defect logs, 4.0 defects/KLOC density, and 94.4% DRE proof. |
| **07** | [`07_Risk_Register_and_Issue_Log.md`](07_Risk_Register_and_Issue_Log.md) | **Risk Management:** 5×5 Probability × Impact heatmap, 8 exposure-ranked risks with R1 (Low adoption) at exposure 20, RMMM action plans for top 3 risks, separate issue log (I-01 to 03), and separation justification. |
| **08** | [`08_Closure_and_Lessons_Learned.md`](08_Closure_and_Lessons_Learned.md) | **Closure & Retrospective:** Pilot actuals (86.0% adoption, zero late messages, Day 29 finish), conditional rollout governance decision, 6 empirical lessons learned, and formal multi-stakeholder sign-off matrix. |

---

## 🛠️ Reproduction & Artifact Generation

To regenerate the high-resolution vector diagrams and publication PDF:

```bash
# 1. Install prerequisites (ReportLab & Matplotlib)
pip3 install reportlab matplotlib

# 2. Generate 300-DPI architecture, CPM, Gantt, and risk diagrams
python3 generate_diagrams.py

# 3. Compile the 29-page two-pass publication-grade PDF report
python3 generate_pdf.py
```

---

## 👤 Author & Governance

- **Sole Candidate Author:** Kishan Ojha ([@Kishann911](https://github.com/Kishann911))
- **Email:** `kishanojha462@gmail.com`
- **Academic Context:** Software Engineering & Project Management, Semester III, B.Tech CSE (2025–2029)
- **License:** Academic Project Artifacts · All Rights Reserved
