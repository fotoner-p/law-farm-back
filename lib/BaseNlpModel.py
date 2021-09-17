from abc import *
from gensim.models import KeyedVectors

from lib.Word2VecWrapper import Word2VecWrapper


class BaseNlpModel(metaclass=ABCMeta):
    def __init__(self, *, word2vec_model: Word2VecWrapper, article: KeyedVectors, paragraph: KeyedVectors):
        self._word2vec = word2vec_model
        self._article = article
        self._paragraph = paragraph

    @abstractmethod
    def search(self, text, size):
        pass

    @abstractmethod
    def article(self, key, size):
        pass

    @abstractmethod
    def paragraph(self, key, size):
        pass

