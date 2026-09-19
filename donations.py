import pandas as pd
import os

DONATIONS_FILE = "donations.csv"

def init_donations_file():
    if not os.path.exists(DONATIONS_FILE):
        df = pd.DataFrame(columns=["type", "village", "item", "quantity", "contact"])
        df.to_csv(DONATIONS_FILE, index=False)

def add_post(post_type, village, item, quantity, contact):
    df = pd.read_csv(DONATIONS_FILE)
    new_row = pd.DataFrame([{
        "type": post_type, "village": village, "item": item,
        "quantity": quantity, "contact": contact
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DONATIONS_FILE, index=False)

def get_all_posts():
    df = pd.read_csv(DONATIONS_FILE)
    return df.to_dict('records')