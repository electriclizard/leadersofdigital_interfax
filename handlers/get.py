from handlers.header_generation import create_dummy_header_service
from handlers.header_generation import create_ngram_service
from handlers.header_generation import create_tfidf_service


handlers = {
    "dummy_header": create_dummy_header_service(),
    "ngram_header": create_ngram_service(),
    "tf_idf_header": create_tfidf_service()
}


def get_service(service_name: str):
    handler = handlers.get(service_name, None)
    return handler
