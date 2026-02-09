import pandas as pd
import os

# Mocking the load_excel function from app.py
def load_excel(path, **kwargs):
    if os.path.exists(path):
        try:
            return pd.read_excel(path, **kwargs)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Simulating the logic for January 2026
base_dir = "january"
kpi_data = {}

with open('verification_report.txt', 'w', encoding='utf-8') as f:
    f.write("--- Testing January 2026 Data Loading ---\n")

    # 1. Load KPI Data (from new_old.xlsx)
    kpi_file = f"{base_dir}/new_old.xlsx"
    f.write(f"Loading {kpi_file}...\n")
    kpi_df = load_excel(kpi_file, header=1) # categorization is in row 1 (0-indexed)

    if not kpi_df.empty and 'categorize' in kpi_df.columns:
        total_customers = len(kpi_df)
        new_customers = len(kpi_df[kpi_df['categorize'].astype(str).str.lower() == 'new'])
        old_customers = len(kpi_df[kpi_df['categorize'].astype(str).str.lower() == 'old'])
        
        kpi_data = {
            "Total Customers": total_customers,
            "New Customers": new_customers,
            "Old Customers": old_customers,
            "Return Customers": old_customers,
            "Gross Profit": 0,
            "Retention %": 0.0
        }
        f.write("KPI Data Loaded:\n")
        f.write(str(kpi_data) + "\n")
    else:
        f.write("Failed to load KPI data or 'categorize' column missing.\n")

    # 2. Load Daily Customer Trend
    daily_file = f"{base_dir}/January_2026_Day_Wise_Customer_Count.xlsx"
    f.write(f"Loading {daily_file}...\n")
    daily_trend_df = load_excel(daily_file)
    f.write(f"Daily Trend Shape: {daily_trend_df.shape}\n")
    f.write(daily_trend_df.head(2).to_string() + "\n")

    # 3. Load Retention Data
    ret_file = f"{base_dir}/Retention_data.xlsx"
    f.write(f"Loading {ret_file}...\n")
    retention_df = load_excel(ret_file)
    if not retention_df.empty and 'Retention %' in retention_df.columns:
        avg_ret = pd.to_numeric(retention_df['Retention %'], errors='coerce').mean()
        kpi_data["Retention %"] = avg_ret
        f.write(f"Calculated Average Retention: {avg_ret}\n")
    f.write(f"Retention DF Shape: {retention_df.shape}\n")

    # 5. Load Products (ITEMS.xlsx)
    prod_file = f"{base_dir}/ITEMS.xlsx"
    f.write(f"Loading {prod_file} with header=2...\n")
    product_df = load_excel(prod_file, header=2)
    if not product_df.empty:
        product_df = product_df.rename(columns={
            'Row Labels': 'Product_Name', 
            'Sum of QuantityInvoiced': 'Quantity_Sold'
        })
        f.write(f"Product DF Shape: {product_df.shape}\n")
        f.write(f"Columns: {product_df.columns.tolist()}\n")
        f.write(product_df.head(2).to_string() + "\n")
    else:
        f.write("Product DF is empty.\n")
