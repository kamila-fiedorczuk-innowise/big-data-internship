import json
from pathlib import Path


class JsonReader:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        try:
            with open(self.path, mode="r", encoding="utf-8") as file:
                json_data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {self.path.resolve()}") from e
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in {self.path.name}: {e.msg} "
                f"(line {e.lineno}, column {e.colno})"
            ) from e

        if not isinstance(json_data, list):
            raise ValueError(
                f"Expected a list of records in {self.path.name}, "
                f"got {type(json_data).__name__}"
            )
        return json_data

