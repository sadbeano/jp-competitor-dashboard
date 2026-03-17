# Japan Market Competitor Intelligence Dashboard

A no-API-key Streamlit prototype for competitor scanning in the Japan market, with Beyond The Vines included as the own-brand benchmark layer.

## What it does

- Runs live web/news searches across the selected competitor list
- Classifies signals into pricing, drop, collaboration, strategy, performance, and store-opening buckets
- Builds a live feed and trend charts
- Generates an AI-style executive brief without requiring an LLM API key
- Scrapes Beyond The Vines Japan official pages for live observable brand stats:
  - observed bag / fashion / lifestyle assortment counts
  - observed price bands and medians
  - new-in assortment signals
  - store footprint mentions and Japan-specific store mentions
  - observed content counts from events / collaborations / press / BTV Express pages

## Competitor set preloaded

- Beyond The Vines
- Porter Yoshida & Co.
- Cotopaxi
- HAY
- Topologie
- Baggu
- Anello
- The Paper Bunny
- Standard Supply
- CASETiFY
- BEAMS
- MUJI
- and wander
- nanamica

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Recommended deployment

### Streamlit Community Cloud
Best for a fast shareable prototype.

1. Push this folder to GitHub.
2. Create a new Streamlit app.
3. Point it at `app.py`.
4. Deploy.

### Render / Railway / other Docker-friendly hosts
Also suitable if you want scheduled jobs next.

## Suggested production v2 upgrades

- Daily snapshot storage in SQLite / Postgres
- Brand-specific official collection maps for all competitors
- Product matching logic to compare like-for-like bag silhouettes and price architecture
- Optional OpenAI-compatible LLM layer for richer briefs
- Scheduled jobs and Slack / email alerts
- Exportable PDF / CSV reports

## Notes

This prototype is intentionally zero-key. That makes it fast to start, but the competitor pricing layer is best treated as directional unless you add structured brand-specific sources.


## Deployment-ready options

### Streamlit Community Cloud
1. Push this folder to a GitHub repo.
2. In Streamlit Community Cloud, create a new app from that repo.
3. Set the main file path to `app.py`.
4. Deploy.

### Render
This repo now includes a `Dockerfile` and `render.yaml`.
1. Push the folder to GitHub.
2. In Render, create a new Web Service from the repo.
3. Render should detect the Docker setup automatically.
4. Deploy and open the generated URL.

### Included deployment files
- `.streamlit/config.toml`
- `runtime.txt`
- `Dockerfile`
- `render.yaml`
