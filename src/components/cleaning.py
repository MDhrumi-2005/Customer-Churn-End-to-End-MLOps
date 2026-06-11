import pandas as pd
import os


class DataCleaner:

    def __init__(
        self,
        input_path="data/validated/validated_churn.csv",
        output_path="data/processed/cleaned_churn.csv",
        report_path="data/processed/cleaning_report.txt"
    ):

        self.input_path = input_path
        self.output_path = output_path
        self.report_path = report_path

    def clean_data(self):

        print("=" * 50)
        print("Loading Validated Dataset...")
        print("=" * 50)

        # Read dataset
        df = pd.read_csv(self.input_path)

        original_rows = len(df)

        print(f"\nDataset Shape: {df.shape}")

        # ----------------------------
        # Fix TotalCharges Column
        # ----------------------------

        if "TotalCharges" in df.columns:

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

            print("Converted TotalCharges to numeric.")

        # ----------------------------
        # Missing Values
        # ----------------------------

        print("\nChecking Missing Values...")

        missing_before = df.isnull().sum().sum()

        print(f"Total Missing Values Before: {missing_before}")

        for column in df.columns:

            if pd.api.types.is_numeric_dtype(df[column]):

                median_value = df[column].median()

                df[column] = df[column].fillna(median_value)

            else:

                mode_value = df[column].mode()[0]

                df[column] = df[column].fillna(mode_value)

        missing_after = df.isnull().sum().sum()

        print(f"Total Missing Values After: {missing_after}")

        # ----------------------------
        # Duplicate Removal
        # ----------------------------

        duplicate_count = df.duplicated().sum()

        print(f"\nDuplicate Rows Found: {duplicate_count}")

        df = df.drop_duplicates()

        final_rows = len(df)

        # ----------------------------
        # Create Output Folder
        # ----------------------------

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # ----------------------------
        # Save Cleaned Dataset
        # ----------------------------

        df.to_csv(self.output_path, index=False)

        print(f"\nCleaned Dataset Saved:")
        print(self.output_path)

        # ----------------------------
        # Generate Report
        # ----------------------------

        with open(self.report_path, "w") as report:

            report.write("DATA CLEANING REPORT\n")
            report.write("=" * 50 + "\n\n")

            report.write(f"Input File: {self.input_path}\n")
            report.write(f"Output File: {self.output_path}\n\n")

            report.write(f"Original Rows: {original_rows}\n")
            report.write(f"Final Rows: {final_rows}\n\n")

            report.write(
                f"Rows Removed Due To Duplicates: "
                f"{original_rows - final_rows}\n\n"
            )

            report.write(
                f"Missing Values Before Cleaning: "
                f"{missing_before}\n"
            )

            report.write(
                f"Missing Values After Cleaning: "
                f"{missing_after}\n"
            )

        print(f"\nCleaning Report Saved:")
        print(self.report_path)

        print("\nData Cleaning Completed Successfully!")

        print("\nFinal Dataset Shape:")
        print(df.shape)


if __name__ == "__main__":

    cleaner = DataCleaner()

    cleaner.clean_data()