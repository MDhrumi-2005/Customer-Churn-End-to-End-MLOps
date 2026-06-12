import os
import yaml
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
from sklearn.model_selection import GridSearchCV

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


def load_params(path="config/params.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)


class ModelTrainer:

    def __init__(self):

        self.artifact_dir = "artifacts/feature_engineering"
        self.model_dir = "models"

        os.makedirs(self.model_dir, exist_ok=True)

    def evaluate_model(self, model, X_test, y_test):

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        precision = precision_score(
            y_test,
            y_pred,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            y_pred,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            y_pred,
            zero_division=0
        )

        try:
            y_prob = model.predict_proba(X_test)[:, 1]

            roc_auc = roc_auc_score(
                y_test,
                y_prob
            )

        except Exception:
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

        # ---------------------------------------
        # Load Data
        # ---------------------------------------

        X_train = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "X_train.csv"
            )
        )

        X_test = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "X_test.csv"
            )
        )

        y_train = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "y_train.csv"
            )
        ).squeeze()

        y_test = pd.read_csv(
            os.path.join(
                self.artifact_dir,
                "y_test.csv"
            )
        ).squeeze()

        print("\nData Loaded Successfully")

        # ---------------------------------------
        # Load Config
        # ---------------------------------------

        params = load_params()

        print("Configuration Loaded Successfully")

        # ---------------------------------------
        # Models
        # ---------------------------------------

        models = {

            "RandomForest": RandomForestClassifier(
                random_state=42
            ),

            "XGBoost": XGBClassifier(
                random_state=42,
                eval_metric="logloss"
            ),

            "LightGBM": LGBMClassifier(
                random_state=42,
                verbose=-1
            )
        }

        # ---------------------------------------
        # Parameter Grids
        # ---------------------------------------

        param_grids = {

            "RandomForest":
                params["random_forest"],

            "XGBoost":
                params["xgboost"],

            "LightGBM":
                params["lightgbm"]
        }

        leaderboard = []

        # ---------------------------------------
        # MLflow Experiment
        # ---------------------------------------

        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment(
            "Customer_Churn"
        )

        # ---------------------------------------
        # Train Models
        # ---------------------------------------

        for model_name, model in models.items():

            print("\n" + "=" * 60)
            print(f"TRAINING {model_name}")
            print("=" * 60)

            with mlflow.start_run(
                run_name=model_name
            ):

                grid_search = GridSearchCV(
                    estimator=model,
                    param_grid=param_grids[
                        model_name
                    ],
                    cv=params["cv_folds"],
                    scoring=params[
                        "selection_metric"
                    ],
                    n_jobs=-1,
                    verbose=2
                )

                grid_search.fit(
                    X_train,
                    y_train
                )

                best_model = (
                    grid_search.best_estimator_
                )

                print(
                    f"\nBest Parameters for "
                    f"{model_name}"
                )

                print(
                    grid_search.best_params_
                )

                metrics = self.evaluate_model(
                    best_model,
                    X_test,
                    y_test
                )

                # --------------------------------
                # MLflow Logging
                # --------------------------------

                mlflow.log_params(
                    grid_search.best_params_
                )

                mlflow.log_param(
                    "cv_folds",
                    params["cv_folds"]
                )

                mlflow.log_param(
                    "selection_metric",
                    params[
                        "selection_metric"
                    ]
                )

                mlflow.log_metrics(
                    metrics
                )

                # --------------------------------
                # Save Model
                # --------------------------------

                model_path = os.path.join(
                    self.model_dir,
                    f"{model_name}.pkl"
                )

                joblib.dump(
                    best_model,
                    model_path
                )

                mlflow.log_artifact(
                    model_path
                )

                mlflow.sklearn.log_model(
                    best_model,
                    artifact_path=model_name
                )

                leaderboard.append({

                    "model":
                        model_name,

                    "accuracy":
                        metrics[
                            "accuracy"
                        ],

                    "precision":
                        metrics[
                            "precision"
                        ],

                    "recall":
                        metrics[
                            "recall"
                        ],

                    "f1_score":
                        metrics[
                            "f1_score"
                        ],

                    "roc_auc":
                        metrics[
                            "roc_auc"
                        ]
                })

                print(
                    f"Accuracy : "
                    f"{metrics['accuracy']:.4f}"
                )

                print(
                    f"F1 Score : "
                    f"{metrics['f1_score']:.4f}"
                )

                print(
                    f"ROC AUC : "
                    f"{metrics['roc_auc']:.4f}"
                )

        # ---------------------------------------
        # Save Leaderboard
        # ---------------------------------------

        leaderboard_df = pd.DataFrame(
            leaderboard
        )

        leaderboard_df = (
            leaderboard_df.sort_values(
                by="roc_auc",
                ascending=False
            )
        )

        leaderboard_path = os.path.join(
            self.model_dir,
            "model_scores.csv"
        )

        leaderboard_df.to_csv(
            leaderboard_path,
            index=False
        )

        print("\n" + "=" * 60)
        print("FINAL LEADERBOARD")
        print("=" * 60)

        print(
            leaderboard_df
        )

        print(
            f"\nLeaderboard Saved:"
            f"\n{leaderboard_path}"
        )

        print(
            "\nMODEL TRAINING "
            "COMPLETED SUCCESSFULLY"
        )


if __name__ == "__main__":

    trainer = ModelTrainer()

    trainer.train()