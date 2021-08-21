from abc import ABC, abstractmethod
from typing import List

from infrastructure.creator_model.abstract import BaseModel

from service.data_models import NewsClusterData
from service.data_models import InputNews
from service.data_models import GeneratedHeader


class HeaderCreator(ABC):

    @abstractmethod
    def __init__(self):
        pass


class InterfaxHeaderCreator(HeaderCreator):

    def __init__(self, header_model: BaseModel):
        self.header_model = header_model

    def create_cluster_header(self, input_data: List) -> GeneratedHeader:
        """
        Main service function to generate cluster header
        :param input_news:
        :return:
        """
        news_list = self._parse_input(input_data)
        created_headers = self.header_model.inference_model(news_list)
        created_header = created_headers[0]
        header = self._serialize_output(created_header)
        return header

    def _parse_input(self, input_data: List):
        """
        Preprocess input if it's needed
        :param some_input:
        :return:
        """
        news_texts = [i['body'] for i in input_data]
        return news_texts


    def _call_some_infrastructure_model(self):
        """
        Call model from infrastructure
        :return:
        """
        pass

    @staticmethod
    def _serialize_output(header_text: str) -> GeneratedHeader:
        generated_header = GeneratedHeader(header=header_text)
        return generated_header
