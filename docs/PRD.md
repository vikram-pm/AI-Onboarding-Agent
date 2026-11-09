# Project 03 · AI Onboarding Assistant — Discovery & PRD

Oct 22, 2026 · Vikram Seenivasan · Concept project, synthetic data only

## Overview

An AI onboarding assistant can cut the time for a consultant to become ready to contribute on a client project from an estimated 15 working days to 9. This is a personal concept project framed around Cognizant Canada's internal onboarding, using synthetic data only. All baselines below are hypotheses until discovery interviews confirm them.

**Problem.** Onboarding is split across HR, IT access, mandatory training, client-specific requirements and project ramp-up, with no single owner. New joiners don't know what to do next, access requests queue in the wrong order, and project managers answer the same questions for every joiner.

**Hero skill: experimentation and growth.** Success is decided by an A/B test on activation, not by model accuracy. That separates this project from Project 01 (extraction accuracy) and Project 02 (AI evaluation).

**Two segments.** New hires joining Cognizant Canada, and existing employees rolling onto a new client project. Both end at the same moment: ready to contribute on the project.

## Discovery

The biggest delay is likely waiting on access and client clearances, not learning. Five interviews will test that before the PRD is locked.

### Personas

| Persona | Context | Goal | Main pain |
| --- | --- | --- | --- |
| Aisha, new-hire consultant | Joins in Toronto, first project in week 2 | Be useful fast and look competent | Doesn't know the order of steps; waits on access |
| Daniel, senior associate | Rolls onto a bank client in Montréal | Get client access and context quickly | Every client has different clearances; French-language documents |
| Mei, project manager | Runs a 12-person delivery team | Joiners billable from week 1 | Answers the same questions; no view of joiner readiness |

Other stakeholders: HR onboarding, IT service desk, Learning, and the privacy office (approver).

### Current-state journey

| Stage | What happens | Pain | Est. time |
| --- | --- | --- | --- |
| 1. Pre-start | Forms, background check, equipment order | No visibility of what's pending | 1–2 weeks before start |
| 2. Company setup | Laptop, accounts, mandatory training | Requests raised in the wrong order | 2–4 days |
| 3. Client clearance | Client background check, client accounts, client training | Varies by client; longest lead time | 3–10 days |
| 4. Project ramp-up | Read project docs, meet the team, set up tools | Docs scattered; joiner asks the PM | 3–5 days |
| 5. First contribution | First task done and logged | Readiness isn't tracked anywhere | Day 15 (est.) |

### Hypotheses to validate

- **H1:** Over half the delay is waiting time on access and clearances that could start earlier.
- **H2:** Joiners lose time because they don't know the next step, not because steps are hard.
- **H3:** Project managers spend about 6 hours per joiner on repeat questions.
- **H4:** Project switchers repeat setup work that a reusable profile would remove.

### Interview plan

Five 30-minute interviews: 2 recent hires, 1 project switcher, 1 project manager, 1 HR onboarding coordinator.

1. Walk me through your last onboarding, from offer or staffing call to first real task.
2. Where did you wait, and what were you waiting for?
3. How did you know what to do next? Who did you ask?
4. What did you have to do again that you'd done before?
5. (PM) How do you know when a joiner is ready? How long does it take you per joiner?
6. If one thing were fixed, what would save the most time?

## Scope and solution

The assistant builds each joiner a personalised onboarding plan, nudges the next step, and shows the project manager who is ready. It drives action, whereas Project 02 answers questions on request, so P03 reuses the P02 assistant for Q&A instead of rebuilding it.

**How it works.** Inputs are role, client, province, project start date, and whether the joiner is new or switching. Gemini assembles a plan from approved onboarding templates, orders steps by lead time (long clearances first), and sends one next step at a time.

| In scope (MVP) | Out of scope |
| --- | --- |
| Personalised plan from approved templates | Raising access or HR requests automatically |
| Next-step nudges by email or Teams | Writing to HR or IT systems |
| PM readiness view per joiner | Using onboarding data in performance reviews |
| Q&A handed off to the P02 assistant | Client-side onboarding inside client systems |
| English and French plans | Learning content creation |

**Experiment hook.** Control keeps today's static checklist; treatment gets the AI plan and nudges. Experiment design comes after discovery.

## Requirements and user stories

Seven stories make the MVP; the first four are must-haves for the experiment.

| ID | As a… | I want… | So that… | Priority |
| --- | --- | --- | --- | --- |
| US1 | New joiner | A plan ordered by lead time | Long clearances start on day 1 | Must |
| US2 | New joiner | One clear next step at a time | I don't have to work out what's next | Must |
| US3 | Project switcher | My completed company steps carried over | I only do client-specific steps | Must |
| US4 | Project manager | A readiness view per joiner | I can plan their first task | Must |
| US5 | New joiner | To ask a question in the plan | I get an answer without asking the PM | Should |
| US6 | Quebec joiner | My plan in French | I can work in my language | Should |
| US7 | HR coordinator | To see where joiners get stuck | I can fix the template | Could |

