from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_mongo_db():
    client = MongoClient("mongodb+srv://userweb:1234@myprojectdbcluster.t5vswpc.mongodb.net/part1",
                         server_api=ServerApi('1'))
    db = client.hw20
    return db




