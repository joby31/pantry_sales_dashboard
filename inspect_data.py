import pandas as pd
import os
import sys

# Force utf-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

folders = ["november_data", "december_data"]

with open("data_inspection_v3.txt", "w", encoding="utf-8") as f:
    for folder in folders:
        if not os.path.exists(folder):
            f.write(f"Folder {folder} not found\n")
            continue
            
        files = [x for x in os.listdir(folder) if x.endswith(".xlsx")]
        for file in files:
            path = os.path.join(folder, file)
            f.write(f"--- {folder}/{file} ---\n")
            try:
                # Try reading with default options first
                df = pd.read_excel(path)
                f.write(f"Columns: {df.columns.tolist()}\n")
                f.write(df.head(10).to_string() + "\n")
                
                # If 'Unnamed' cols, try header=1
                if "Unnamed: 0" in df.columns:
                     f.write("\n--- Retrying with header=1 ---\n")
                     df = pd.read_excel(path, header=1)
                     f.write(f"Columns: {df.columns.tolist()}\n")
                     f.write(df.head(10).to_string() + "\n")

            except Exception as e:
                f.write(f"Error reading {file}: {e}\n")
            f.write("\n" + "="*30 + "\n")
