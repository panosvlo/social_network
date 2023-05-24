from celery import shared_task, chain
from .models import User, Post, Article, Topic
import requests
import random
import string
from bs4 import BeautifulSoup
import re
from time import sleep
import lxml

API_BASE_URL = "http://localhost:8000"


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_bot_account(topic):
    username = f"{topic['name']}_bot"
    email = f"{username}@example.com"
    password = generate_password()

    # Check if the user already exists
    user_exists = User.objects.filter(username=username).exists()

    # if user_exists:
    #     print(f"Bot account for topic '{topic['name']}' with username '{username}' already exists. Skipping.")
    if not user_exists:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.topics_of_interest.add(topic['id'])
        user.save()

        print(f"Created bot account for topic '{topic['name']}' with username '{username}'")


def google_news(topic):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 "
            "Safari/537.36"
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
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 "
            "Safari/537.36 Edge/18.19582"
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


@shared_task()
def create_bots_for_all_topics():
    response = requests.get("http://localhost:8000/api/topics/")
    print(response.json())
    topics = response.json()

    for topic in topics:
        create_bot_account(topic)


@shared_task()
def bot_posts():
    # Fetch all bot accounts
    bots = User.objects.filter(username__contains='_bot')

    for bot in bots:
        # Fetch articles for each topic the bot is interested in
        for topic in bot.topics_of_interest.all():
            # Fetch saved articles for the topic
            articles = Article.objects.filter(topic=topic)

            # If there are no articles for this topic, continue to the next topic
            if not articles:
                continue

            # Randomly select an article
            article = random.choice(articles)

            # Check for existing posts with the same URL
            existing_post = Post.objects.filter(content=article.url).first()

            # If there is no existing post with the same URL, create a new post
            if existing_post is None:
                post_content = f'{article.title}\n{article.url}'
                post = Post(user=bot, content=post_content, topic=topic)
                post.save()

                # Delete the article from the database
                article.delete()

                print(f"Created post for bot '{bot.username}' with content '{post_content}'")
            else:
                print(f"Skipped duplicate post for bot '{bot.username}' with content '{article.url}'")


@shared_task()
def save_articles_to_database(*args):
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


@shared_task()
def delete_all_articles():
    # Get all articles
    articles = Article.objects.all()

    # Delete all articles
    articles.delete()

    print("All articles have been deleted.")


@shared_task
def delete_all_articles_and_search_again():
    chain(delete_all_articles.s(), save_articles_to_database.s())()
