from celery import shared_task
from .models import User
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

    # Check if the user already exists
    user_exists = User.objects.filter(username=username).exists()

    if user_exists:
        print(f"Bot account for topic '{topic['name']}' with username '{username}' already exists. Skipping.")
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.topics_of_interest.add(topic['id'])
        user.save()

        print(f"Created bot account for topic '{topic['name']}' with username '{username}'")


@shared_task()
def create_bots_for_all_topics():
    response = requests.get("http://localhost:8000/api/topics/")
    print(response.json())
    topics = response.json()

    print("in the task")

    for topic in topics:
        create_bot_account(topic)
