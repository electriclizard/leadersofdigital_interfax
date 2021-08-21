import re
from typing import List, Tuple
from collections import Counter
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

from infrastructure.creator_model.abstract import BaseModel


class NgrammModel(BaseModel):

    def __init__(self):
        self.ngram_range = (3, 6)

    def inference_model(self, model_input=List[str]) -> List:
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
        return counter.most_common()[:20]


class TfidfModel(BaseModel):

    def __init__(self, encoder_path: str, ngram_range=(3, 4), max_features=10000):
        self.encoder_path = encoder_path
        self.tfidf = TfidfVectorizer(ngram_range=(3, 4), max_features=100000).fit(None)
        pass

    def load_model(self):
        model = pickle.load(open(self.encoder_path, 'wb'))
        return model

    def inference_model(self, model_input=List[str]):
        generated_headers = self.tfidf_generate(model_input)
        return generated_headers

    def tfidf_generate(self, news: List[str]) -> List:
        indexes = (-self.tfidf.transform(news).sum(axis=0)).argsort()[0, :20].tolist()[0]
        res = []
        for i in indexes:
            res.append(self.tfidf.get_feature_names()[i])
        return res
