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

    header_model = TfidfModel()
    header_service = InterfaxHeaderCreator(header_model)
    return header_service
