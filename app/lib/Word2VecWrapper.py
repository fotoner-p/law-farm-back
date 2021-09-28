from konlpy.tag import Mecab
from gensim.models import Word2Vec


class Word2VecWrapper:
    def __init__(self, path: str):
        self.__word2vec: Word2Vec = Word2Vec.load(path)

        self.__word_keys = self.__word2vec.wv.key_to_index.keys()
        self.__nlp = Mecab()

    def __parse_text(self, text: str):
        result = [item[0] + "/" + item[1] for item in self.__nlp.pos(text)]

        return result

    def vectorize_text(self, text: str):
        doc2vec = None
        parse_result = self.__parse_text(text)

        count = 0
        for word in parse_result:
            if word in self.__word_keys:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = self.__word2vec.wv.get_vector(word)
                else:
                    doc2vec = doc2vec + self.__word2vec.wv.get_vector(word)

        return doc2vec / count if doc2vec is not None else None
