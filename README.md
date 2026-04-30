# Support Team Performance Dashboard

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B)](https://support-metrics-dashboard-gwdhg8qipd7ftybpxstcgq.streamlit.app/)

**🚀 Live App:** https://support-metrics-dashboard-gwdhg8qipd7ftybpxstcgq.streamlit.app/

An interactive Streamlit dashboard for visualizing support team KPIs — cases handled, CSAT scores, resolution times, and escalations.

## Features

- **KPI Cards** — total cases, avg resolution time, avg CSAT, total escalations
- **CSAT Line Chart** — score trends over time per advisor
- **Cases Bar Chart** — total cases handled per advisor
- **Escalation Pie Chart** — breakdown by category (Billing, Technical, Policy)
- **Resolution Time Chart** — avg handle time per advisor (color-coded)
- **CSV Upload** — load your own data or use the built-in sample
- **Date Range & Advisor Filters** — sidebar controls for all charts
- **Export** — download filtered data as CSV

## Setup

```bash
git clone https://github.com/renhairston-oss/support-metrics-dashboard.git
cd support-metrics-dashboard
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly openpyxl
```

## Run Locally

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## CSV Format

Upload any CSV with these columns:

| Column | Type | Example |
|--------|------|---------|
| Date | YYYY-MM-DD | 2024-01-02 |
| Advisor Name | string | Marcus Johnson |
| Cases Handled | int | 18 |
| Avg Resolution Time (min) | float | 23.5 |
| CSAT Score | float (1–5) | 4.7 |
| Escalations | int | 1 |
| Escalation Category | string | Technical |

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub
3. Click **New app** → select this repo → set main file to `app.py`
4. Click **Deploy**

## File Structure

```
support-dashboard/
├── app.py                  # Main Streamlit app
├── data/
│   └── support_data.csv    # Sample data (36 rows, 4 advisors)
└── README.md
```
