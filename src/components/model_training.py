import os
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


class ModelTrainer:

    def __init__(self):

        self.artifact_dir = "artifacts/feature_engineering"
        self.model_dir = "models"

        os.makedirs(self.model_dir, exist_ok=True)

    def evaluate_model(self, model, X_test, y_test):

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        try:
            y_prob = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_prob)
        except:
            roc_auc = 0

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc
        }

    def train(self):

        print("=" * 60)
        print("MODEL TRAINING STARTED")
        print("=" * 60)

        # ---------------------------
        # Load Data
        # ---------------------------

        X_train = pd.read_csv(
            f"{self.artifact_dir}/X_train.csv"
        )

        X_test = pd.read_csv(
            f"{self.artifact_dir}/X_test.csv"
        )

        y_train = pd.read_csv(
            f"{self.artifact_dir}/y_train.csv"
        ).squeeze()

        y_test = pd.read_csv(
            f"{self.artifact_dir}/y_test.csv"
        ).squeeze()

        print("\nData Loaded Successfully")

        models = {

            "RandomForest": RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                random_state=42
            ),

            "XGBoost": XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric="logloss"
            ),

            "LightGBM": LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        }

        leaderboard = []

        mlflow.set_experiment("Customer_Churn")

        for model_name, model in models.items():

            print(f"\nTraining {model_name}...")

            with mlflow.start_run(run_name=model_name):

                model.fit(X_train, y_train)

                metrics = self.evaluate_model(
                    model,
                    X_test,
                    y_test
                )

                mlflow.log_params(
                    model.get_params()
                )

                mlflow.log_metrics(metrics)

                model_path = (
                    f"{self.model_dir}/{model_name}.pkl"
                )

                joblib.dump(
                    model,
                    model_path
                )

                mlflow.log_artifact(model_path)

                mlflow.sklearn.log_model(
                    model,
                    artifact_path=model_name
                )

                leaderboard.append({

                    "model": model_name,
                    **metrics
                })

                print(
                    f"{model_name} Accuracy:"
                    f" {metrics['accuracy']:.4f}"
                )

        leaderboard_df = pd.DataFrame(
            leaderboard
        )

        leaderboard_df.to_csv(
            f"{self.model_dir}/model_scores.csv",
            index=False
        )

        print("\nLeaderboard Saved")
        print(
            f"{self.model_dir}/model_scores.csv"
        )

        print("\nTraining Completed Successfully")


if __name__ == "__main__":

    trainer = ModelTrainer()
    trainer.train()