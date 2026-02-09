# Pantry Business Dashboard

A Streamlit-based dashboard for visualizing pantry business performance, including customer trends, retention rates, and product sales.

## Features

- **Monthly Filtering**: View data for November 2025, December 2025, and January 2026.
- **KPI Cards**: Track Total Customers, New vs Old, Return Customers, Gross Profit, and Retention Rate.
- **Interactive Charts**:
    - Daily Customer Trends (Line Chart)
    - Daily Retention Calculation (Line Chart)
    - Gross Profit Trends (Bar Chart)
    - Top Selling Products (Bar Chart)

## Data Sources

The dashboard reads data from Excel files stored in the repository:
- `november_data/`
- `december_data/`
- `january/`

## Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd pantry-dashboard
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the dashboard**:
    ```bash
    streamlit run app.py
    ```

## Deployment

This app is designed to be deployed on **Streamlit Community Cloud**.
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full instructions.
