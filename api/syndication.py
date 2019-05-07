from rfeed import *
from flask import Flask, g, jsonify, Response, request
import requests
import datetime
import json
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True

'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
from cassandra import ReadTimeout
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')
'''#############################################################################
Older Cassandra implementation possibly no longer necessary
#############################################################################'''
from flask_cassandra import CassandraCluster
cassandra = CassandraCluster()
app.config['CASSANDRA_NODES'] = ['172.17.0.2']

basic_auth_creds = ('test@email.com', 'test@email.com')

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    resp.content_type = "application/json"
    return resp


@app.route('/syndication/summary', methods=['GET'])
def summary():
    r = requests.get('http://localhost/articles/recent/meta/10', auth=basic_auth_creds)
    summ = []
    response = r.json()

    for obj in response:
        summ.append(Item(
            title = obj["title"],
            link = f"http://localhost/{obj['location']}",
            author = obj["author"],
            pubDate = datetime.datetime.strptime(obj["article_date"], "%m/%d/%Y")
        ))

    feed = Feed(
    title = "Sample RSS Feed",
    link = "http://localhost/syndication/summary",
    description = "Summary feed of articles",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = summ
    )

    return feed.rss()


@app.route('/syndication/full', methods=['GET'])
def full():
    meta = requests.get('http://localhost/articles/recent/meta/100', auth=basic_auth_creds)
    article = requests.get('http://localhost/articles/recent/100', auth=basic_auth_creds)
    articles = article.json()

    rss = []
    tags = []
    comment_counts = []

    #Get tags for each article and add whole json obj into list
    for obj in meta.json():
        url = obj["location"].replace("/", "=")

        tag = requests.get(f"http://localhost/tags/url/{url}", auth=basic_auth_creds)
        comment_count = requests.get(f"http://localhost/comments/count/{url}", auth=basic_auth_creds)

        tags.append(tag.json())
        comment_counts.append(comment_count.json())

    idx = 0
    # for every article
    for article in articles:
        category_obj = []
        comment_num = []

        #append its tags as categories
        for tag in tags[idx]:
            if "status" not in tag:
                category_obj.append(Category(tag["tag"]))
            else:
                category_obj.append(Category(""))

        #Bc of the structure of the data, I have to do a sketch for loop.
        for comment in comment_counts[idx]:
            comment_num.append(comment["count"])


        rss.append(Item(
            title = article["title"],
            link = f"http://localhost/articles/{article['article_id']}",
            author = article["author"],
            pubDate = datetime.datetime.strptime(article["article_date"], "%m/%d/%Y"),
            categories = category_obj,
            comments = comment_num[0],
            description = article["content"]
        ))

        idx += 1

    feed = Feed(
    title = "Full text article feed",
    link = "http://localhost/syndication/full",
    description = "Full text article RSS feed",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = rss
    )

    return feed.rss()


@app.route('/syndication/comments', methods=['GET'])
def comments():
    article = requests.get('http://localhost/articles/recent/meta/100', auth=basic_auth_creds)
    articles = article.json()

    comments = []
    rss = []

    for r in articles:
        url = r["location"].replace("/", "=")
        comments.append(requests.get(f'http://localhost/comments/100/{url}', auth=basic_auth_creds).json())

    for comment in comments:
        com_obj = []
        for c in comment:
            if c["comment"] != '':
                #com_obj.append({"user": c["user_display_name"], "comment": c["comment"]})
                com_obj.append(f"{c['user_display_name']}: {c['comment']}")

        if "article_url" in comment[0]:
            rss.append(Item(
                link = f"http://localhost/comments/{comment[0]['article_url']}",
                comments = f"http://localhost/comments/{comment[0]['article_url']}",
                description = str(com_obj).strip('[]')
            ))

    feed = Feed(
    title = "Full text article feed",
    link = "http://localhost/syndication/full",
    description = "Full text article RSS feed",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = rss
    )

    return feed.rss()



if __name__ == '__main__':
    #basic_auth.init_app(app)
    app.run()
