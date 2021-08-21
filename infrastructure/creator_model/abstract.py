from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def __init__(self):
        """
        Initialize model path or som input parameters
        """
        pass

    @abstractmethod
    def inference_model(self, model_input=None):
        """
        Make a model nference
        :return:
        """
        pass


class DummyModel(BaseModel):

    def __init__(self):
        pass

    def inference_model(self, model_input=None):
        import random
        header_tokens = [
            'Россия', 'лучшая', 'страна', 'в мире',
            'Путен', 'наш', 'президент'
        ]
        random_sequence = random.sample(header_tokens, 3)
        return "".join(random_sequence)