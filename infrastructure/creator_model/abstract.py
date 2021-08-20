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
