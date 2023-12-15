import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://userweb:1234@myprojectdbcluster.t5vswpc.mongodb.net/part1", server_api=ServerApi('1'))
db = client.hw20

with open("quotes.json", 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)


for quote in quotes:
        author = db.authors.find_one({'fullname': quote['author']})
        if author:
            db.quotes.insert_one({
                'quote': quote['quote'],
                'tags': quote['keywords'],
                'author': ObjectId(author['_id'])
            })
        else:
            print(f"Author not found for {quote['author']}")



