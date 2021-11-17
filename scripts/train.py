# -*- coding: utf-8 -*-
"""project-final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KukBVu5LsyJDHXLENqOZMCtTcv5ZLiX_

# 필수 라이브러리설치
"""

# !pip
# install
# git
# !git clone https: // github.com / SOMJANG / Mecab - ko -for -Google - Colab.git
#     !bash
#     Mecab - ko -
#     for -Google - Colab / install_mecab - ko_on_colab190912.sh

# !apt - qq - y install fonts - nanum

"""# 데이터 전처리"""

from konlpy.tag import Mecab
import pandas as pd

import gensim
from tensorflow.keras.preprocessing.text import Tokenizer
from gensim.models.word2vec import Word2Vec
import json

df = pd.read_json('../app/build/all_paragraphs.json')
texts = df['text'].tolist()
nlp = Mecab()


def preprocess(content: list):
    re_content = []
    for item in content:
        re_str = item
        result = [item[0] + "/" + item[1] for item in nlp.pos(re_str)]
        result_str = " ".join(result)
        re_content.append(result_str)

    return re_content


texts = preprocess(texts)

vocab_size = 30000
tokenizer = Tokenizer(vocab_size)
tokenizer.fit_on_texts(texts)

tokenizer_json = tokenizer.to_json()
with open('../app/build/tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))

texts_sequences = tokenizer.texts_to_sequences(texts)

content_length = []
for arr in texts_sequences:
    content_length.append(len(arr))

# 컨텐츠 길이

# content_max_len = max(content_length)
# content_max_len = 300 # 길이기 2500이 넘어가는 이상치 존재, 평균적으로는 그보다 한참 밑
# title_max_len = max(title_length)
# print(title_max_len)

max(content_length)
sum(content_length) / len(content_length)

texts = [text.split(' ') for text in texts]

w2v_model = Word2Vec(sentences=texts, vector_size=100, window=4, min_count=0, workers=4, epochs=80)
w2v_model.save("./build/w2v.model")
# w2v_model.save("./build/proto")=
# w2v_model.wv.save_word2vec_format("./build/w2v")



# !python3 - m gensim.scripts.word2vec2tensor - -input. / build / proto - -output. / build / proto


def vectors(document_list):
    document_embedding_list = []

    # 각 문서에 대해서
    for line in document_list:
        doc2vec = None
        count = 0
        for word in line:
            if word in w2v_model.wv.key_to_index.keys():
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = w2v_model.wv.get_vector(word)
                else:
                    doc2vec = doc2vec + w2v_model.wv.get_vector(word)

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list


document_embedding_list = vectors(texts)
print('문서 벡터의 수 :', len(document_embedding_list))

paragraph_model = gensim.models.KeyedVectors(vector_size=100)
paragraph_model.add_vectors(weights=document_embedding_list, keys=df['fullname'].tolist())
paragraph_model.save("./build/paragraph_model.kv")


with open('../app/build/all_paragraphs.json', 'r') as f:
    paragraph_data: dict = json.load(f)

paragraph_data = {
    paragraph['fullname']: {
        'statute': paragraph['statute'],
        'article': paragraph['article'],
        'paragraph': paragraph['paragraph'],
        'text': paragraph['text'],
    } for paragraph in paragraph_data
}

with open('../app/build/all_statutes.json', 'r') as f:
    statute_data: dict = json.load(f)

article_list = []
article_weights = []
article_text = dict()
article_type = dict()
for statute in statute_data:
    if 'articles' not in statute.keys():
        continue

    for article in statute['articles']:
        doc2vec = None

        article_text[article['fullname']] = article['text']
        article_type[article['fullname']] = article['type']

        count = 0
        if 'paragraphs' not in article.keys():
            words = preprocess([article['text']])[0].split(' ')

            for word in words:
                if word in w2v_model.wv.key_to_index.keys():
                    count += 1
                    # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                    if doc2vec is None:
                        doc2vec = w2v_model.wv.get_vector(word)
                    else:
                        doc2vec = doc2vec + w2v_model.wv.get_vector(word)

        else:
            for paragraph in article['paragraphs']:
                paragraph_key = paragraph['fullname']
                if paragraph_key in paragraph_model.key_to_index.keys():
                    count += 1
                    # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                    if doc2vec is None:
                        doc2vec = paragraph_model[paragraph_key]
                    else:
                        doc2vec = doc2vec + paragraph_model[paragraph_key]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            article_list.append(article['fullname'])
            article_weights.append(doc2vec)

article_model = gensim.models.KeyedVectors(vector_size=100)
article_model.add_vectors(weights=article_weights, keys=article_list)
article_model.save("./build/article_model.kv")