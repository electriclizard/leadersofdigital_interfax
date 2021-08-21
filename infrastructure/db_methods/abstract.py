from abc import ABC, abstractmethod


class DataBase(ABC):

    @abstractmethod
    def __init__(self):
        """
        Init connection to db or smth like that
        """
        pass

    @abstractmethod
    def _make_connection(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def write_entity(self, entity):
        """
        Save smth to db
        :return:
        """
        pass
