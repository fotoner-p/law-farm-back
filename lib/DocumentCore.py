from konlpy.tag import Mecab
from gensim.models import KeyedVectors, Word2Vec


class Core:
    def __init__(self):
        self.word2vec_model: Word2Vec = Word2Vec.load("./build/w2v.model")
        self.article_model: KeyedVectors = KeyedVectors.load("./build/article_model.kv")
        self.paragraph_model: KeyedVectors = KeyedVectors.load("./build/paragraph_model.kv")
        self.word_keys = self.word2vec_model.wv.key_to_index.keys()
        self.nlp = Mecab()

    def parse_text(self, text: str):
        result = [item[0] + "/" + item[1] for item in self.nlp.pos(text)]

        return result

    def vectorize_text(self, text: str):
        doc2vec = None
        parse_result = self.parse_text(text)

        count = 0
        for word in parse_result:
            if word in self.word_keys:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = self.word2vec_model.wv.get_vector(word)
                else:
                    doc2vec = doc2vec + self.word2vec_model.wv.get_vector(word)

        return doc2vec / count if doc2vec is not None else None

    def search_paragraph(self, text, size):
        cur_vector = self.vectorize_text(text)
        return self.paragraph_model.similar_by_vector(cur_vector, topn=size)

    def search_article(self, text, size):
        cur_vector = self.vectorize_text(text)
        return self.article_model.similar_by_vector(cur_vector, topn=size)

    def relate_paragraph(self, key, size):
        return self.paragraph_model.similar_by_key(key, topn=size)

    def relate_article(self, key, size):
        return self.article_model.similar_by_key(key, topn=size)

    def article_to_paragraph(self, key, size):
        cur_vector = self.article_model.get_vector(key)
        return self.paragraph_model.similar_by_vector(cur_vector, topn=size)

    def paragraph_to_article(self, key, size):
        cur_vector = self.paragraph_model.get_vector(key)
        return self.article_model.similar_by_vector(cur_vector, topn=size)

