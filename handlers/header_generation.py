from service.header_generator import InterfaxHeaderCreator


def create_dummy_header_service():
    from infrastructure.creator_model.abstract import DummyModel

    header_model = DummyModel()
    header_service = InterfaxHeaderCreator(header_model)
    return header_service

  
def create_ngram_service():
    from infrastructure.creator_model.models import NgrammModel

    header_model = NgrammModel()
    header_service = InterfaxHeaderCreator(header_model)
    return header_service


def create_tfidf_service():
    from infrastructure.creator_model.models import TfidfModel
    from configs.models import TfidfConfig

    header_model = TfidfModel(
        encoder_path=TfidfConfig.encoder_path
    )
    header_service = InterfaxHeaderCreator(header_model)
    return header_service


def create_bert_service():
    from infrastructure.creator_model.models import BertModel
    from configs.models import BertConfig

    header_model = BertModel(
        max_len=BertConfig.max_len,
        device=BertConfig.device,
        tokenizer_name=BertConfig.tokenizer_name,
        model_path=BertConfig.model_path
    )
    header_service = InterfaxHeaderCreator(header_model)
    return header_service