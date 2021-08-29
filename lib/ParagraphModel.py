from BaseNlpModel import BaseNlpModel


class ParagraphModel(BaseNlpModel):
    def article(self, key, size):
        cur_vector = self.__paragraph.get_vector(key)
        return self.__article.similar_by_vector(cur_vector, topn=size)

    def paragraph(self, key, size):
        return self.__paragraph.similar_by_key(key, topn=size)

    def search(self, text, size):
        cur_vector = self.__word2vec.vectorize_text(text)
        return self.__paragraph.similar_by_vector(cur_vector, topn=size)

