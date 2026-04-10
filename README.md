# Ad campaign performance tracker

A Python-based automation tool designed to streamline the analysis of Meta and Google Ads campaigns. It handles data cleaning, calculates essential KPIs, and generates an Excel report with integrated charts, eliminating the need for manual reporting.

## Key Features

* Metric Automation: Automatically calculates CTR, CPC, CPL, CVR, and ROAS per campaign and channel.
* Anomaly Detection: Flags days with irregular spending (defined as $> 2\sigma$ above the campaign mean).
* Visual Reporting: Generates 4 automated performance charts.
* Excel Export: Produces a comprehensive workbook with 5 dedicated tabs, saved directly to the /outputs directory.
  
## Project Structure

ad-campaign-tracker/
├── generate_data.py   # Generates mock CSV data for testing
├── pipeline.py        # Core ETL and export logic
├── run.py             # Main entry point
└── requirements.txt

## Installation & Usage

```bash
pip install -r requirements.txt
python run.py
```
Note: If data/campaigns.csv is missing, the script will automatically generate a dataset. Results are stored in the outputs/ folder.

## Core KPIs

The script automates the calculation of the following industry-standard metrics:

* **CTR (Click-Through Rate):** $Clicks / Impressions$
* **CPC (Cost Per Click):** $Spend / Clicks$
* **CPL (Cost Per Lead):** $Spend / Conversions$
* **CVR (Conversion Rate):** $Conversions / Clicks$
* **ROAS (Return on Ad Spend):** $Revenue / Spend$

## Tech Stack

Python · Pandas · NumPy · Matplotlib · OpenPyXL
