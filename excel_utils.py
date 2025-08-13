import pandas as pd

def read_excel_and_filter(business_functions, region):
    df = pd.read_excel('Files/Cop.xlsx')
    filtered = df[df['BusinessFunction'].isin(business_functions)]
    return filtered, region

def read_credentials_excel(path):
    """
    Reads the credentials Excel file and returns a dict with keys:
    username, password, url, reportname, businessfunctions, region
    Throws a ValueError if the file cannot be read, required columns are missing, or any value is empty.
    """
    required_cols = ['username', 'password', 'url', 'reportname', 'businessfunctions', 'region']
    try:
        df = pd.read_excel(path)
    except Exception as e:
        raise ValueError(f"Could not read credentials Excel file: {e}")
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Credentials file must contain columns: {required_cols}")
    if df.empty:
        raise ValueError("Credentials file is empty.")
    row = df.iloc[0]
    creds = {col: row[col] for col in required_cols}
    for col, val in creds.items():
        if pd.isna(val) or str(val).strip() == "":
            raise ValueError(f"Credentials value for '{col}' is missing or empty.")
    return creds
