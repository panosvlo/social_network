from celery import shared_task
from django.contrib.auth.models import User
import requests
import random
import string

API_BASE_URL = "http://localhost:8000"


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_bot_account(topic):
    username = f"{topic['name']}_bot"
    email = f"{username}@example.com"
    password = generate_password()

    user = User.objects.create_user(username=username, email=email, password=password)
    user.profile.topics_of_interest.add(
        topic['id'])  # Assuming you have a ManyToManyField 'topics_of_interest' in UserProfile model
    user.profile.save()

    print(f"Created bot account for topic '{topic['name']}' with username '{username}'")


@shared_task()
def create_bots_for_all_topics():
    response = requests.get(f"{API_BASE_URL}/topics/")
    print(response)
    topics = response.json()

    print("in the task")

    for topic in topics:
        create_bot_account(topic)
