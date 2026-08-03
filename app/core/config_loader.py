from pathlib import Path
import yaml


class ConfigLoader:
    """
    Loads YAML configuration files.
    """

    CONFIG_DIR = Path("config")

    @classmethod
    def load(cls, filename: str):
        """
        Load a YAML configuration file.

        Args:
            filename: YAML filename (e.g. categories.yaml)

        Returns:
            dict
        """

        path = cls.CONFIG_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)