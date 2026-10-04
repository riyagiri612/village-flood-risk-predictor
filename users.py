import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.csv"
FIELDS = ["name", "email", "password_hash"]


def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)


def register_user(name, email, password):
    """Returns True if registered, False if the email already exists."""
    init_users_file()
    with open(USERS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["email"].lower() == email.strip().lower():
                return False
    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([name.strip(), email.strip(), generate_password_hash(password)])
    return True


def verify_user(email, password):
    """Returns the user's name if email and password match, otherwise None."""
    init_users_file()
    with open(USERS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["email"].lower() == email.strip().lower() and check_password_hash(row["password_hash"], password):
                return row["name"]
    return None