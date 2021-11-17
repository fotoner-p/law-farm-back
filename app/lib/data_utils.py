import json


def get_paragraph_dict():
    with open('./app/build/all_paragraphs.json', 'r') as f:
        paragraph_data: dict = json.load(f)

    paragraph_data = {
        paragraph['fullname']: {
            'statute': paragraph['statute'],
            'article': paragraph['article'],
            'paragraph': paragraph['paragraph'],
            'text': paragraph['text'],
        } for paragraph in paragraph_data
    }

    return paragraph_data


def get_article_dict():
    with open('./app/build/all_articles.json', 'r') as f:
        article_data: dict = json.load(f)

    article_data = {
        article['fullname']: {
            'statute': article['statute'],
            'article': article['article'],
            'paragraphs': article['paragraphs'] if 'paragraphs' in article else [],
            'text': article['text'],
        } for article in article_data
    }

    return article_data


def get_statues_dict():
    with open('./app/build/all_statutes.json', 'r') as f:
        statute_data: dict = json.load(f)

    statute_data = {
        statute['fullname']: {
            'articles': statute['articles'] if 'articles' in statute else [],
            'text': statute['text'],
        } for statute in statute_data
    }

    return statute_data

# def word_tagging(content: list):
#     re_content = []
#     for item in content:
#         re_str = item
#         result = [item[0] + "/" + item[1] for item in nlp.pos(re_str)]
#         result_str = " ".join(result)
#         re_content.append(result_str)
#
#     return re_content

