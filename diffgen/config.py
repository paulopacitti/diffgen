import json
from os import makedirs
from os.path import isfile
from pathlib import Path
from pydantic import BaseModel, ValidationError
from typing import Optional
from rich import print


HOME_DIR = Path.home()
CONFIG_DIR_PATH = Path(f"{HOME_DIR}/.config/diffgen")
CONFIG_FILE_PATH = Path(f"{CONFIG_DIR_PATH}/config.json")


class DiffgenConfig(BaseModel):
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    custom_headers: Optional[str] = None


def load_config() -> dict:
    if not isfile(CONFIG_FILE_PATH):
        makedirs(CONFIG_DIR_PATH, exist_ok=True)
        with open(CONFIG_FILE_PATH, "w+") as f:
            initial_config = DiffgenConfig(
                model="default", base_url="http://localhost:8000"
            )
            f.write(initial_config.model_dump_json(indent=4))
    with open(CONFIG_FILE_PATH, "r") as f:
        try:
            config = json.load(f)
            return DiffgenConfig(**config).model_dump()
        except json.JSONDecodeError as e:
            print(
                rf"[red]Invalid JSON in config file. Make sure the configuration is correct in {CONFIG_FILE_PATH}[/]"
            )
            exit(1)
        except ValidationError as e:
            print(
                rf"[red]Invalid config file. Make sure the configuration is correct in {CONFIG_FILE_PATH}[/]"
            )
            exit(1)


# Example usage
if __name__ == "__main__":
    config = load_config()
    print(config.model_dump_json(indent=4))
