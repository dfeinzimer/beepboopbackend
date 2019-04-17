import datetime
from rfeed import *
import requests
import json
from flask import Flask, g, jsonify, Response, request
from flask_basicauth import BasicAuth
import os

# A feed containing the full text for each article, its tags as RSS categories, and a comment count.

# Get the article data
article_request = requests.get('http://localhost/articles/recent/10', auth=('dfeinzimer@gmail.com','password1'))

# Parse the article data
article_loaded = json.loads(article_request.text)

for x in article_loaded:
    print("Article:",x['article_id'])
    print("\t",x['content'])
    tag_request = requests.get('http://localhost/tags/url/articles='+str(x['article_id']), auth=('dfeinzimer@gmail.com','password1'))
    tag_loaded = json.loads(tag_request.text)
    if tag_loaded:
        for y in tag_loaded:
            print("\t\t",y['tag'])
# Make an empty list to hold rfeed items
feed_items = []
