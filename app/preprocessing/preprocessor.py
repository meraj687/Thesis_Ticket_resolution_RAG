import re
import pandas as pd


class TicketPreprocessor:
    """
    Preprocess SAP MDG support ticket data.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def validate(self):
        """Print dataset statistics."""
        print("\n========== DATA VALIDATION ==========")
        print(f"Rows    : {self.df.shape[0]}")
        print(f"Columns : {self.df.shape[1]}")

        print("\nMissing Values:")
        print(self.df.isnull().sum())

        print("\nDuplicate Rows:")
        print(self.df.duplicated().sum())

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self

    def remove_missing(self):
        self.df = self.df.dropna()
        return self

    @staticmethod
    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def preprocess(self):
        self.df["clean_description"] = self.df["description"].apply(self.clean_text)
        return self.df