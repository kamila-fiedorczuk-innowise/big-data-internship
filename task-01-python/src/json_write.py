import json
from pathlib import Path


class JsonWriter:
    def __init__(self, path):
        self.path = Path(path)

    def write(self, result):
        self.path.parent.mkdir(exist_ok=True)

        with open(self.path, mode="w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        return self.path