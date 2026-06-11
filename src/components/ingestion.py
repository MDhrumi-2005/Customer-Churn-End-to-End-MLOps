from pathlib import Path
import shutil
import kagglehub


DATASET_NAME = "blastchar/telco-customer-churn"


def ingest_data():
    """
    Download dataset from KaggleHub
    and save it inside data/raw
    """

    print("Starting data ingestion...")

    # Download dataset
    dataset_path = kagglehub.dataset_download(
        DATASET_NAME
    )

    print(f"Dataset downloaded to cache:\n{dataset_path}")

    # Raw folder
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Dataset file
    source_file = (
        Path(dataset_path)
        / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )

    destination_file = (
        raw_dir
        / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )

    # Copy dataset
    shutil.copy2(
        source_file,
        destination_file
    )

    print(
        f"\nDataset successfully saved to:\n"
        f"{destination_file}"
    )

    return destination_file


if __name__ == "__main__":
    ingest_data()