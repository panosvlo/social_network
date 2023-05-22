import os
import django
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import lxml
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from users.models import Topic, Article  # import the Article model


def google_news(topic):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    response = requests.get(
        f"https://www.google.com/search?q={topic}&tbm=nws&num=20", headers=headers, cookies=cookies
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []
    for el in soup.select("div.SoaBEf"):
        news_results.append(
            (
                el.find("a")["href"],
                el.select_one("div.MBeuO").get_text(),
            )
        )
    return news_results


def bing_news(topic):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    html = requests.get(f'https://www.bing.com/news/search?q={topic}', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    news_results = []
    for result in soup.select('.card-with-cluster'):
        news_results.append(
            (
                result.select_one('.title')['href'],
                result.select_one('.title').text,
            )
        )
    return news_results


def yahoo_news(search):
    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)
    links = set()

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }

    for x in range(3):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find_all('div', 'NewsArticle')

        for card in cards:
            headline = card.find('h4', 's-title').text
            source = card.find('span', 's-source').text
            posted = card.find('span', 's-time').text.replace('.', '').strip()
            description = card.find('p', 's-desc').text.strip()
            raw_link = card.find('a').get('href')
            unquoted_link = requests.utils.unquote(raw_link)
            pattern = re.compile(r'RU=(.+)\/RK')
            clear_link = re.search(pattern, unquoted_link).group(1)
            links.add(
                (
                    clear_link,
                    headline,
                )
            )

        try:
            url = soup.find('a', 'next').get('href')
            sleep(2)
        except AttributeError:
            break

    return list(links)


search_functions = [google_news, bing_news, yahoo_news]


def save_articles_to_database():
    topics = Topic.objects.all()

    for topic in topics:
        search_function = random.choice(search_functions)
        article_data = search_function(topic.name)
        search_engine_name = search_function.__name__.replace('_news', '')

        for url, title in article_data:
            if len(url) < 2048:
                existing_article = Article.objects.filter(url=url).first()

                if existing_article is None:
                    article = Article(url=url, title=title, topic=topic, source=search_engine_name)
                    article.save()
                    print(f"Saved article with URL '{url}' for topic '{topic.name}' from '{search_engine_name}'")
                else:
                    print(f"Skipped duplicate article with URL '{url}'")


if __name__ == '__main__':
    save_articles_to_database()
