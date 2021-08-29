from abc import *
from Word2VecWrapper import Word2VecWrapper
from gensim.models import KeyedVectors


class BaseNlpModel(metaclass=ABCMeta):
    def __init__(self, *, word2vec_model: Word2VecWrapper, article: KeyedVectors, paragraph: KeyedVectors):
        self.__word2vec = word2vec_model
        self.__article = article
        self.__paragraph = paragraph

    @abstractmethod
    def search(self, text, size):
        pass

    @abstractmethod
    def article(self, key, size):
        pass

    @abstractmethod
    def paragraph(self, key, size):
        pass

