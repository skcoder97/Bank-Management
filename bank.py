import json
import random
import string
from pathlib import Path


DATABASE = "data.json"


# ── Persistence ───────────────────────────────────────────────────────────────

def load_data():
    """Load all accounts from the JSON database."""
    try:
        p = Path(DATABASE)
        if p.exists():
            with open(p) as f:
                return json.loads(f.read())
    except Exception as e:
        print(f"Error loading data: {e}")
    return []


def save_data(data):
    """Persist all accounts to the JSON database."""
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))


# ── Helpers ───────────────────────────────────────────────────────────────────

def generate_account_no():
    """Generate a random alphanumeric + special-char account number."""
    alpha  = random.choices(string.ascii_letters, k=3)
    num    = random.choices(string.digits, k=3)
    spchar = random.choices("!@#$%^&*", k=1)
    parts  = alpha + num + spchar
    random.shuffle(parts)
    return "".join(parts)


def find_user(data, account_no, pin):
    """Return list of matching user records (should be 0 or 1)."""
    return [u for u in data if u["AccountNo"] == account_no and u["Pin"] == pin]


# ── Core operations ───────────────────────────────────────────────────────────

def create_account(name, age, email, pin):
    """
    Create a new bank account.
    Returns (success: bool, message: str, account_info: dict | None)
    """
    if age < 18:
        return False, "You must be at least 18 years old to open an account.", None
    if not str(pin).isdigit() or len(str(pin)) != 4:
        return False, "PIN must be exactly 4 digits.", None

    data   = load_data()
    acc_no = generate_account_no()
    record = {
        "Name":      name,
        "Age":       int(age),
        "Email":     email,
        "Pin":       int(pin),
        "AccountNo": acc_no,
        "Balance":   0,
    }
    data.append(record)
    save_data(data)
    return True, "Account created successfully!", record


def deposit(account_no, pin, amount):
    """
    Deposit money into an account.
    Returns (success: bool, message: str, new_balance: int | None)
    """
    data  = load_data()
    users = find_user(data, account_no, pin)

    if not users:
        return False, "Invalid account number or PIN.", None
    if amount <= 0 or amount > 10000:
        return False, "Deposit amount must be between ₹1 and ₹10,000.", None

    users[0]["Balance"] += int(amount)
    save_data(data)
    return True, f"₹{amount:,} deposited successfully!", users[0]["Balance"]


def withdraw(account_no, pin, amount):
    """
    Withdraw money from an account.
    Returns (success: bool, message: str, new_balance: int | None)
    """
    data  = load_data()
    users = find_user(data, account_no, pin)

    if not users:
        return False, "Invalid account number or PIN.", None
    if amount <= 0:
        return False, "Withdrawal amount must be greater than ₹0.", None
    if users[0]["Balance"] < amount:
        return False, f"Insufficient balance. Available: ₹{users[0]['Balance']:,}", None

    users[0]["Balance"] -= int(amount)
    save_data(data)
    return True, f"₹{amount:,} withdrawn successfully!", users[0]["Balance"]


def get_details(account_no, pin):
    """
    Fetch account details.
    Returns (success: bool, message: str, user: dict | None)
    """
    data  = load_data()
    users = find_user(data, account_no, pin)

    if not users:
        return False, "Invalid account number or PIN.", None
    return True, "Account found.", users[0]


def update_details(account_no, pin, new_name=None, new_email=None, new_pin=None):
    """
    Update mutable account fields (name, email, pin).
    Returns (success: bool, message: str)
    """
    data  = load_data()
    users = find_user(data, account_no, pin)

    if not users:
        return False, "Invalid account number or PIN."

    if new_pin is not None:
        if not str(new_pin).isdigit() or len(str(new_pin)) != 4:
            return False, "New PIN must be exactly 4 digits."
        users[0]["Pin"] = int(new_pin)

    if new_name:
        users[0]["Name"]  = new_name
    if new_email:
        users[0]["Email"] = new_email

    save_data(data)
    return True, "Details updated successfully!"


def delete_account(account_no, pin):
    """
    Permanently delete an account.
    Returns (success: bool, message: str)
    """
    data  = load_data()
    users = find_user(data, account_no, pin)

    if not users:
        return False, "Invalid account number or PIN."

    data.remove(users[0])
    save_data(data)
    return True, "Account closed successfully."