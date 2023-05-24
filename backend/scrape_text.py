from bs4 import BeautifulSoup
import requests
import re


def extract_article(soup):
    text = [p.text for p in soup.find_all('p')]
    return '\n'.join(text)


url = "https://www.news247.gr/politismos/tina-turner-i-schesi-tis-me-ton-david-bowie-kai-i-nychta-poy-ektoxeythike-i-kariera-tis.10055585.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_text = extract_article(soup)

print(article_text)
