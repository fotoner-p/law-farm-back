import os
import json
import gensim

# os.chdir('../')

from app.lib.DocumentCore import Core


core = Core()

with open('./app/build/all_statutes.json', 'r') as f:
    statute_data: dict = json.load(f)


statute_list = []
statute_weights = []

for statute in statute_data:
    if 'articles' not in statute.keys():
        continue

    articles = statute["articles"]

    doc2vec = None
    count = 0

    for article in articles:
        try:
            cur_vec = core.articleVector.get_vector(article["fullname"])
        except:
            continue

        if doc2vec is None:
            doc2vec = cur_vec
        else:
            doc2vec = doc2vec + cur_vec

        count += 1

    if count == 0:
        continue

    statute_list.append(statute["fullname"])
    statute_weights.append(doc2vec / count)

statute_model = gensim.models.KeyedVectors(vector_size=100)
statute_model.add_vectors(weights=statute_weights, keys=statute_list)
statute_model.save("./build/statute_model.kv")