**AI behaviour rules**

- Builds plans only from approved templates and shows the source for each step.
- Never marks a compliance or security step complete; only the owning system or a person can.
- Flags a missing template (unknown client or role) to HR instead of guessing steps.
- Nudges at most once a working day, and joiners can pause them.

## Metrics

The north-star metric is the **10-day activation rate**: the share of joiners who are ready to contribute within 10 working days of their project start date. "Ready" means all required access is granted, mandatory training is complete, and a first project task is logged.

| Metric | Type | Baseline (hypothesis) | Target | Method |
| --- | --- | --- | --- | --- |
| 10-day activation rate | North star | 35% | 50% | Access, training and task logs |
| Working days to first contribution | Primary | 15 | 9 | Same logs, median |
| PM hours on joiner questions | Secondary | 6 h per joiner | 3 h | PM time survey |
| Joiner confidence at day 10 | Secondary | 3.0 / 5 | 4.0 / 5 | 3-question pulse survey |
| Compliance steps skipped or out of order | Guardrail | 0 | No increase | Audit of step completion |
| Nudge pause rate | Guardrail | n/a (new) | Under 10% | Product analytics |
| Plan steps wrong or missing | Guardrail | n/a (new) | Under 5% | Weekly review by HR |

Baselines are placeholders; interviews and a sample of past onboarding records will replace them before the experiment is sized.

## Responsible AI and Canadian context

The main risk is that onboarding tracking feels like surveillance, so the data is used only to help joiners and is kept out of performance decisions.

| Area | What it means here | Design response |
| --- | --- | --- |
| Privacy (PIPEDA; Quebec Law 25) | Personal data in plans; Quebec requires a privacy impact assessment and transparency | Minimum fields, privacy office sign-off, plain-language notice to joiners |
| Ontario electronic monitoring policy | Employers with 25+ staff must disclose electronic monitoring | Readiness tracking listed in the disclosed policy |
| French language (Quebec) | Workplace communications in French | French plans and nudges for Quebec joiners |
| Accessibility (AODA) | Ontario accessibility standards | Plan and readiness view meet WCAG 2.1 AA |
| Fairness | Plans could differ in quality by role or client | Review plan errors by segment each week |
| Human control | AI could mark compliance steps done | AI never closes compliance steps |
| Data | Real records can't leave Cognizant | Synthetic joiners, clients and templates only |

## Experiment design

The test will be decided on **days to first contribution**, not the activation rate: at an assumed 40 joiners a month, powering on activation would take about 8 months, while days to first contribution needs about 3.

**Hypothesis.** If joiners get a plan ordered by lead time and one next-step nudge a day, mean working days to first contribution falls from 15 to 12, because clearances start earlier and joiners stop waiting to ask.

| Element | Decision |
| --- | --- |
| Control | Today's static onboarding checklist |
| Treatment | AI plan, daily next-step nudge, PM readiness view |
| Unit | Individual joiner, 50/50 split |
| Stratification | Segment (new hire vs switcher) and province (Quebec vs rest of Canada) |
| Decision metric | Working days to first contribution (log-transformed) |
| Reported metrics | 10-day activation rate, PM hours, joiner confidence |
| Guardrails | Compliance steps skipped, nudge pause rate, plan errors |
| Significance and power | 5% two-sided, 80% power |

### Sample size

| Decision metric | Detects | Per arm | Total | Time at 40 joiners/month |
| --- | --- | --- | --- | --- |
| Days to first contribution (SD 6 days, assumed) | 15 → 12 days | 63 | 126 | About 3 months |
| 10-day activation rate | 35% → 50% | 170 | 340 | About 8.5 months |

Enrolment runs 13 weeks, plus 2 weeks so the last joiners reach day 10. Onboarding happens once per person, so novelty effects are not a concern.

### Known risk: contamination

A project manager may have joiners in both arms and coach control joiners using what they see in the treatment view. Randomising by project team would remove this but roughly doubles the sample needed. The MVP accepts the risk and measures it: PMs log help given to each joiner.

### Decision and stop rules

- **Ship:** at least 2 days faster, significant at 5%, and no guardrail breached.
- **Iterate:** positive but not significant; review where treatment joiners still stall.
- **Stop:** no improvement, or worse than control.
- **Pause immediately:** any compliance step skipped in treatment, plan errors over 10%, or nudge pause rate over 20% in the first 2 weeks.

## Open questions and next steps

The biggest open question for the experiment is volume: if Cognizant Canada onboards only a few dozen joiners a month, a simple A/B test may need months to reach significance.

- [ ] Run the 5 interviews and replace the hypothesised baselines
- [ ] Estimate monthly joiner volume per segment (new hire vs switcher)
- [ ] Confirm which HR, IT and learning tools the plan would read from
- [ ] Validate the 6-day standard deviation and 40 joiners a month, then re-run the sample size
- [x] Figma flow and wireframes for control and treatment
- [x] Agent prototype (Google ADK), live browser prototype, product demo
