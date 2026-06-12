import os
import json
import shutil
import joblib
import pandas as pd

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


class ModelSelector:

    def __init__(self):

        self.model_dir = "models"

        self.score_file = os.path.join(
            self.model_dir,
            "model_scores.csv"
        )

    def select_best_model(self):

        print("=" * 60)
        print("MODEL SELECTION STARTED")
        print("=" * 60)

        # ----------------------------------
        # Read Leaderboard
        # ----------------------------------

        df = pd.read_csv(
            self.score_file
        )

        print("\nModel Leaderboard:\n")
        print(df)

        # ----------------------------------
        # Select Best Model
        # ----------------------------------

        best_row = df.iloc[0]

        best_model_name = best_row["model"]

        best_score = best_row["roc_auc"]

        print(
            f"\nBest Model: {best_model_name}"
        )

        print(
            f"ROC AUC: {best_score:.4f}"
        )

        # ----------------------------------
        # Copy Best Model
        # ----------------------------------

        source_model_path = os.path.join(
            self.model_dir,
            f"{best_model_name}.pkl"
        )

        best_model_path = os.path.join(
            self.model_dir,
            "best_model.pkl"
        )

        shutil.copy(
            source_model_path,
            best_model_path
        )

        # ----------------------------------
        # Save Metadata
        # ----------------------------------

        metadata = {

            "best_model":
                best_model_name,

            "accuracy":
                float(best_row["accuracy"]),

            "precision":
                float(best_row["precision"]),

            "recall":
                float(best_row["recall"]),

            "f1_score":
                float(best_row["f1_score"]),

            "roc_auc":
                float(best_row["roc_auc"])
        }

        metadata_path = os.path.join(
            self.model_dir,
            "best_model_metadata.json"
        )

        with open(
            metadata_path,
            "w"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        print(
            "\nBest Model Saved:"
        )

        print(
            best_model_path
        )

        print(
            "\nMetadata Saved:"
        )

        print(
            metadata_path
        )

        # ==================================
        # MLFLOW MODEL REGISTRY
        # ==================================

        print(
            "\nRegistering Model to MLflow..."
        )

        mlflow.set_tracking_uri(
            "sqlite:///mlflow.db"
        )

        mlflow.set_experiment(
            "Customer_Churn"
        )

        model = joblib.load(
            best_model_path
        )

        model_name = (
            "CustomerChurnModel"
        )

        with mlflow.start_run(
            run_name="Best_Model_Registration"
        ):

            mlflow.log_param(
                "best_model",
                best_model_name
            )

            mlflow.log_metric(
                "roc_auc",
                best_score
            )

            model_info = (
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model"
                )
            )

            run_id = (
                mlflow.active_run()
                .info
                .run_id
            )

        model_uri = (
            f"runs:/{run_id}/model"
        )

        registered_model = (
            mlflow.register_model(
                model_uri=model_uri,
                name=model_name
            )
        )

        client = MlflowClient()

        latest_versions = (
            client.search_model_versions(
                f"name='{model_name}'"
            )
        )

        latest_version = max(
            latest_versions,
            key=lambda x: int(x.version)
        )

        client.set_registered_model_alias(
            name=model_name,
            alias="production-candidate",
            version=latest_version.version
        )

        print(
            "\nMODEL REGISTERED SUCCESSFULLY"
        )

        print(
            f"Model Name : {model_name}"
        )

        print(
            f"Version    : "
            f"{latest_version.version}"
        )

        print(
            f"Alias      : "
            f"production-candidate"
        )

        print(
            "\nMODEL SELECTION COMPLETED"
        )


if __name__ == "__main__":

    selector = ModelSelector()

    selector.select_best_model()