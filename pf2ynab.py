import pandas as pd
import sys
import os
import re

def extract_payee_and_memo(text):
    payee = None
    memo = text

    # Handle different patterns
    if "KAUF/DIENSTLEISTUNG" in text:
        payee = re.search(r'KAUF/DIENSTLEISTUNG VOM \d{2}\.\d{2}\.\d{4} KARTEN NR. .*? (.+)$', text)
    elif "TWINT GELD EMPFANGEN" in text:
        payee = re.search(r'VON TELEFON-NR. \+\d+ AN TELEFON-NR. \+\d+ (.+?) MITTEILUNGEN:', text)
        memo_match = re.search(r'MITTEILUNGEN: (.+)$', text)
        memo = memo_match.group(1) if memo_match else None
    elif "TWINT GELD SENDEN" in text:
        payee = re.search(r'VOM \d{2}\.\d{2}\.\d{4} VON TELEFON-NR. \+\d+ AN TELEFON-NR. \+\d+ (.+?) MITTEILUNGEN:', text)
        memo_match = re.search(r'MITTEILUNGEN: (.+)$', text)
        memo = memo_match.group(1) if memo_match else None
    elif "TWINT KAUF/DIENSTLEISTUNG" in text:
        payee = re.search(r'TWINT KAUF/DIENSTLEISTUNG VOM \d{2}\.\d{2}\.\d{4} VON TELEFON-NR. \+\d+ (.+)$', text)
    elif "LASTSCHRIFT DAUERAUFTRAG:" in text:
        payee = re.search(r'LASTSCHRIFT DAUERAUFTRAG:.*?(\d{2}\-\d+ [A-Z].+)$', text)
    elif "LASTSCHRIFT" in text:
        payee = re.search(r'LASTSCHRIFT .*?(\d+ [A-Z].+)$', text)
    else:
        payee = None
    
    # Extract payee and memo if regex search is successful
    payee = payee.group(1) if payee else None
    
    return payee, memo

def process_bank_csv(input_file):
    # Determine the output file path
    base_path, filename = os.path.split(input_file)
    output_file = os.path.join(base_path, filename.replace('.csv', '_YNAB.csv'))

    # Load the CSV file, skipping the initial rows and excluding the last few lines
    data = pd.read_csv(input_file, sep=';', skiprows=6, skipfooter=3, engine='python')

    # Drop unnecessary columns
    data.drop(columns=['Valuta', 'Saldo in CHF'], inplace=True)

    # Combine columns into amount column
    data['Gutschrift in CHF'] = data['Gutschrift in CHF'].fillna(data['Lastschrift in CHF'])
    data.drop(columns=['Lastschrift in CHF'], inplace=True)

    # Rename columns as per the translations required
    data.rename(columns={
        'Datum': 'Date',
        'Avisierungstext': 'Memo',
        'Gutschrift in CHF': 'Amount'
    }, inplace=True)

    # Apply the extract_payee_and_memo function
    data[['Payee', 'Memo']] = data['Memo'].apply(lambda x: pd.Series(extract_payee_and_memo(x)))

    # Save the cleaned data to a new CSV file
    data.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pf2ynab.py <path_to_input_file.csv>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    process_bank_csv(input_file_path)
