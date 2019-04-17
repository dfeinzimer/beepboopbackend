import datetime
from rfeed import *
import requests
import json
from flask import Flask, g, jsonify, Response, request
from flask_basicauth import BasicAuth
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

# A summary feed listing the title, author, date, and link for the 10 most recent articles.
@app.route('/rss/summary', methods=['GET'])
def feed_summary():
    # Pull the data
    request = requests.get('http://localhost/articles/recent/10', auth=('dfeinzimer@gmail.com','password1'))

    # Parse the data
    loaded = json.loads(request.text)

    # Make an empty items list
    feed_items = []

    for x  in loaded:
        # Generate an rfeed item
        item = Item(
            title = x['title'],
            link = "http://localhost/articles/"+str(x['article_id']),
            author = x['author'],
            pubDate = datetime.datetime.now()
            # TODO fix the pubDate parmater. Below should work but it does not.
            #pubDate = datetime.datetime.strptime(x['article_date'], "%m/%d/%Y").strftime("%a, %d %b %Y %H:%M:%S %Z")
        )

        # Add the new item to the items list
        feed_items.append(item)

    # Build the rfeed feed object
    feed = Feed(
        title = "10 Most Recent Articles",
        link = "http://localhost/rss/summary",
        description = "A summary feed listing the title, author, date, and link for the 10 most recent articles.",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = feed_items
    )

    return (feed.rss())

# A full feed containing the full text for each article, its tags as RSS categories, and a comment count.
@app.route('/rss/full', methods=['GET'])
def feed_full():
    # Make an empty list to hold rfeed items
    feed_items = []

    article_request = requests.get('http://localhost/articles', auth=('dfeinzimer@gmail.com','password1'))
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

# A comment feed for each article.
@app.route('/rss/comments/<article_ID>', methods=['GET'])
def feed_comments(article_ID):
    # Make an empty list to hold rfeed items
    feed_items = []

    article_request = requests.get('http://localhost/comments/count/articles='+str(article_ID), auth=('dfeinzimer@gmail.com','password1'))
    article_loaded = json.loads(article_request.text)

    comment_count = None

    for x in article_loaded:
        comment_count = x['count']

    print("comment_count",comment_count)


    comment_request = requests.get('http://localhost/comments/'+str(comment_count)+'/articles='+str(article_ID), auth=('dfeinzimer@gmail.com','password1'))
    comment_loaded = json.loads(comment_request.text)

    for x in comment_loaded:
        item = Item(
            description = x['comment'],
        )
        feed_items.append(item)

    feed = Feed(
        title = "Comment Feed",
        link = "http://localhost/rss/comments/<num>",
        description = "A comment feed for each article.",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = feed_items
    )

    return(feed.rss())

if __name__ == '__main__':
    basic_auth.init_app(app)
    app.run()
