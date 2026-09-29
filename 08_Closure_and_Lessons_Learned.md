# Closure Note and Lessons Learned — SchoolDiary

*Simulated for the case study — the pilot results, defect data and issues are simulated actuals, in line with `06_Test_Plan_and_Evidence.md` and `07_Risk_Register_and_Issue_Log.md`.*

## 1. Closure note

### Project summary

SchoolDiary is a parent–teacher communication app for a group of 12 schools with 14,000 parents and 650 teachers. It delivers notices, homework, attendance alerts, fee reminders and two-way messaging within school hours. The project built all 8 work items (68 person-days, 3 people) and ran the pilot at 2 schools (adoption measured over the first pilot month; post-release defects counted over the first 2 pilot weeks) with 2,300 parents (16.4% of all parents) and about 107 teachers.

### Pilot results

| Measure | Target | Result | Status |
|---|---|---|---|
| Monthly active parents | 90% (2,070 of 2,300) | 1,978 of 2,300 = **86.0%** (−4.0 pp; 92 parents short) | Not met |
| Teacher messages delivered after 20:00 | 0 | **0** routine. 3 principal-approved urgent messages, reported separately | Met |
| Notice read rate within 24 h | (no target set) | 81% | Reported |
| Delivery within 5 min (NFR-01) | ≥ 99% | 99.3% | Met |

### Planned vs actual finish

| Point | Finish (working days) |
|---|---:|
| Baseline plan (critical path A → B → G → H) | 27 |
| Actual | **29** (+2 days, +7.4%) |

- Messaging took 14 days instead of 12 (R7 happened). E had 6 days of total float, but P3 was due to start D after E, so P1 took 2 days of D on days 16–18. D still finished by day 18, and there was no critical-path impact.
- The actual slip came from UAT defect fixes: Testing (task G, on the critical path) took 6 days instead of 4.

### Scope delivered

FR-01 to FR-10 were delivered on Android and the web admin panel, in English, for the 2 pilot schools. The Could items (C-01 multilingual UI, C-02 SMS fallback, C-03 meeting booking), the iOS app and the 10 other schools are later scope. Online fee payment, video calls, student logins and WhatsApp integration remain out of scope.

### Quality summary

36 defects were found in total: 34 before release and 2 after release (in the first 2 pilot weeks). DRE = 34 ÷ (34 + 2) = **94.4%**, above the 90% target. Test-phase DRE = 27 ÷ 29 = 93.1%, and defect density is 4.0 per KLOC. Severity: critical 1, high 7, medium 16, low 12. The two post-release defects were 1 high (an after-hours message queued twice on midnight rollover) and 1 medium; both are fixed.

### Decision

**Conditional rollout** to the remaining 10 schools (11,700 parents). The adoption figure (86.0% against 90%) is below target, so SMS fallback (C-02) is prioritised to lift adoption. Rollout proceeds school by school if adoption reaches at least 80% by week 3 (the R1 trigger).

### Open risks

| Risk | Exposure | Status at closure |
|---|---:|---|
| R1 Low parent adoption | 20 | Partly happened (86.0%). Stays open, is the main rollout risk. |
| R2 Push delivery failure / no smartphone | 12 | Open. I-03 happened. Reduced by SMS fallback. |
| R5 Messaging rule too strict | 12 | Open. 3 urgent messages needed approval in the pilot. |
| R3 Teachers keep WhatsApp groups | 12 | Open. Watched with the after-8 p.m. report. |

R7 has happened and is closed with no critical-path effect. Open risks carry into the rollout with their RMMM plans (see `07_Risk_Register_and_Issue_Log.md`).

### Handover items

- Source code, configuration and the messaging-hours rule tests (BVA and decision table)
- Test suite and defect log
- Admin guide, teacher and parent quick guides
- Adoption and delivery reports for the pilot
- Issue log with the two open items (I-01, I-03)

### Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Project manager | Kishan Ojha | Closure note issued | |
| Sponsor (school group management) | (representative) | Conditional rollout approved | |
| QA lead | (Developer/QA) | Test evidence and DRE accepted | |
| Principals of the 2 pilot schools | (representatives) | Pilot results accepted | |

## 2. Lessons learned (Simulated for the case study)

| # | What happened | Root cause | Lesson | Action for the 10-school rollout | Owner |
|---|---|---|---|---|---|
| 1 | Testing took 6 days instead of 4, and the project finished on day 29 instead of 27. | UAT found defects late, and fixes and retests were done inside the critical Testing task, with no buffer. | The critical path needs schedule buffer where late defects are likely. | Add a 2-day fix-and-retest buffer after UAT and start UAT earlier on finished modules. | Project manager |
| 2 | Adoption was 86.0% against 90%. | Onboarding relied on class teachers alone, and some parents lacked smartphones or data. | An adoption target needs its own plan, not only a product. | Run the onboarding drive from week 1 and bring SMS fallback (C-02) forward, with weekly adoption tracking and the R1 trigger. | Project manager with school sponsors |
| 3 | Messaging took 14 days instead of 12. | The time rules, queue and approval flow were more complex than estimated. | Total float absorbed the slip only because work was reassigned; resource-levelled float is smaller. | Keep float visible in the plan and add 20% to complex rule-based work in estimates. | Project manager |
| 4 | An after-hours message was queued twice on midnight rollover (DEF-35) and reached the pilot. | TC-BVA-08 and TC-BVA-09 were run as separate messages on a reset test clock, so a 23:59 message still queued when the clock crossed 00:00 was never exercised. | Time-based rules need state tests across the boundary, not only single values. | Add clock-controlled tests across midnight, month end and holidays, and rerun TC-BVA-08 and TC-BVA-09 on every release. | QA lead |
| 5 | Contact numbers were missing for 186 of 2,300 parents (I-01). | Import data came from school records that no one had validated. | Data quality is a schedule item, not an assumption. | Ask each school to validate rosters before import and use the admin panel's dry-run report. | School admins |
| 6 | Push was delayed on low-end phones with battery saver on (I-03). | Testing devices were mostly newer than the parents' phones. | Test on the devices users really have. | Keep two Android 8 phones with 2 GB RAM in the test kit, publish battery-saver help, and fund the SMS fallback. | Developer 1 (technical lead) |
