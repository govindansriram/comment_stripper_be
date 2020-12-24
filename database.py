import json
import pymongo
import ssl
import os
from dotenv import load_dotenv

class db:

    def __init__(self, json_string):
        self.comment_data = json.loads(json_string)
        channel_id = self.comment_data[0]['videoChannelID']
        database_name = channel_id
        load_dotenv()
        CONNECTION_STRING = os.getenv('DB_KEY')
        client = pymongo.MongoClient(CONNECTION_STRING, ssl_cert_reqs=ssl.CERT_NONE)
        self.base = client[database_name]

    def add_data(self):
        collection_name = self.comment_data[0]['videoId']
        self.base[collection_name].drop()
        collection = self.base[collection_name]

        for i in self.comment_data:
            i['_id'] = i.pop('commentId')
            i.pop('videoId')
            i.pop('videoChannelID')

            collection.insert_one(i)
