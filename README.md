# AI Onboarding Agent

An AI agent that builds each new consultant’s onboarding plan, starts the slowest steps first, and stops for a human when it isn’t sure. Project 03 of my AI Product Manager portfolio.

**Live case study:** https://vikram-pm.github.io/AI-Onboarding-Agent
**Live prototype:** https://vikram-pm.github.io/AI-Onboarding-Agent/prototype.html

> Concept project with synthetic data only. Not affiliated with or endorsed by Cognizant or any client.

## What’s here

| Path | What it is |
| --- | --- |
| `index.html` | Case study page (GitHub Pages) |
| `prototype.html` | Live prototype: the full end-to-end flow in the browser |
| `video/product-demo.mp4` | Product demo walkthrough (1:53) |
| `docs/PRD.md` | Discovery, PRD and experiment design |
| `docs/interview-deck.pdf` | Interview deck |
| `img/` | Wireframes and agent flow diagram |
| `agent/` | Multi-agent prototype: Google ADK + Gemini, evals, Streamlit demo |

## Results (offline eval, 10 synthetic joiners)

- Plan correctness: 10/10
- Seeded errors caught by the compliance guard: 31/31
- Key finding: one client’s plan can’t hit the Day 10 target because the background check takes 7 days. Starting clearance before day one brings it to Day 6.

## Live AI in the prototype

The prototype runs in demo mode by default. To use Gemini, open **AI mode** in the header and paste your own key. The key stays in that browser tab only.

**Never commit an API key to this repo.** For the Python agent, put your key in `agent/.env` (ignored by Git).

## Run the agent locally

```bash
cd agent
pip install -r requirements.txt
cp .env.example .env            # add your Gemini key
python eval/run_eval.py         # offline eval, no key needed
python eval/run_eval.py --live  # full agent eval
streamlit run app.py            # demo UI
```

© 2026 Vikram Seenivasan
