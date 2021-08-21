def create_header_service():
    from infrastructure.creator_model.abstract import DummyModel
    from service.header_generator import InterfaxHeaderCreator

    header_model = DummyModel()
    header_service = InterfaxHeaderCreator(header_model)
    return header_service


handlers = {
    "random_header": create_header_service()
}


def get_service(service_name: str):
    handler = handlers.get(service_name, None)
    return handler
