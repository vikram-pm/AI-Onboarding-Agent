# P03 · AI Onboarding Agent

Concept project for an AI PM portfolio. Synthetic data only; not affiliated with Cognizant or any client.

A multi-agent system (Google ADK + Gemini) that builds a joiner's onboarding plan, checks it, and writes the daily nudge.

| Agent | Job | Tools |
| --- | --- | --- |
| plan_builder | Loads approved templates, orders steps by lead time, skips steps a switcher already did. Pauses for HR if no template exists. | get_templates, flag_template_gap, build_plan |
| compliance_guard | Checks mandatory coverage, dependency order, no invented or auto-closed steps | validate_plan |
| nudge_writer | One next-step message in English or French | get_next_step |

**Design choice:** rules that must never be wrong (scheduling, compliance checks) are deterministic code in `onboarding_agent/logic.py`. The LLM decides which tools to call, handles the template-gap path, and writes the explanations and nudges.

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env          # add your NEW Gemini key; never commit .env
python eval/run_eval.py       # offline eval, no key needed
python eval/run_eval.py --live  # full agent eval with Gemini
streamlit run app.py          # demo UI
adk web                       # optional: ADK's built-in dev UI (copy .env into onboarding_agent/)
```

## Eval (offline, 10 synthetic joiners)
- Plan correctness: 10/10
- Compliance guard caught seeded errors: 31/31 (dropped mandatory step, broken order, invented step, auto-closed compliance step)

## Deploy
Push to GitHub, create an app on Streamlit Community Cloud pointing at `app.py`, and add `GOOGLE_API_KEY` under App settings > Secrets.
