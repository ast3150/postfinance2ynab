import pandas as pd
import sys
import os
import re

def consolidate_charges(data):
    # Convert the 'Amount' column to numeric to ensure mathematical operations work
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Initialize a list to mark indices for rows to drop
    rows_to_drop = []

    # Iterate through the DataFrame
    for i in range(len(data) - 1):  # -1 to avoid index error on the last item
        # Check if memo contains the specific text
        if "6006 ZUSCHLAG CHF IM AUSLAND" in str(data.loc[i, 'Memo']):
            # Safely add amount of the current row to the next row
            if pd.notna(data.loc[i, 'Amount']) and pd.notna(data.loc[i + 1, 'Amount']):
                data.loc[i + 1, 'Amount'] += data.loc[i, 'Amount']
            # Mark the current row to be dropped
            rows_to_drop.append(i)

    # Drop the rows where the charges are consolidated
    data = data.drop(rows_to_drop).reset_index(drop=True)
    return data

def process_bank_csv(input_file):
    # Determine the output file path
    base_path, filename = os.path.split(input_file)
    output_file = os.path.join(base_path, filename.replace('.csv', '_YNAB.csv'))

    # Load the CSV file, skipping the initial rows and excluding the last few lines
    data = pd.read_csv(input_file, sep=';', skiprows=2, skipfooter=3, engine='python')

    # Combine columns into amount column
    data['Gutschrift in CHF'] = data['Gutschrift in CHF'].fillna(data['Lastschrift in CHF'])
    data.drop(columns=['Lastschrift in CHF'], inplace=True)

    # Rename columns as per the translations required
    data.rename(columns={
        'Datum': 'Date',
        'Buchungsdetails': 'Memo',
        'Gutschrift in CHF': 'Amount'
    }, inplace=True)

    # Consolidate fees for foreign transactions into original transaction
    data = consolidate_charges(data)

    # Save the cleaned data to a new CSV file
    data.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pfcc2ynab.py <path_to_input_file.csv>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    process_bank_csv(input_file_path)
