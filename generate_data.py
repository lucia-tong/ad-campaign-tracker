# generador de datos sintéticos: crea un csv con 90 días de campañas

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

CAMPAIGNS = [
    {"name": "Brand Awareness Q1",  "channel": "Meta",    "budget": 5000},
    {"name": "Lead Gen Spring",      "channel": "Google",  "budget": 8000},
    {"name": "Retargeting EU",       "channel": "Meta",    "budget": 3000},
    {"name": "Product Launch",       "channel": "TikTok",  "budget": 6000},
    {"name": "Email Nurture",        "channel": "Email",   "budget": 1500},
    {"name": "Search Brand",         "channel": "Google",  "budget": 4000},
    {"name": "Display Prospecting",  "channel": "Display", "budget": 2500},
]

DATES = pd.date_range("2024-01-01", "2024-03-31", freq="D")

rows = []
for campaign in CAMPAIGNS:
    base_ctr   = np.random.uniform(0.01, 0.06)
    base_cvr   = np.random.uniform(0.02, 0.12)
    base_cpc   = np.random.uniform(0.30, 3.50)
    daily_spend = campaign["budget"] / len(DATES) * np.random.uniform(0.6, 1.4, len(DATES))

    for i, date in enumerate(DATES):
        spend       = round(daily_spend[i], 2)
        impressions = int(spend / base_cpc * np.random.uniform(80, 120))
        clicks      = max(int(impressions * base_ctr * np.random.uniform(0.8, 1.2)), 0)
        conversions = max(int(clicks * base_cvr * np.random.uniform(0.7, 1.3)), 0)

        rows.append({
            "date":        date.strftime("%Y-%m-%d"),
            "campaign":    campaign["name"],
            "channel":     campaign["channel"],
            "spend":       spend,
            "impressions": impressions,
            "clicks":      clicks,
            "conversions": conversions,
        })

Path("data").mkdir(exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv("data/campaigns.csv", index=False)
print(f"CSV generado: {len(df)} filas → data/campaigns.csv")
