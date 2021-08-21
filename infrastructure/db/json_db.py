import json
from typing import List

from infrastructure.db._base import DB


class JsonDB(DB):
    name = "json"

    def __init__(self, config: dict = None):
        super().__init__(config)
        with open(self.config.get('db_path', './data/dataset_public.json')) as f:
            self._db = json.load(f)

    def get_one(self, start):
        return self._db[start]

    def get_many(self, start, number):
        return self._db[start: start + number]

    def insert_one(self, doc: dict):
        self._db.append(doc)

    def insert_many(self, docs: List[dict]):
        self._db.extend(docs)

    def close(self):
        with open(self.config.get(
                'backup_db_path', './data/backup_dataset_public.json'
        ), mode='w') as f:
            json.dump(self._db, f)

    def get_size(self):
        return len(self._db)
