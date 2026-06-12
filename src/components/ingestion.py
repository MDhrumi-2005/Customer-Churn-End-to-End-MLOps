from pathlib import Path
import shutil


DATASET_NAME = "blastchar/telco-customer-churn"

RAW_DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")


def ingest_data():
    """
    Download dataset using KaggleHub.
    
    Requires Kaggle API credentials to be set up:
      - ~/.kaggle/kaggle.json  (Linux/Mac)
      - %USERPROFILE%\\.kaggle\\kaggle.json  (Windows)
      
    Or set environment variables:
      - KAGGLE_USERNAME
      - KAGGLE_KEY
      
    If the dataset already exists locally, download is skipped.
    """

    # Check if dataset already exists — skip download
    if RAW_DATA_PATH.exists():
        print(f"✓ Dataset already exists at: {RAW_DATA_PATH}")
        print("  Skipping download.")
        return RAW_DATA_PATH

    print("Starting data ingestion from Kaggle...")

    try:
        import kagglehub

        # Download dataset via KaggleHub
        dataset_path = kagglehub.dataset_download(DATASET_NAME)

        print(f"Dataset downloaded to cache:\n{dataset_path}")

        # Create raw data directory
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)

        # Locate the CSV file
        source_file = (
            Path(dataset_path)
            / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        )

        if not source_file.exists():
            # Search for any CSV in the downloaded folder
            csv_files = list(Path(dataset_path).glob("*.csv"))
            if not csv_files:
                raise FileNotFoundError(
                    f"No CSV file found in downloaded dataset: {dataset_path}"
                )
            source_file = csv_files[0]
            print(f"Found dataset file: {source_file.name}")

        # Copy to project raw folder
        shutil.copy2(source_file, RAW_DATA_PATH)

        print(
            f"\n✓ Dataset saved to:\n"
            f"  {RAW_DATA_PATH}"
        )

        return RAW_DATA_PATH

    except ImportError:
        raise ImportError(
            "\n❌ kagglehub is not installed.\n"
            "   Install it with: pip install kagglehub\n"
            f"   Or place the dataset manually at: {RAW_DATA_PATH}"
        )

    except Exception as e:
        # Provide a helpful error message
        raise RuntimeError(
            f"\n❌ Data ingestion failed: {e}\n\n"
            "   Possible fixes:\n"
            "   1. Set Kaggle credentials:\n"
            "      - Create ~/.kaggle/kaggle.json with your API key\n"
            "      - Or set KAGGLE_USERNAME and KAGGLE_KEY env variables\n"
            f"   2. Manually place the dataset at: {RAW_DATA_PATH}\n"
            "      Download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
        ) from e


if __name__ == "__main__":
    ingest_data()
