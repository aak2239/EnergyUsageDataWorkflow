import pandas as pd
from pathlib import Path
import traceback
from calendar import monthrange

conversion_factors = {
    ('Gallons (US)', 'Fuel Oil (No. 1)'): 139.105,
    ('Gallons (US)', 'Fuel Oil (No. 2)'): 138.605,
    ('Gallons (US)', 'Diesel'): 151.571,
    ('Gallons (US)', 'Propane'): 91.4045,
    ('therms', None): 99.9761,
    ('kWh', None): 3.412140644,
    ('kWh (thousand Watt-hours)', None): 3.412140644,
    ('cubic feet', 'Natural Gas'): 1.0285,
    ('ccf (hundred cubic feet)', 'Natural Gas'): 102.85,
    ('kBtu (thousand Btu)', 'Electric - Grid'): 1,
    ('cf (cubic feet)', 'Natural Gas'): 1.0285,
}

def convert_to_kbtu(quantity, unit, meter_type):
    factor = conversion_factors.get((unit, meter_type), conversion_factors.get((unit, None)))
    if factor is None:
        raise ValueError(f"No conversion factor for unit {unit} and meter type {meter_type}")
    return quantity * factor

def get_month_from_date(row):
    start_date = pd.to_datetime(row['Start Date'], errors='coerce')
    end_date = pd.to_datetime(row['End Date'], errors='coerce')
    if pd.isnull(start_date) or pd.isnull(end_date):
        return 'Not Available'
    else:
        start_month_days = monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
        end_month_days = end_date.day
        start_month_majority = start_month_days >= end_month_days
        
        if start_month_majority or start_date.month == end_date.month:
            return start_date.strftime('%b-%Y')
        else:
            return end_date.strftime('%b-%Y')

def process_file(file_path, output_dir_path):
    try:
        df = pd.read_excel(file_path)
        
        df['Usage (kBTU)'] = df.apply(
            lambda row: convert_to_kbtu(row['Usage/Quantity'], row['Usage Units'], row['Meter Type']),
            axis=1
        )
        df['Month'] = df.apply(get_month_from_date, axis=1)
        
        df['Month'] = pd.to_datetime(df['Month'], format='%b-%Y', errors='coerce')
        df = df[df['Month'] >= pd.to_datetime('2016-09-01')]
        
        output_df = pd.DataFrame(df['Month'].dropna().unique(), columns=['Month']).sort_values(by='Month')
        
        for meter in df['Meter Name'].unique():
            meter_data = df[df['Meter Name'] == meter].groupby('Month')['Usage (kBTU)'].sum().reset_index()
            output_df = output_df.merge(meter_data, on='Month', how='left').rename(
                columns={'Usage (kBTU)': f'{meter} (kBTU)'}
            )
        
        for meter_type in df['Meter Type'].unique():
            meter_type_data = df[df['Meter Type'] == meter_type].groupby('Month')['Usage (kBTU)'].sum().reset_index()
            output_df = output_df.merge(meter_type_data, on='Month', how='left').rename(
                columns={'Usage (kBTU)': f'{meter_type} (kBTU)'}
            )
        
        output_file_path = output_dir_path / f"{file_path.stem}_output.csv"
        output_df.to_csv(output_file_path, index=False)
        
        print(f"Processed {file_path.name} successfully.")
        return output_file_path

    except Exception as e:
        print(f"An error occurred while processing {file_path.name}: {e}")
        traceback.print_exc()
        return None

input_dir_path = Path('/path/to/intermediate_files')
output_dir_path = Path('/path/to/output_files')

output_dir_path.mkdir(parents=True, exist_ok=True)

for file_path in input_dir_path.glob('*.xlsx'):
    process_file(file_path, output_dir_path)

print("Processing complete.")
