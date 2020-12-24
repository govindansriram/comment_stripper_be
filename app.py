import json
import os
from pathlib import Path
from os.path import expanduser
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Paugers_comment_Stripper import CommentStripper
from database import db
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder='./build', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/videoId/<ID>/<APIKEY>', methods =['POST'])
def get_comments(ID,APIKEY):
    strip = CommentStripper(ID,APIKEY)
    strip.video_data()
    x =strip.top_comment_strip()
    y=strip.remove_unwanted(x)
    spread_insert = db(strip.un_cringe(y))
    spread_insert.add_data()
    ret = "Successfully added videoId: " + ID + " to MongoDB"
    return ret


@app.route('/videoIdM/<ID>/<APIKEY>', methods =['GET'])
def get_comments_manual(ID,APIKEY):
    strip = CommentStripper(ID,APIKEY)
    strip.video_data()
    x =strip.top_comment_strip()
    y=strip.remove_unwanted(x)
    spread_insert = db(strip.un_cringe(y))
    spread_insert.add_data()
    ret = "Successfully added videoId: " + ID + " to MongoDB"
    return ret


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
