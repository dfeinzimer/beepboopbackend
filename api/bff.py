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





# A comment feed for each article.




if __name__ == '__main__':
    basic_auth.init_app(app)
    app.run()
