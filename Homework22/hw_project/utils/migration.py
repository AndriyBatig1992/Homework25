import sys
import os
import django
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from pathlib import Path
import pathlib


sys.path.append(Path(__file__).resolve().parent.parent.__str__())
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hw_project.settings')
django.setup()


from quotes.models import Author, Quote, Tag # noqa


client = MongoClient("mongodb+srv://userweb:1234@myprojectdbcluster.t5vswpc.mongodb.net/part1", server_api=ServerApi('1'))
db = client.hw20


authors = db.authors.find()

for author in authors:
    print(author)
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["date_born"],
        born_location=author["location_born"],
        description=author["bio"]
    )


quotes= db.quotes.find()

for quote in quotes:
    print(quote['tags'])
    tags =[]
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quotes =bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quotes:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(
            quote = quote['quote'],
            author = a
        )
        for tag in tags:
            q.tags.add(tag)


