from celery import shared_task, chain
from .models import User, Post, Article, Topic, Comment
import requests
import random
import string
from bs4 import BeautifulSoup
import re
from time import sleep
import lxml
from faker import Faker
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

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
        f"https://www.google.com/search?q={topic}&num=20&lr=lang_en&tbs=lr:lang_1en,qdr:d&tbm=nws&source=lnt",
        headers=headers, cookies=cookies
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

    html = requests.get(f'https://www.bing.com/news/search?q={topic}&setlang=en', headers=headers)
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

    return list(links)


def generate_random_bot_name():
    fake = Faker()
    name = fake.name()
    username = name.replace(" ", "")

    return username


def get_article_text(content):
    def extract_article(soup):
        text = [p.text for p in soup.find_all('p')]
        return '\n'.join(text)

    # Extract URL from the content
    url = re.search(r'(https?://[^\s]+)', content).group(1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = extract_article(soup)
    lines = article_text.split('\n')
    filtered_lines = [line for line in lines if len(line) > 150]
    filtered_text = '\n'.join(filtered_lines)
    return filtered_text


def get_title(content):
    # Extract title from the content
    title = content.split('(')[0].strip()
    return title


def generate_article_comment(article_title, article_text):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2',
                                            pad_token_id=tokenizer.eos_token_id)

    model.to(device)

    text = f"""I just read the below article.\nTitle of the article: {article_title}\nThe content of the article: {article_text}\nWhat I would like to comment on the article is that"""

    tokens = tokenizer.encode(text, truncation=False)
    if len(tokens) <= 1024:
        input_ids = tokenizer.encode(text, return_tensors='pt')

        output = model.generate(input_ids.to(device),
                                max_length=10000,
                                num_beams=1,
                                no_repeat_ngram_size=2,
                                early_stopping=True,
                                num_return_sequences=1)
        gpt_output = tokenizer.decode(output[0], skip_special_tokens=True)
        print(gpt_output)
        gpt_output = gpt_output.split("What I would like to comment on the article is that")
        if len(gpt_output) > 1:
            comment = gpt_output[1].strip()
            return comment
    else:
        return "Could not produce comment, skipping it."


def generate_self_post_comment(content):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2',
                                            pad_token_id=tokenizer.eos_token_id)

    model.to(device)

    text = f"""A user in Facebook made the below post.\n{content}\nAnother user commented on that post:"""

    tokens = tokenizer.encode(text, truncation=False)
    if len(tokens) <= 1024:
        input_ids = tokenizer.encode(text, return_tensors='pt')

        output = model.generate(input_ids.to(device),
                                max_length=10000,
                                num_beams=1,
                                no_repeat_ngram_size=2,
                                early_stopping=True,
                                num_return_sequences=1)
        gpt_output = tokenizer.decode(output[0], skip_special_tokens=True)
        print(gpt_output)
        gpt_output = gpt_output.split("Another user commented on that post:")
        if len(gpt_output) > 1:
            comment = gpt_output[1].strip()
            return comment
    else:
        return "Could not produce comment, skipping it."


search_functions = [google_news, bing_news, yahoo_news]


@shared_task()
def create_bots_for_all_topics():
    response = requests.get("http://localhost:8000/api/topics/")
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
                post_content = f'{article.title}\n (Search source: {article.source}.com news) \n{article.url}'
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
        temp_search_functions = search_functions.copy()
        for x in range(2):
            search_function = random.choice(temp_search_functions)
            # Remove the selected function to ensure it's not chosen in the next iteration
            temp_search_functions.remove(search_function)
            article_data = search_function(topic.name)
            search_engine_name = search_function.__name__.replace('_news', '')

            for url, title in article_data:
                if len(url) < 2048 and 'youtube.com/watch' not in url:
                    existing_article = Article.objects.filter(url=url).first()

                    if existing_article is None:
                        article = Article(url=url, title=title, topic=topic, source=search_engine_name)
                        article.save()
                        print(f"Saved article with URL '{url}' for topic '{topic.name}' from '{search_engine_name}'")
                    else:
                        print(f"Skipped duplicate article with URL '{url}'")

            # If we have done two iterations, reset the temp_search_functions for the next topic
            if x == 1:
                temp_search_functions = search_functions.copy()


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


@shared_task()
def create_random_bots(num_bots=10):
    # Get all topics
    topics = Topic.objects.all()

    for _ in range(num_bots):
        # Generate a random bot name
        bot_name = generate_random_bot_name()

        # Generate a random email
        email = f'{bot_name}@example.com'

        # Generate a random password
        password = bot_name

        # Create the bot account
        user = User.objects.create_user(username=bot_name, email=email, password=password, is_bot=True)

        # Assign the bot to a random subset of the topics
        if len(topics) >= 3:
            num_topics = random.randint(3, len(topics))
        else:
            num_topics = random.randint(1, len(topics))

        chosen_topics = random.sample(list(topics), num_topics)
        user.topics_of_interest.set(chosen_topics)

        user.save()

        print(f"Created bot account with username '{bot_name}'")


