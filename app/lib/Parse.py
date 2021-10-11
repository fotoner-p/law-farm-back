import marko
import re
from bs4 import BeautifulSoup


def parse_md(md_str: str) -> str:
    html = marko.convert(md_str)
    soup = BeautifulSoup(html, 'html.parser')
    parse = re.sub('[~]', '', soup.text)
    parse = re.sub('[\n]', ' ', parse)

    return parse