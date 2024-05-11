# postfinance2ynab

Simple formatter to transform PostFinance account statement CSV format to a format usable for import in [YNAB](youneedabudget.com)

# Installation

Requires Python 3 and Pandas (`pip3 install pandas`).

# Usage

1. Download transactions from PostFinance using the 'Export' Feature
2. Use the script from command line to transform the downloaded CSV into YNAB-compatible CSV:

```
# For normal account transactions
python3 pf2ynab.py <path-to-csv>

# For credit card transactions
python3 pfcc2ynab.py <path-to-scv>
```

3. The files will be saved in the original directory as FileName_YNAB.csv
4. Drag-and-drop to YNAB to import the transactions

# Contributing

This is provided as-is. Feel free to submit PRs or issues, but don't expect any regular maintenance.

# Credits

Credits go to ChatGPT.