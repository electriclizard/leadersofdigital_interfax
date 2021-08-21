from infrastructure.db_methods.abstract import DataBase

from mongoengine import connect
from mongoengine import Document


class MongoEngineBase(DataBase):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._make_connection()

    def _make_connection(self):
        connect(
            db='header_db',
            username='root',
            password='example',
            host="mongodb://root:example@0.0.0.0:27017/header_db"
        )

    def write_entity(self, entity: Document) -> bool:
        try:
            entity.save()
            return True
        except Exception as err:
            print(f"DB saveing Exception: {err}")
            return False
