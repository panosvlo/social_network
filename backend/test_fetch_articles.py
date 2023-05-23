import os
import django
import requests
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def fetch_articles_urls_for_topic(topic_name, api_key, search_engine_id):
    url = f'https://www.googleapis.com/customsearch/v1?q={topic_name}&cx={search_engine_id}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    article_urls = []

    for item in data['items']:
        article_urls.append(item['link'])

    return article_urls


# tasks.py
from users.models import User, Post

API_KEY = 'AIzaSyD0QLdpamj_gR1CFIO2ReEXPilAWQPVwbs'
SEARCH_ENGINE_ID = '3234e11bf0e0940fb'


def fetch_articles_and_create_posts():
    # Fetch all bot accounts
    bots = User.objects.filter(username__contains='_bot')

    for bot in bots:
        # Fetch articles for each topic the bot is interested in
        for topic in bot.topics_of_interest.all():
            # Fetch article URLs for the topic
            article_urls = fetch_articles_urls_for_topic(topic.name, API_KEY, SEARCH_ENGINE_ID)

            for url in article_urls[:2]:
                print(url)
                print(bot)
                print(topic.name)


if __name__ == '__main__':
    fetch_articles_and_create_posts()
