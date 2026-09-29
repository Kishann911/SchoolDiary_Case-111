# Estimation Sheet — SchoolDiary (Case 111)

## 1. Inputs (given)

| Input | Value | Source |
|---|---|---|
| Schools in the group | 12 | Case brief (given) |
| Parents | 14,000 | Case brief (given) |
| Teachers | 650 | Case brief (given) |
| Pilot schools | 2 | Case brief (given) |
| Pilot parents | 2,300 | Case brief (given) |
| Effort (person-days) | Notices 8, Homework 10, Attendance alerts 6, Fee reminders 5, Messaging with time limits 12, Admin panel 10, Testing 12, Training 5 | Case brief (given) |
| Team size | 3 | Case brief (given) |
| Target 1 | 90% of parents active monthly | Case brief (given) |
| Target 2 | Teacher messages after 8 p.m. reduced to zero | Case brief (given) |

## 2. Assumptions

| ID | Assumption |
|---|---|
| A1 | Parents are spread evenly over the 12 schools, so parents per school = 14,000 ÷ 12 |
| A2 | Teachers are proportional to parents, so pilot teachers = 650 × pilot share |
| A3 | Every person-day is one productive working day for one person; the given efforts already include rework |
| A4 | Ideal duration assumes perfect parallelism across 3 people |
| A5 | Scheduled duration comes from the CPM in `03_Project_Plan.md`; dependencies are the stated assumptions there |
| A6 | Durations are working days; day 0 is project start; no holidays or leave |
| A7 | "Active parent" (monthly active) means a parent who opens at least one notice or message in the calendar month (definition to be agreed with management) |

## 3. Calculations

| # | Quantity | Formula | Working | Result | Uses |
|---:|---|---|---|---:|---|
| 1 | Pilot share of parents | pilot parents ÷ all parents | 2,300 ÷ 14,000 = 0.16429 | **16.4%** | given |
| 2 | Parents per school | parents ÷ schools | 14,000 ÷ 12 | ≈ 1,167 | A1 |
| 3 | Pilot parents per school | pilot parents ÷ pilot schools | 2,300 ÷ 2 | 1,150 (consistent with row 2) | given |
| 4 | Pilot teachers | teachers × pilot share | 650 × 0.16429 | ≈ **107** | A2 |
| 5 | Total effort | sum of the 8 items | 8 + 10 = 18; + 6 = 24; + 5 = 29; + 12 = 41; + 10 = 51; + 12 = 63; + 5 = 68 | **68 person-days** | A3 |
| 6 | Ideal duration | effort ÷ team | 68 ÷ 3 = 22.67 | **≈ 23 working days** | A4 |
| 7 | Scheduled duration | critical path A → B → G → H | 8 + 10 + 4 + 5 | **27 working days** | A5 |
| 8 | Capacity available | team × scheduled duration | 3 × 27 | 81 person-days | A5 |
| 9 | Utilisation | effort ÷ capacity | 68 ÷ 81 = 0.8395 | **84%** | A5 |
| 10 | Schedule stretch | scheduled − ideal | 27 − 23 | 4 days | A4, A5 |
| 11 | Pilot activity target | 90% × pilot parents | 0.9 × 2,300 | **2,070 parents** | A7 |
| 12 | Full-rollout activity target | 90% × all parents | 0.9 × 14,000 | **12,600 parents** | A7 |
| 13 | After-8 p.m. teacher messages | target | reduced to zero | **0** | given |

Cross-check of the 68: Build 8 + 10 + 6 + 5 + 12 + 10 = 51; Verify 12; Deploy and train 5; 51 + 12 + 5 = 68.

## 4. Confidence level

This is a bottom-up estimate made at the requirements stage, before design, so the confidence is **±20%**.

| Measure | Point estimate | Low (× 0.8) | High (× 1.2) |
|---|---:|---:|---:|
| Effort (person-days) | 68 | 68 × 0.8 = **54.4** | 68 × 1.2 = **81.6** |
| Ideal duration (days, team of 3) | 22.67 | 54.4 ÷ 3 = **18.1** | 81.6 ÷ 3 = **27.2** |

The scheduled duration of 27 days is a point value from the CPM. At the high end (effort 81.6) the ideal duration of 27.2 days already equals it, so the critical path would then have to be re-planned.

## 5. Estimate vs promise

68 person-days, 23 days ideal and 27 days scheduled are estimates, not promises. They come from a bottom-up sum made before design, so the honest accuracy is ±20%: 54.4 to 81.6 person-days. The figures rest on assumptions I have stated, such as the dependencies, one person per task and no leave, and if any of them fails the numbers move. Messaging is the largest item at 12 person-days and the likeliest to slip, though it has 6 days of float. A promise would be a fixed date and price regardless of what we learn. An estimate is our best current forecast, and we will revise it at each milestone M1–M4 and report the variance.
