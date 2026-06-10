from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path(
    "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

VALIDATED_DATA_PATH = Path(
    "data/validated/validated_churn.csv"
)

EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn"
]


def validate_data():

    print("Loading raw dataset...")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    if df.empty:
        raise ValueError("Dataset is empty")

    missing_columns = [
        col
        for col in EXPECTED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate Rows: {duplicate_count}")

    null_counts = df.isnull().sum()

    print("\nMissing Values:")
    print(null_counts[null_counts > 0])

    VALIDATED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        VALIDATED_DATA_PATH,
        index=False
    )

    print(
        f"\nValidated dataset saved to:"
        f"\n{VALIDATED_DATA_PATH}"
    )


if __name__ == "__main__":
    validate_data()