from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post
from faker import Faker
import random


class Command(BaseCommand):
    help = "Creates sample users and posts"

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        # Create 5 users
        users = []
        for i in range(5):
            username = fake.user_name()
            email = fake.email()
            password = "password123"
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))

        # Create 20 posts
        for i in range(20):
            author = random.choice(users)
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.text(max_nb_chars=500),
                author=author,
            )
            self.stdout.write(self.style.SUCCESS(f"Created post: {post.title[:30]}..."))

        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))
