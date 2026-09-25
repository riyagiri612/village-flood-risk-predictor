import pandas as pd
import os

SAFETY_FILE = "safety_status.csv"

def init_safety_file():
    if not os.path.exists(SAFETY_FILE):
        df = pd.DataFrame(columns=["village", "name", "contact"])
        df.to_csv(SAFETY_FILE, index=False)

def mark_safe(village, name, contact):
    df = pd.read_csv(SAFETY_FILE)
    new_row = pd.DataFrame([{"village": village, "name": name, "contact": contact}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(SAFETY_FILE, index=False)

def get_safety_records():
    df = pd.read_csv(SAFETY_FILE)
    return df.to_dict('records')

def get_safety_counts():
    df = pd.read_csv(SAFETY_FILE)
    if df.empty:
        return {}
    return df['village'].value_counts().to_dict()