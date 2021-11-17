from gensim.models import KeyedVectors

from app.lib.Word2VecWrapper import Word2VecWrapper
from app.lib.BaseNlpModel import BaseNlpModel
from app.lib.ArticleModel import ArticleModel
from app.lib.ParagraphModel import ParagraphModel
from app.lib.StatuteModel import StatuteModel


class Core:
    def __init__(self):
        word2vec: Word2VecWrapper = Word2VecWrapper("./app/build/w2v.model")

        articleVector: KeyedVectors = KeyedVectors.load("./app/build/article_model.kv")
        paragraphVector: KeyedVectors = KeyedVectors.load("./app/build/paragraph_model.kv")
        statuteVector: KeyedVectors = KeyedVectors.load("./app/build/statute_model.kv")

        self.__article: BaseNlpModel = ArticleModel(
            word2vec_model=word2vec, article=articleVector, paragraph=paragraphVector, statute=statuteVector
        )
        self.__paragraph: BaseNlpModel = ParagraphModel(
            word2vec_model=word2vec, article=articleVector, paragraph=paragraphVector, statute=statuteVector
        )
        self.__statute: StatuteModel = StatuteModel(
            word2vec_model=word2vec, article=articleVector, paragraph=paragraphVector, statute=statuteVector
        )

    @property
    def article(self):
        return self.__article

    @property
    def paragraph(self):
        return self.__paragraph

    @property
    def statute(self):
        return self.__statute
