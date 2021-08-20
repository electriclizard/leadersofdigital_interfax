from abc import ABC, abstractmethod

from service.data_models import NewsClusterData
from service.data_models import InputNews
from service.data_models import GeneratedHeader


class HeaderCreator(ABC):

    @abstractmethod
    def __init__(self):
        pass


class InterfaxHeaderCreator(HeaderCreator):

    def __init__(self):
        pass

    def create_cluster_header(self, input_news: NewsClusterData) -> GeneratedHeader:
        """
        Main service function to generate cluster header
        :param input_news:
        :return:
        """
        pass

    def _parse_input(self, some_input):
        """
        Preprocess input if it's needed
        :param some_input:
        :return:
        """
        pass

    def _call_some_infrastructure_model(self):
        """
        Call model from infrastructure
        :return:
        """
        pass