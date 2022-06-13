import os
from pathlib import Path


class BaseConfig:
    BASE_PATH = os.fspath(Path(__file__).resolve().parent.parent)

    YA_MAPS_API_KEY: str