@shared_task()
def create_post_from_random_bot():
    # Fetch all bot accounts
    bots = User.objects.filter(is_bot=True)

    if not bots:
        print('No bot users found.')
        return

    # Randomly select a bot
    bot = random.choice(bots)

    # Fetch topics the bot is interested in
    topics = bot.topics_of_interest.all()

    if not topics:
        print(f'Bot user {bot.username} is not following any topics.')
        return

    # Randomly select a topic
    topic = random.choice(topics)

    # Fetch articles for the topic
    articles = Article.objects.filter(topic=topic)

    # If there are no articles for this topic, log it and return
    if not articles:
        print(f'No articles found for topic {topic.name}.')
        return

    # Randomly select an article
    article = random.choice(articles)

    # Check for existing posts with the same URL
    existing_post = Post.objects.filter(content=article.url).first()

    # If there is no existing post with the same URL, create a new post
    if existing_post is None:
        post_content = f'{article.title}\n (Search source: {article.source}.com news) \n{article.url}'
        post = Post(user=bot, content=post_content, topic=topic)
        post.save()

        # Delete the article from the database
        article.delete()

        print(f"Created post for bot '{bot.username}' with content '{post_content}'")
    else:
        print(f"Skipped duplicate post for bot '{bot.username}' with content '{article.url}'")


@shared_task()
def create_comment_from_random_bot():
    # Set the maximum number of comments
    max_comments = 5
    comment_count = 0

    # Fetch all bot accounts
    bots = User.objects.filter(is_bot=True)

    if not bots:
        print('No bot users found.')
        return

    while comment_count < max_comments:
        # Randomly select a bot
        bot = random.choice(bots)

        # Fetch topics the bot is interested in
        topics = bot.topics_of_interest.all()
        # Fetch users the bot is following
        followed_users = bot.following.all()

        if not topics and not followed_users:
            print(f'Bot user {bot.username} is not following any topics or users.')
            continue

        # Fetch posts for the topics within the last 24 hours
        one_day_ago = timezone.now() - timedelta(days=1)
        topic_posts = Post.objects.filter(topic__in=topics, created_at__gte=one_day_ago)
        # Fetch posts from followed users within the last 24 hours
        followed_posts = Post.objects.filter(user__in=followed_users, created_at__gte=one_day_ago)

        # Combine querysets
        posts = topic_posts | followed_posts

        # Remove duplicates, if any
        posts = posts.distinct()

        # If there are no recent posts for this topic, log it and continue
        if not posts:
            print(f'No recent posts found for topics and users followed by {bot.username}.')
            continue

        # Loop through the posts until a post without a comment is found
        for post in posts:
            with transaction.atomic():
                # If the post already has a comment, skip it
                if post.comments.exists():
                    continue

                if "Search source:" not in post.content:
                    comment_text = generate_self_post_comment(post.content)
                else:
                    # Scrape the article text
                    article_text = get_article_text(post.content)

                    # Generate a comment
                    title = get_title(post.content)
                    comment_text = generate_article_comment(title, article_text)

                if comment_text == "Could not produce comment, skipping it.":
                    continue

                # Create the comment
                Comment.objects.create(user=bot, post=post, content=comment_text)

                print(f"Created comment for bot '{bot.username}' on post '{post.id}'")

                comment_count += 1
                if comment_count >= max_comments:
                    return


@shared_task()
def create_like_from_random_bot():
    # Fetch all bot accounts
    bots = User.objects.filter(is_bot=True)

    if not bots:
        print('No bot users found.')
        return

    # Randomly select a bot
    bot = random.choice(bots)

    # Fetch topics the bot is interested in
    topics = bot.topics_of_interest.all()
    # Fetch users the bot is following
    followed_users = bot.following.all()

    if not topics and not followed_users:
        print(f'Bot user {bot.username} is not following any topics or users.')
        return

    # Randomly select a topic
    topic = random.choice(topics)

    # Fetch posts for the topic within the last 24 hours
    one_day_ago = timezone.now() - timedelta(days=1)
    # Fetch posts for the topics within the last 24 hours
    topic_posts = Post.objects.filter(topic__in=topics, created_at__gte=one_day_ago)

    # Fetch posts from followed users within the last 24 hours
    followed_posts = Post.objects.filter(user__in=followed_users, created_at__gte=one_day_ago)

    # Combine querysets
    posts = topic_posts | followed_posts

    # Remove duplicates, if any
    posts = posts.distinct()

    # If there are no recent posts for this topic, log it and return
    if not posts:
        print(f'No recent posts found for topic {topic.name}.')
        return

    # Randomly select a post
    post = random.choice(posts)

    # If the bot already liked this post, skip it
    if post.likes.filter(pk=bot.pk).exists():
        print(f"Bot '{bot.username}' already liked post '{post.id}', skipping.")
        return

    # Add a like from the bot to the post
    post.likes.add(bot)

    print(f"Bot '{bot.username}' liked post '{post.id}'")


@shared_task()
def bot_follow_users(num_users=100):
    # Fetch all bot accounts
    bots = User.objects.filter(is_bot=True)

    if not bots:
        print('No bot users found.')
        return

    # Randomly select a bot
    bot = random.choice(bots)

    # Fetch all non-bot accounts
    users = User.objects.filter(is_bot=False)

    if not users:
        print('No non-bot users found.')
        return

    # Count the number of users the bot is already following
    following_count = bot.following.count()

    # If the bot is already following the maximum number of users, log it and return
    if following_count >= num_users:
        print(f"Bot '{bot.username}' is already following {following_count} users.")
        return

    # Calculate the number of users the bot needs to follow
    num_users_to_follow = 5

    # Filter the non-bot users to only include those not already being followed by the bot
    users_not_followed = users.exclude(id__in=bot.following.values_list('id', flat=True))

    if not users_not_followed:
        print(f"Bot '{bot.username}' is already following all non-bot users.")
        return

    # Randomly select users for the bot to follow, up to the maximum
    users_to_follow = random.sample(list(users_not_followed), min(num_users_to_follow, users_not_followed.count()))
    for user in users_to_follow:
        bot.following.add(user)

        print(f"Bot '{bot.username}' started following '{user.username}'")
