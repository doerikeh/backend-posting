from django.core.management.base import BaseCommand
from kisahkita_art.models import Posting, Categories, Comment
import random
import datetime

categories = [
    'Teknologi',
    'Sport',
]

user = [
    "firdaus alfajar"
]


slug = [
    "firdaus alfajar"
]

posting = [
    "kasmdansdjnaksdn asdasjdoiasjd ,masdbjaskbdoua smlaksdjoiashdas dadasmoiwyqwyeasvdasd"
]

def generate_author_name():
    index = random.randint(0, 7)
    return user[index]

def generate_slug_name():
    index = random.randint(0, 7)
    return slug[index]

def generate_posting_name():
    index = random.randint(0, 7)
    return posting[index]

def generate_categories_name():
    index = random.randint(0, 7)
    return categories[index]

def generate_view_count():
    return random.randint(0, 100)

def generate_date_created():
    year = random.randint(2000, 2030)
    mounth = random.randint(1, 12)
    day = random.randint(1, 30)
    return datetime.date(year, mounth, day)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='the txt file that contains the journey'
        )

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                title = row
                categories = generate_categories_name()
                viewed = generate_view_count()
                user = generate_author_name()
                slug = generate_slug_name()
                posting = generate_posting_name()
                date_created = generate_date_created()
            

