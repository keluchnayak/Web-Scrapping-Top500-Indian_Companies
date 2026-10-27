import pandas as pd
import numpy as np
import os

def clean_data(raw_csv_path, output_csv_path, output_excel_path):
    print("Loading raw data from:", raw_csv_path)
    df = pd.read_csv(raw_csv_path)
    print(f"Original shape: {df.shape}")
    
    # 1. Drop Duplicates
    df = df.drop_duplicates(subset=['company_url'])
    print(f"Shape after dropping duplicates: {df.shape}")
    
    # 2. Text Cleaning: Headquarters
    # Format is usually 'City, State, Country'. We extract the main city.
    def extract_city(hq_str):
        if pd.isna(hq_str):
            return np.nan
        return str(hq_str).split(',')[0].strip()
        
    df['hq_city'] = df['headquarters'].apply(extract_city)
    
    # 3. Text Cleaning: Employees
    if 'employees' in df.columns:
        df['employees_clean'] = df['employees'].astype(str).str.replace('Employees', '').str.strip()
        # Clean up 'nan' strings that might appear from astype(str)
        df.loc[df['employees_clean'] == 'nan', 'employees_clean'] = np.nan
        
    # The scraping process (using JSON-LD) means our numbers (ratings, reviews) 
    # are already clean floats/ints, so we do not need complex regex parsing for them!
    
    # 4. Save the cleaned dataset
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    df.to_csv(output_csv_path, index=False)
    print(f"Cleaned data saved to CSV: {output_csv_path}")
    
    try:
        df.to_excel(output_excel_path, index=False)
        print(f"Cleaned data saved to Excel: {output_excel_path}")
    except Exception as e:
        print(f"Note: Could not save Excel file. {e}")

if __name__ == "__main__":
    raw_path = '../data/ambitionbox_top_500_raw.csv'
    clean_csv = '../data/ambitionbox_top_500_cleaned.csv'
    clean_xlsx = '../data/ambitionbox_top_500_cleaned.xlsx'
    
    # Run cleaning if the raw file exists
    if os.path.exists(raw_path):
        clean_data(raw_path, clean_csv, clean_xlsx)
    else:
        print(f"Error: Raw data file {raw_path} not found. Ensure the scraper has finished running.")
