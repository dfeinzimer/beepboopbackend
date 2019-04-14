import datetime
from rfeed import *
import requests
import json
from flask import g
from flask import Response
from flask import request, jsonify
from flask_basicauth import BasicAuth
import os

# gets meta data for the 10 most recent articles
def getSummaryFeed():
    r = requests.get('http://localhost:5000/articles/recent/meta/10')
    r.json()
    return r.json()

# gets the full text in an article for 10 articles
def getArcicleText():
    for n in 10:
        r = requests.get('http://localhost/articles/recent/{}'.format(n))
        r.json()
        return r.json()

# gets tags for a arctile
# todo: Need to figure out how to get a tag from a giving url without knowing the url
def getTags():
    Article_url = getSummaryFeed()
    for n in Article_url:
        article_url = Article_url['location']

    r = requests.get('http://localhost/tags/from/{}'.format(article_url)
    r.json()
    return r.json()

# gets the comments in an article
def getCommentFeed():
    for n in 1:
        for x in 1:
            r = requests.get("http://localhost/comments/{}/articles={}".format(n,x))
            r.json()
            return r.json()

# get the comment count for a article
def getCommentCount():
    for n in 1:
        r = requests.get("http://localhost/comments/count/arcticles={}".format(n))
        r.json()
        return r.json()

# flask route to get rss summary
@app.route('/rss/summary/')
def rssSummary():
    arc = getSummaryFeed()

    for a in arc:
        Title =  a['title']
        Author = a['author']
        Date = a['article_date']

    item1 = Item(
        title = Title,
        author = Author,
        pubDate = datetime.datetime(2014, 12, 30, 14, 15), # need to fix the date format
        link = "http://localhost:5000/articles/recent/10")

    feed = Feed(
        title = "Summary RSS Feed",
        link = "http://localhost/comments/recent/10",
        description = "A summary feed listing the title, author, date, and link for the 10 most recent articles.",
        language = "en-US",
        items = [item1])

    return feed.rss()

# flask route to get comments rss
@app.route('rss/comments/')
def rssComments():
    comm = getCommentFeed()
    for c in comm:
        User_id = comm['user_display_name']
        Comment = comm['comment']
        Article_url = comm['article_url']

    item1 = Item(
        title = Comment,
        author = User_id,
        link = Article_url)

    feed = Feed(
        title = "Comment RSS Feed",
        description = "A comment feed for each article.",
        language = "en-US",
        items = [item1])

    return feed.rss()

# flask route to get full rss
@app.route('rss/full/')
def rssFull():
    commCount = getCommentCount()
    arcText = getArcicleText()
    tags = getTags()

    for text in arcText:
        Content = text['content']

    for cc in commCount:
        Count = commCount['count']

    for tag in tags:
        Tag = tags['tag']

    item1 = Item(
        description = Content,
        comments = Count,
        category = Tag)

    feed = Feed(
        title = "Full RSS Feed",
        description = "A full feed containing the full text for each article, its tags, and a comment count.",
        language = "en-US",
        items = [item1])

    return feed.rss()

if __name__ == '__main__':
    app.run()
