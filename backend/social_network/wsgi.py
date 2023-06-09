"""
WSGI config for social_network project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from users.tasks import (
    fetch_and_save_topics,
    create_bots_for_all_topics,
    bot_posts,
    save_articles_to_database,
    create_random_bots,
    create_post_from_random_bot,
    create_comment_from_random_bot,
    create_like_from_random_bot,
    bot_follow_users)
from users.models import Topic

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

# add the Django project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

application = get_wsgi_application()

if not Topic.objects.exists():
    # If it is empty, run the fetch_and_save_topics function
    fetch_and_save_topics()
    save_articles_to_database()
    # create_bots_for_all_topics()
    create_random_bots()
    # bot_posts()
    create_post_from_random_bot()
    bot_follow_users()
    create_comment_from_random_bot()
    create_like_from_random_bot()
    print("Environment initiation completed.")