
import pandas as pd
import os
import sys

# Redirect stdout to file
sys.stdout = open("verification_report.txt", "w", encoding="utf-8")

def load_excel(path, **kwargs):
    """Safe load of excel file"""
    if os.path.exists(path):
        try:
            return pd.read_excel(path, **kwargs)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

print("--- Verifying November 2025 ---")
month = "November 2025"
if month == "November 2025":
    raw_file = "november_data/jan4 (1).xlsx"
    if os.path.exists(raw_file):
        print(f"File found: {raw_file}")
        raw_df = load_excel(raw_file, header=1)
        if not raw_df.empty:
            raw_series = raw_df.iloc[:,0]
            dates = []
            
            for i in range(len(raw_series) - 1):
                val = raw_series.iloc[i]
                next_val = raw_series.iloc[i+1]
                
                # Check if next_val is a date
                try:
                    ts = pd.to_datetime(next_val, errors='coerce')
                    if not pd.isna(ts):
                        dates.append(ts)
                except:
                    pass

            if dates:
                nov_daily_df = pd.DataFrame({'Date': dates})
                # Count occurrences per date
                daily_trend_df = nov_daily_df.groupby('Date').size().reset_index(name='Total Customers')
                print(f"Calculated Total Customers: {len(dates)}")
                print("Daily Trend Head:")
                print(daily_trend_df.head().to_string())
            else:
                 print("No dates found in November file")
        else:
            print("File is empty or failed to load")
    else:
        print(f"File NOT found: {raw_file}")

print("\n--- Verifying December 2025 ---")
month = "December 2025"
if month == "December 2025":
    base_dir = "december_data"
    
    # KPI Data
    kpi_file = f"{base_dir}/Pantry_December_2025_Correct_KPI_Data (1).xlsx"
    kpi_df = load_excel(kpi_file)
    if not kpi_df.empty:
        kpi_df["Metric"] = kpi_df["Metric"].astype(str).str.strip()
        kpi_map = dict(zip(kpi_df["Metric"], kpi_df["Value"]))
        print("KPIs Loaded:")
        print(kpi_map)
    else:
        print("KPI File failed")

    # Dimensions
    daily_file = f"{base_dir}/Dec_2025_Daily_Pivot_Count.xlsx"
    daily_trend_df = load_excel(daily_file)
    print(f"Daily Trend Rows: {len(daily_trend_df)}")
    
    ret_file = f"{base_dir}/Dec_2025_Daily_Retention.xlsx"
    retention_df = load_excel(ret_file)
    print(f"Retention Rows: {len(retention_df)}")
    
    prof_file = f"{base_dir}/December_2025_Gross_Profit.xlsx"
    profit_df = load_excel(prof_file)
    print(f"Profit Rows: {len(profit_df)}")

    prod_file = f"{base_dir}/All_Product_Quantity_Sales.xlsx"
    product_df = load_excel(prod_file)
    print(f"Product Rows: {len(product_df)}")

sys.stdout.close()
