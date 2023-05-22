import os
import django
import requests
import sys
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from users.models import User, Post, Article  # import the Article model


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


if __name__ == '__main__':
    bot_posts()
