"""
Add New Customers to Dataset
==============================
Run this script to add new customer rows to the raw data.
The watcher (watch_and_push.py) will detect the change and
trigger the full pipeline automatically.

Usage:
    venv_mlops\\Scripts\\python.exe add_new_customers.py
"""

import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# ─────────────────────────────────────────────
# Add your new customer rows here
# Just copy-paste and change the values
# ─────────────────────────────────────────────
new_customers = [
    {
        "customerID":        "NEW-0001",
        "gender":            "Female",
        "SeniorCitizen":     0,
        "Partner":           "Yes",
        "Dependents":        "No",
        "tenure":            3,
        "PhoneService":      "Yes",
        "MultipleLines":     "No",
        "InternetService":   "Fiber optic",
        "OnlineSecurity":    "No",
        "OnlineBackup":      "No",
        "DeviceProtection":  "No",
        "TechSupport":       "No",
        "StreamingTV":       "Yes",
        "StreamingMovies":   "Yes",
        "Contract":          "Month-to-month",
        "PaperlessBilling":  "Yes",
        "PaymentMethod":     "Electronic check",
        "MonthlyCharges":    89.50,
        "TotalCharges":      268.50,
        "Churn":             "Yes"
    },
    {
        "customerID":        "NEW-0002",
        "gender":            "Male",
        "SeniorCitizen":     0,
        "Partner":           "Yes",
        "Dependents":        "Yes",
        "tenure":            55,
        "PhoneService":      "Yes",
        "MultipleLines":     "Yes",
        "InternetService":   "DSL",
        "OnlineSecurity":    "Yes",
        "OnlineBackup":      "Yes",
        "DeviceProtection":  "Yes",
        "TechSupport":       "Yes",
        "StreamingTV":       "No",
        "StreamingMovies":   "No",
        "Contract":          "Two year",
        "PaperlessBilling":  "No",
        "PaymentMethod":     "Bank transfer (automatic)",
        "MonthlyCharges":    64.00,
        "TotalCharges":      3520.00,
        "Churn":             "No"
    },
    {
        "customerID":        "NEW-0003",
        "gender":            "Female",
        "SeniorCitizen":     1,
        "Partner":           "No",
        "Dependents":        "No",
        "tenure":            1,
        "PhoneService":      "Yes",
        "MultipleLines":     "No",
        "InternetService":   "Fiber optic",
        "OnlineSecurity":    "No",
        "OnlineBackup":      "No",
        "DeviceProtection":  "No",
        "TechSupport":       "No",
        "StreamingTV":       "No",
        "StreamingMovies":   "No",
        "Contract":          "Month-to-month",
        "PaperlessBilling":  "Yes",
        "PaymentMethod":     "Electronic check",
        "MonthlyCharges":    70.35,
        "TotalCharges":      70.35,
        "Churn":             "Yes"
    },
]

# ─────────────────────────────────────────────
# Load existing data, append new rows, save
# ─────────────────────────────────────────────
df_existing = pd.read_csv(RAW_DATA)
print(f"Existing rows : {len(df_existing)}")

df_new = pd.DataFrame(new_customers)
df_updated = pd.concat([df_existing, df_new], ignore_index=True)

df_updated.to_csv(RAW_DATA, index=False)

print(f"New rows added: {len(new_customers)}")
print(f"Updated rows  : {len(df_updated)}")
print(f"Saved to      : {RAW_DATA}")
print()
print("The watcher will detect this change and trigger")
print("the full pipeline automatically in ~5 seconds.")
print("(Make sure watch_and_push.py is running)")
