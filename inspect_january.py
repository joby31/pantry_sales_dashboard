import pandas as pd
import os

files = [
    'january/January_2026_Day_Wise_Customer_Count.xlsx',
    'january/Retention_data.xlsx',
    'january/new_old.xlsx',
    'january/ITEMS.xlsx'
]

with open('january_inspection_v2.txt', 'w', encoding='utf-8') as outfile:
    for f in files:
        outfile.write(f"\n{'='*20} {f} {'='*20}\n")
        if os.path.exists(f):
            try:
                df = pd.read_excel(f)
                outfile.write(f"Columns: {list(df.columns)}\n")
                outfile.write(f"Shape: {df.shape}\n")
                outfile.write("\nHead:\n")
                outfile.write(df.head(3).to_string())
                outfile.write("\n")
            except Exception as e:
                outfile.write(f"Error reading {f}: {e}\n")
        else:
            outfile.write(f"File not found: {f}\n")
