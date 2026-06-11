import os
import json
import shutil
import pandas as pd


class ModelSelector:

    def __init__(self):

        self.model_dir = "models"
        self.score_file = os.path.join(
            self.model_dir,
            "model_scores.csv"
        )

    def select_best_model(self):

        print("=" * 50)
        print("MODEL SELECTION STARTED")
        print("=" * 50)

        scores = pd.read_csv(
            self.score_file
        )

        best_model = scores.sort_values(
            by="roc_auc",
            ascending=False
        ).iloc[0]

        best_model_name = best_model["model"]

        print(
            f"\nBest Model: {best_model_name}"
        )

        source_model = os.path.join(
            self.model_dir,
            f"{best_model_name}.pkl"
        )

        destination_model = os.path.join(
            self.model_dir,
            "best_model.pkl"
        )

        shutil.copy(
            source_model,
            destination_model
        )

        metadata = {
            "best_model": best_model_name,
            "accuracy": float(best_model["accuracy"]),
            "precision": float(best_model["precision"]),
            "recall": float(best_model["recall"]),
            "f1_score": float(best_model["f1_score"]),
            "roc_auc": float(best_model["roc_auc"])
        }

        with open(
            os.path.join(
                self.model_dir,
                "best_model_metadata.json"
            ),
            "w"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )

        print(
            "\nBest model saved successfully"
        )

        print(
            "Metadata saved successfully"
        )


if __name__ == "__main__":

    selector = ModelSelector()

    selector.select_best_model()