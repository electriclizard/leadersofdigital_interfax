from abc import ABC, abstractmethod
from typing import List


class BaseModel(ABC):

    @abstractmethod
    def __init__(self):
        """
        Initialize model path or som input parameters
        """
        pass

    @abstractmethod
    def inference_model(self, model_input: List[str]):
        """
        Make a model nference
        :return:
        """
        pass


class DummyModel(BaseModel):

    def __init__(self):
        pass

    def inference_model(self, model_input=None):
        header_tokens = [
            'Россия', 'лучшая', 'страна', 'в мире',
            'Путен', 'наш', 'президент'
        ]
        return header_tokens
