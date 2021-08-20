from dataclasses import dataclass
from typing import List


@dataclass()
class InputNews:
    news_text: str


@dataclass()
class NewsClusterData:
    input_news: List[InputNews]


@dataclass
class GeneratedHeader:
    header: str
