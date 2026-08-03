from pathlib import Path
import pandas as pd


class DataLoader:
    """Loads the SAP MDG ticket dataset."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.file_path}")

        df = pd.read_csv(self.file_path)
        return df