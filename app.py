import json
import os
from pathlib import Path
from os.path import expanduser
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Paugers_comment_Stripper import CommentStripper

app = Flask(__name__, static_folder='./build', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/videoId/<ID>/<APIKEY>', methods =['POST'])
def get_comments(ID,APIKEY):
    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder = path_to_download_folder + "/Dataset.json"
    strip = CommentStripper(ID,APIKEY)
    strip.video_data()
    x =strip.top_comment_strip()
    y=strip.remove_unwanted(x)
    strip.un_cringe(y)

    transfer_file = None
    with open(path_to_download_folder, "r") as file:
        transfer_file = json.load(file)
    temp_string = "/" + ID + "video.json"
    destination = expanduser("~") + '/Downloads' + temp_string
    with open(destination, "w") as saved_file:
        json.dump(transfer_file, saved_file)

    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder0 = path_to_download_folder + "/extraced.json"
    path_to_download_folder1 = path_to_download_folder + "/Dataset.json"

    os.remove(path_to_download_folder0)
    os.remove(path_to_download_folder1)

    return("Comments Extracted")

@app.route('/videoIdM/<ID>/<APIKEY>', methods =['GET'])
def get_comments_manual(ID,APIKEY):
    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder = path_to_download_folder + "/Dataset.json"
    strip = CommentStripper(ID,APIKEY)
    strip.video_data()
    x =strip.top_comment_strip()
    y=strip.remove_unwanted(x)
    strip.un_cringe(y)

    transfer_file = None

    with open(path_to_download_folder, "r") as file:
        transfer_file = json.load(file)
    temp_string = "/" + ID + "video.json"
    destination = expanduser("~") + '/Downloads' + temp_string
    with open(destination, "w") as saved_file:
        json.dump(transfer_file, saved_file)

    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder0 = path_to_download_folder + "/extraced.json"
    path_to_download_folder1 = path_to_download_folder + "/Dataset.json"

    os.remove(path_to_download_folder0)
    os.remove(path_to_download_folder1)

    return("Comments Extracted")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
