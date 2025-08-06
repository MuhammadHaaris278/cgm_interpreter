import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.path = Path(config_path)
        self.config = self._load_yaml()

        self.app_name = self.config["app"]["name"]
        self.host = self.config["app"]["host"]
        self.port = self.config["app"]["port"]
        self.debug = self.config["app"]["debug"]

        self.llm_model = self.config["llm"]["model"]
        self.llm_base_url = self.config["llm"]["base_url"]
        self.llm_api_key = os.getenv(self.config["llm"]["api_key_env"])

        self.input_dir = Path(self.config["paths"]["input_dir"])
        self.output_dir = Path(self.config["paths"]["interpretation_dir"])
        self.billing_log_dir = Path(self.config["paths"]["billing_log_dir"])

        # Ensure output paths exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.billing_log_dir.mkdir(parents=True, exist_ok=True)

    def _load_yaml(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.path}")
        with open(self.path, "r") as f:
            return yaml.safe_load(f)

    def as_dict(self):
        return self.config