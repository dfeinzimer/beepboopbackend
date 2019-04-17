import datetime
from rfeed import *
import requests
import json
from flask import Flask, g, jsonify, Response, request
from flask_basicauth import BasicAuth
import os

article_request = requests.get('http://localhost/articles/recent/10', auth=('dfeinzimer@gmail.com','password1'))

# Parse the article data
article_loaded = json.loads(article_request.text)
print("article_loaded",article_loaded)

# Make an empty list to hold rfeed items
feed_items = []
