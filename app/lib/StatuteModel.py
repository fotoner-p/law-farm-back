from app.lib.BaseNlpModel import BaseNlpModel
import numpy as np


class StatuteModel(BaseNlpModel):
    @staticmethod
    def __reform_result(result, size, documents):
        reform_result = []
        count = 0

        for data in result:
            if data[0] in documents:
                documents.remove(data[0])
            else:
                reform_result.append(data)
                count += 1

            if count == size:
                break

        return reform_result

    def __documents2vec(self, documents):
        doc2vec = None
        count = 0

        for doc in documents:
            cur_vector = self._article.get_vector(doc)
            count += 1

            if doc2vec is None:
                doc2vec = cur_vector
            else:
                doc2vec = doc2vec + cur_vector * np.exp(-count * 0.1)  # 지수 분포 반영

        return doc2vec / count

    def article(self, key, size):
        cur_vector = self._statute.get_vector(key)
        return self._article.similar_by_vector(cur_vector, topn=size)

    def paragraph(self, key, size):
        cur_vector = self._statute.get_vector(key)
        return self._paragraph.similar_by_vector(cur_vector, topn=size)

    def search(self, text, size):
        cur_vector = self._word2vec.vectorize_text(text)
        return self._paragraph.similar_by_vector(cur_vector, topn=size)

    def statute(self, key, size):
        return self._statute.similar_by_key(key, topn=size)

    def keyword(self, key, size):
        cur_vector = self._statute.get_vector(key)
        return self._word2vec.keyword(cur_vector, size)

    def recommend(self, documents, size, duplicate):
        doc2vec = self.__documents2vec(documents)

        return self._statute.similar_by_vector(doc2vec, topn=size)

    def combined_recommend(self, documents, size, duplicate):
        log2vec = self.__documents2vec(documents["log"])
        bookmark2vec = self.__documents2vec(documents["bookmark"])

        doc2vec = bookmark2vec * 0.5 + log2vec * 0.5
        return self._statute.similar_by_vector(doc2vec, topn=size)

    def inference_statute(self, text, size):
        cur_vector = self._word2vec.vectorize_text(text)
        return self._statute.similar_by_vector(cur_vector, topn=size)
