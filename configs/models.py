class TfidfConfig:
    encoder_path: str = "model_files/tfidf"


class BertConfig:
    max_len: int = 512
    device: str = 'cpu'
    tokenizer_name: str = 'DeepPavlov/rubert-base-cased-sentence'
    model_path: str = 'model_files/model_100'
