import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeatureEngineering:

    def __init__(
        self,
        input_path="data/processed/cleaned_churn.csv",
        artifacts_dir="artifacts/feature_engineering"
    ):

        self.input_path = input_path
        self.artifacts_dir = artifacts_dir

    def process(self):

        print("=" * 50)
        print("FEATURE ENGINEERING STARTED")
        print("=" * 50)

        # Create artifacts directory
        os.makedirs(self.artifacts_dir, exist_ok=True)

        # Load cleaned dataset
        df = pd.read_csv(self.input_path)

        print(f"\nDataset Shape: {df.shape}")

        # --------------------------------------------------
        # Remove Customer ID
        # --------------------------------------------------

        if "customerID" in df.columns:
            df.drop("customerID", axis=1, inplace=True)

        # --------------------------------------------------
        # Encode Target Variable
        # --------------------------------------------------

        df["Churn"] = df["Churn"].map({
            "No": 0,
            "Yes": 1
        })

        # --------------------------------------------------
        # Separate Features & Target
        # --------------------------------------------------

        X = df.drop("Churn", axis=1)
        y = df["Churn"]

        # --------------------------------------------------
        # Identify Column Types
        # --------------------------------------------------

        categorical_cols = X.select_dtypes(
            include=["object", "string"]
        ).columns.tolist()

        numerical_cols = X.select_dtypes(
            include=["number"]
        ).columns.tolist()

        print("\nCategorical Columns:")
        print(categorical_cols)

        print("\nNumerical Columns:")
        print(numerical_cols)

        # --------------------------------------------------
        # Preprocessing Pipeline
        # --------------------------------------------------

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    StandardScaler(),
                    numerical_cols
                ),
                (
                    "cat",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False
                    ),
                    categorical_cols
                )
            ]
        )

        # --------------------------------------------------
        # Transform Features
        # --------------------------------------------------

        X_processed = preprocessor.fit_transform(X)

        print(f"\nProcessed Feature Shape: {X_processed.shape}")

        # --------------------------------------------------
        # Train-Test Split
        # --------------------------------------------------

        X_train, X_test, y_train, y_test = train_test_split(
            X_processed,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        print(f"\nX Train Shape : {X_train.shape}")
        print(f"X Test Shape  : {X_test.shape}")

        print(f"y Train Shape : {y_train.shape}")
        print(f"y Test Shape  : {y_test.shape}")

        # --------------------------------------------------
        # Save Preprocessor
        # --------------------------------------------------

        preprocessor_path = os.path.join(
            self.artifacts_dir,
            "preprocessor.pkl"
        )

        joblib.dump(
            preprocessor,
            preprocessor_path
        )

        print(f"\nPreprocessor Saved:")
        print(preprocessor_path)

        # --------------------------------------------------
        # Save Train/Test Data
        # --------------------------------------------------

        pd.DataFrame(X_train).to_csv(
            os.path.join(
                self.artifacts_dir,
                "X_train.csv"
            ),
            index=False
        )

        pd.DataFrame(X_test).to_csv(
            os.path.join(
                self.artifacts_dir,
                "X_test.csv"
            ),
            index=False
        )

        pd.DataFrame(y_train).to_csv(
            os.path.join(
                self.artifacts_dir,
                "y_train.csv"
            ),
            index=False
        )

        pd.DataFrame(y_test).to_csv(
            os.path.join(
                self.artifacts_dir,
                "y_test.csv"
            ),
            index=False
        )

        print("\nTrain/Test Files Saved Successfully")

        print("\nFeature Engineering Completed Successfully!")

        print("\nGenerated Artifacts:")
        print(" - preprocessor.pkl")
        print(" - X_train.csv")
        print(" - X_test.csv")
        print(" - y_train.csv")
        print(" - y_test.csv")


if __name__ == "__main__":

    engineer = FeatureEngineering()
    engineer.process()