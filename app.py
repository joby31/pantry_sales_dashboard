
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Pantry Business Dashboard", layout="wide")

# Valid months
MONTHS = ["November 2025", "December 2025", "January 2026"]

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Pantry Dashboard")
    month = st.selectbox("📅 Select Month", MONTHS)
    
    st.markdown("---")
    st.markdown("### Dashboard Settings")
    show_kpi = st.checkbox("Show KPI Cards", True)
    show_charts = st.checkbox("Show Charts", True)

def load_excel(path, **kwargs):
    """Safe load of excel file"""
    if os.path.exists(path):
        try:
            return pd.read_excel(path, **kwargs)
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Data Loading Logic
kpi_data = {}
daily_trend_df = pd.DataFrame()
retention_df = pd.DataFrame() # For December/January
profit_df = pd.DataFrame()    # For December
product_df = pd.DataFrame()   # For December/January

if month == "November 2025":
    # November: Raw Data in 'november_data/jan4 (1).xlsx'
    raw_file = "november_data/jan4 (1).xlsx"
    if os.path.exists(raw_file):
        # Read header=1 safely as per inspection
        raw_df = load_excel(raw_file, header=1)
        if not raw_df.empty:
            # Logic: The file has structure like: Customer Name -> Date -> ...
            # We iterate to find valid Dates and associate them with count.
            # Simpler robust approach:
            # 1. Convert column 0 to datetime to find date rows.
            # 2. Iterate: If row is a date, increment count for that date. (Assuming 1 customer per date entry or similar)
            # Actually, per inspection: Name is at index i, Date at i+1.
            
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
                total_customers = len(dates)
            else:
                 total_customers = 0

            kpi_data = {
                "Total Customers": total_customers,
                "New Customers": 0,    # N/A
                "Old Customers": 0,    # N/A
                "Return Customers": 0, # N/A
                "Gross Profit": 0,     # N/A
                "Retention %": 0.0     # N/A
            }

elif month == "December 2025":
    # December: Structured Data in 'december_data/'
    base_dir = "december_data"
    
    # 1. Load KPI Data
    kpi_file = f"{base_dir}/Pantry_December_2025_Correct_KPI_Data (1).xlsx"
    kpi_df = load_excel(kpi_file)
    if not kpi_df.empty:
        # Expected cols: Metric, Value
        kpi_df["Metric"] = kpi_df["Metric"].astype(str).str.strip()
        kpi_map = dict(zip(kpi_df["Metric"], kpi_df["Value"]))
        kpi_data = {
            "Total Customers": int(kpi_map.get("Total Customers", 0)),
            "New Customers": int(kpi_map.get("New Customers", 0)),
            "Old Customers": int(kpi_map.get("Total Customers", 0)) - int(kpi_map.get("New Customers", 0)), # Fallback calc
            "Return Customers": int(kpi_map.get("Return_customer", 0)),
            "Gross Profit": float(kpi_map.get("Gross Profit", 0)),
            "Retention %": float(kpi_map.get("Average Retention (%)", 0))
        }

    # 2. Load Daily Customer Trend (Pivot Count)
    daily_file = f"{base_dir}/Dec_2025_Daily_Pivot_Count.xlsx"
    daily_trend_df = load_excel(daily_file) # Cols: Date, Customer Count
    
    # 3. Load Retention Data
    ret_file = f"{base_dir}/Dec_2025_Daily_Retention.xlsx"
    retention_df = load_excel(ret_file) # Cols: Date, Old Customers, Prev Day Total, Daily Retention %
    
    # 4. Load Gross Profit Trend
    prof_file = f"{base_dir}/December_2025_Gross_Profit.xlsx"
    profit_df = load_excel(prof_file) # Cols: Date, Gross Profit
    
    # 5. Load Products
    prod_file = f"{base_dir}/All_Product_Quantity_Sales.xlsx"
    product_df = load_excel(prod_file) # Cols: Product_Name, Quantity_Sold

