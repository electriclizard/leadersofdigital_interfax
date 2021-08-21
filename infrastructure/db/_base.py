from abc import abstractmethod
from typing import List


class DB:
    """
    Должен быть метод инициализации базы данных - чтение из файла 200 кластеров


    """
    name = None
    _registry = {}

    def __init__(self, config: dict = None):
        self.config = config or {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if cls.name:
            cls._registry[cls.name] = cls

    @classmethod
    def factory(cls, name, config):
        return cls._registry[name](config)

    @abstractmethod
    def get_one(self, start):
        pass

    @abstractmethod
    def get_many(self, start, number):
        pass

    @abstractmethod
    def insert_one(self, doc: dict):
        pass

    @abstractmethod
    def insert_many(self, docs: List[dict]):
        pass
