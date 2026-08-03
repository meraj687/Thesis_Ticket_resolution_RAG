from pathlib import Path
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)
from sklearn.model_selection import train_test_split


class TicketClassifier:

    def __init__(self, dataset_path: str):

        self.dataset_path = Path(dataset_path)

        self.vectorizer = TfidfVectorizer()

        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

    def train(self):

        df = pd.read_csv(self.dataset_path)

        X = df["description"]

        y = df["category"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

        X_train_vec = self.vectorizer.fit_transform(X_train)

        X_test_vec = self.vectorizer.transform(X_test)

        self.model.fit(X_train_vec, y_train)

        predictions = self.model.predict(X_test_vec)

        accuracy = accuracy_score(y_test, predictions)

        print("\nAccuracy:", round(accuracy * 100, 2), "%\n")

        print(classification_report(y_test, predictions))

        Path("models").mkdir(exist_ok=True)

        joblib.dump(
            self.model,
            "models/ticket_classifier.pkl"
        )

        joblib.dump(
            self.vectorizer,
            "models/vectorizer.pkl"
        )

        print("\nModel saved successfully.")