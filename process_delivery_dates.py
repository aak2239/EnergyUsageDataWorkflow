import pandas as pd
from pathlib import Path
from datetime import timedelta

input_dir_path = Path('/path/to/input_files')
intermediate_dir_path = Path('/path/to/intermediate_files')
intermediate_dir_path.mkdir(parents=True, exist_ok=True)

def process_delivery_dates(file_path, intermediate_dir_path):
    df = pd.read_excel(file_path, sheet_name='Meter Entries')
    df['Delivery Date'] = pd.to_datetime(df['Delivery Date'].astype(str), errors='coerce', format='%m/%d/%y')
    df.sort_values(by='Delivery Date', inplace=True)

    df['Start Date'] = pd.NaT
    df['End Date'] = pd.NaT

    for i in df.index:
        # ... [Rest of the function remains the same] ...

    df['Start Date'] = df['Start Date'].dt.strftime('%m/%d/%y')
    df['End Date'] = df['End Date'].dt.strftime('%m/%d/%y')
    df['Start Date'].replace({pd.NaT: ''}, inplace=True)
    df['End Date'].replace({pd.NaT: ''}, inplace=True)
    df.drop(columns=['Delivery Date'], inplace=True)

    intermediate_file_path = intermediate_dir_path / f"{file_path.stem}_intermediate.xlsx"
    df.to_excel(intermediate_file_path, index=False)
    return intermediate_file_path

for file_path in input_dir_path.glob('*.xlsx'):
    intermediate_file_path = process_delivery_dates(file_path, intermediate_dir_path)
    print(f"Intermediate file saved: {intermediate_file_path}")

print("Processing of delivery dates complete.")
