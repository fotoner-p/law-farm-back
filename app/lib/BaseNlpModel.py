from abc import *
import numpy as np
from gensim.models import KeyedVectors

from app.lib.Word2VecWrapper import Word2VecWrapper


class BaseNlpModel(metaclass=ABCMeta):
    def __init__(self, *, word2vec_model: Word2VecWrapper, article: KeyedVectors, paragraph: KeyedVectors, statute: KeyedVectors):
        self._word2vec = word2vec_model
        self._article = article
        self._paragraph = paragraph
        self._statute = statute

    @abstractmethod
    def search(self, text, size):
        pass

    @abstractmethod
    def article(self, key, size):
        pass

    @abstractmethod
    def paragraph(self, key, size):
        pass

    @abstractmethod
    def statute(self, key, size):
        pass

    @abstractmethod
    def recommend(self, documents, size, duplicate):
        pass

