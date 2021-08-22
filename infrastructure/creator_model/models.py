import re
from typing import List, Tuple
from collections import Counter
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import EncoderDecoderModel, BertTokenizerFast
import torch
import razdel

from infrastructure.creator_model.abstract import BaseModel


class NgrammModel(BaseModel):

    def __init__(self):
        self.ngram_range = (3, 6)

    def inference_model(self, model_input: List[str]) -> List:
        most_popular_headers = self.most_popular_ngram(
            news=model_input,
            ngram_range=self.ngram_range
        )
        return most_popular_headers

    @staticmethod
    def most_popular_ngram(news: List[str], ngram_range: Tuple) -> List:
        counter = Counter()
        for n in news:
            tokens = [token for token in re.findall(r'\w+', n)]
            for ngram in range(ngram_range[0], ngram_range[-1]+1):
                for i in range(len(tokens)-ngram):
                    counter[' '.join(tokens[i:i+ngram])] += 1
        return [i[0] for i in counter.most_common()[:20]]


class TfidfModel(BaseModel):

    def __init__(self, encoder_path: str, ngram_range=(3, 4), max_features=10000):
        self.encoder_path = encoder_path
        self.tfidf_encoder = self.load_model()

    def load_model(self):
        model = pickle.load(open(self.encoder_path, 'rb'))
        return model

    def inference_model(self, model_input: List[str]):
        generated_headers = self.tfidf_generate(model_input)
        return generated_headers

    def tfidf_generate(self, news: List[str]) -> List:
        indexes = (-self.tfidf_encoder.transform(news).sum(axis=0)).argsort()[0, :20].tolist()[0]
        res = []
        for i in indexes:
            res.append(self.tfidf_encoder.get_feature_names()[i])
        res = res if res != [] else [None]
        return res


class BertModel(BaseModel):

    def __init__(
            self,
            max_len: int = 512,
            device: str = 'cpu',
            tokenizer_name: str = 'DeepPavlov/rubert-base-cased-sentence',
            model_path: str = 'model_files/model_100/'
    ):
        self.max_len = max_len
        self.device = device
        self.tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name)
        self.model = EncoderDecoderModel.from_pretrained(model_path)
        self.model.to(device)
        self.model.eval()

    def inference_model(self, model_input: List[str]):
        news = self.preprocess_inputs(model_input)
        out = self.model.generate(
            input_ids=news,
            decoder_start_token_id=101, num_beams=5, num_return_sequences=5)
        output = [self.tokenizer.decode(out[i], skip_special_tokens=True) for i in range(5)]

        return output

    def preprocess_inputs(self, texts: List[str]) -> torch.Tensor:
        news_batch = ' '.join([' '.join([s.text for s in list(razdel.sentenize(n))[2:4]]) for n in texts])
        news = torch.tensor(
            self.tokenizer.encode(
                news_batch,
                max_length=self.max_len,
                padding="max_length",
                truncation=True
            )
        )
        news = news.unsqueeze(0).to(self.device)
        return news
