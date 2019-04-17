import datetime
from rfeed import *
import requests
import json
from flask import Flask, g, jsonify, Response, request
from flask_basicauth import BasicAuth
import os

# A feed containing the full text for each article, its tags as RSS categories, and a comment count.

# Make an empty list to hold rfeed items
feed_items = []

article_request = requests.get('http://localhost/articles/recent/10', auth=('dfeinzimer@gmail.com','password1'))
article_loaded = json.loads(article_request.text)

for x in article_loaded:
    print("Article:",x['article_id'])
    print("\t"+x['content'])
    content = x['content']

    tag_request = requests.get('http://localhost/tags/url/articles='+str(x['article_id']), auth=('dfeinzimer@gmail.com','password1'))
    tag_loaded = json.loads(tag_request.text)

    categories = []
    if tag_loaded:
        for y in tag_loaded:
            print("\t\t#"+y['tag'])
            categories.append(y['tag'])

    comment_request = requests.get('http://localhost/comments/count/articles='+str(x['article_id']), auth=('dfeinzimer@gmail.com','password1'))
    comment_loaded = json.loads(comment_request.text)
    for z in comment_loaded:
        print("\t\t\tComment Count:",z['count'])
        count = z['count']

    print("Content:",content)
    print("Categories:",categories)
    print("Count:",count)

    item = Item(
        description = content,
        categories = categories,
        comments = count
    )
    feed_items.append(item)

feed = Feed(
    title = "Full Article Feed",
    link = "http://localhost/rss/full",
    description = "A feed containing the full text for each article, its tags as RSS categories, and a comment count.",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = feed_items
)

return (feed.rss())
