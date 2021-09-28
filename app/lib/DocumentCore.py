from gensim.models import KeyedVectors

from app.lib.Word2VecWrapper import Word2VecWrapper
from app.lib.BaseNlpModel import BaseNlpModel
from app.lib.ArticleModel import ArticleModel
from app.lib.ParagraphModel import ParagraphModel


class Core:
    def __init__(self):
        word2vec: Word2VecWrapper = Word2VecWrapper("./build/w2v.model")

        articleVector: KeyedVectors = KeyedVectors.load("./build/article_model.kv")
        paragraphVector: KeyedVectors = KeyedVectors.load("./build/paragraph_model.kv")

        self.__article: BaseNlpModel = ArticleModel(
            word2vec_model=word2vec, article=articleVector, paragraph=paragraphVector
        )
        self.__paragraph: BaseNlpModel = ParagraphModel(
            word2vec_model=word2vec, article=articleVector, paragraph=paragraphVector
        )

    @property
    def article(self):
        return self.__article

    @property
    def paragraph(self):
        return self.__paragraph
