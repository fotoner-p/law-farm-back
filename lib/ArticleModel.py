from lib.BaseNlpModel import BaseNlpModel


class ArticleModel(BaseNlpModel):
    def article(self, key, size):
        return self._article.similar_by_key(key, topn=size)

    def paragraph(self, key, size):
        cur_vector = self._article.get_vector(key)
        return self._paragraph.similar_by_vector(cur_vector, topn=size)

    def search(self, text, size):
        cur_vector = self._word2vec.vectorize_text(text)
        return self._article.similar_by_vector(cur_vector, topn=size)