elif month == "January 2026":
    # January: Data in 'january/'
    base_dir = "january"
    
    # 1. Load KPI Data (from new_old.xlsx)
    kpi_file = f"{base_dir}/new_old.xlsx"
    kpi_df = load_excel(kpi_file, header=1) # categorization is in row 1 (0-indexed)
    
    if not kpi_df.empty and 'categorize' in kpi_df.columns:
        total_customers = len(kpi_df)
        new_customers = len(kpi_df[kpi_df['categorize'].astype(str).str.lower() == 'new'])
        # "Old" covers both returning and old in this context, or we just map old -> old
        old_customers = len(kpi_df[kpi_df['categorize'].astype(str).str.lower() == 'old'])
        
        kpi_data = {
            "Total Customers": total_customers,
            "New Customers": new_customers,
            "Old Customers": old_customers,
            "Return Customers": old_customers, # Assuming Old = Return for simplicity if not distinguished
            "Gross Profit": 0,     # Not available
            "Retention %": 0.0     # Will be calc from retention file if possible, else 0
        }

    # 2. Load Daily Customer Trend
    daily_file = f"{base_dir}/January_2026_Day_Wise_Customer_Count.xlsx"
    daily_trend_df = load_excel(daily_file)
    
    # 3. Load Retention Data
    ret_file = f"{base_dir}/Retention_data.xlsx"
    retention_df = load_excel(ret_file)
    # If retention_df has 'Retention %' column, we can calculate average for KPI
    if not retention_df.empty and 'Retention %' in retention_df.columns:
        # Convert to numeric, coerce errors, drop na
        avg_ret = pd.to_numeric(retention_df['Retention %'], errors='coerce').mean()
        kpi_data["Retention %"] = avg_ret
        # Rename for chart consistency
        retention_df = retention_df.rename(columns={'Retention %': 'Daily Retention %'})

    # 4. Load Gross Profit Data
    prof_file = f"{base_dir}/January_2026_Datewise_Data.xlsx"
    profit_df = load_excel(prof_file)
    
    if not profit_df.empty:
        # Standardize columns for visualization: 'Date', 'Gross Profit'
        # File has 'Date', 'Amount'
        if 'Amount' in profit_df.columns:
            profit_df = profit_df.rename(columns={'Amount': 'Gross Profit'})
            
        # Calculate Total Gross Profit for KPI
        if 'Gross Profit' in profit_df.columns:
             kpi_data["Gross Profit"] = profit_df['Gross Profit'].sum()

    # 5. Load Products (ITEMS.xlsx)
    prod_file = f"{base_dir}/ITEMS.xlsx"
    # Header is on row 2 (index 2), so header=2
    product_df = load_excel(prod_file, header=2)
    # Rename columns to match December logic if needed: 'Row Labels' -> 'Product_Name', 'Sum of QuantityInvoiced' -> 'Quantity_Sold'
    if not product_df.empty:
        product_df = product_df.rename(columns={
            'Row Labels': 'Product_Name', 
            'Sum of QuantityInvoiced': 'Quantity_Sold'
        })


st.title(f"🥫 Pantry Performance Dashboard — {month}")

# Display KPIs
if show_kpi and kpi_data:
    k1, k2, k4, k5, k6 = st.columns(5)
    k1.metric("👥 Total Customers", kpi_data.get("Total Customers", 0))
    k2.metric("🆕 New Customers", kpi_data.get("New Customers", "-"))
    # k3 (Old Customers) removed as per request
    k4.metric("🔁 Return Customers", kpi_data.get("Return Customers", "-"))
    
    gp = kpi_data.get("Gross Profit", 0)
    k5.metric("💰 Gross Profit", f"₹ {gp:,.0f}" if gp else "-")
    
    ret = kpi_data.get("Retention %", 0)
    k6.metric("📊 Avg Retention", f"{ret:.1f}%" if ret else "-")
    
    st.markdown("---")
elif show_kpi:
    st.warning("No KPI Data available for this month.")

# Visualizations
if show_charts:
    # Row 1: Trends
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📈 Customer Trends")
        if not daily_trend_df.empty:
            if month == "November 2025":
                 fig1 = px.line(daily_trend_df, x="Date", y="Total Customers", markers=True, title="Daily Total Customers")
            else:
                # December specific structure or general fallback
                y_col = daily_trend_df.columns[1] # Typically 'Customer Count' or similar
                fig1 = px.line(daily_trend_df, x="Date", y=y_col, markers=True, title="Daily Total Customers")
            
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No daily data.")

    with c2:
        st.subheader("📉 Retention Trends")
        if not retention_df.empty:
            fig2 = px.line(retention_df, x="Date", y="Daily Retention %", markers=True, title="Daily Retention %")
            fig2.update_traces(line_color="purple")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Retention trend not available.")

    # Row 2: Profit & Products
    c3, c4 = st.columns([1, 1])
    
    with c3:
        st.subheader("💰 Gross Profit Trend")
        if not profit_df.empty:
            # Changed to line graph as requested
            fig3 = px.line(profit_df, x="Date", y="Gross Profit", markers=True, title="Daily Gross Profit Trend")
            fig3.update_traces(line_color="green")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Profit data not available.")

    with c4:
        st.subheader("🏆 Top Products")
        if not product_df.empty:
            # Sort and take top 10
            top_products = product_df.sort_values(by="Quantity_Sold", ascending=False).head(10)
            fig4 = px.bar(top_products, x="Quantity_Sold", y="Product_Name", orientation="h", text="Quantity_Sold")
            fig4.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Product data not available.")

st.markdown("<center>📊 Pantry Custom Dashboard</center>", unsafe_allow_html=True)
