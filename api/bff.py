import datetime
from rfeed import *
import requests
import json


def getSummaryFeed():
    #r = requests.get('https://www.technologyreview.com/c/computing/rss/') #works
    r = requests.get('http://localhost:5000/articles/recent/meta/10')
    r.json()
    return r.json()


def getArcicleText():
    r = requests.get('http://localhost:5000/articles/recent/10')
    r.json()
    return r.json()

# def getTags():
#     r = requests.get('http://localhost:5000/tags/from/)

def getCommentFeed():
    for
    r = requests.get('http://localhost:5000/comments/{n}/articles={x}')
    for n
    r = requests.get(f"http://localhost/comments/count/arcticles={n}")
    r.json()
    #print(r.json())
    return r.json()

def RSSFeed():
    arc = getSummaryFeed()
    #arcText = getArcicleText()
    print("******************************")
    for a in arc:
        Title =  a['title']
        Author = a['author']
        Date = a['article_date']

    # arcText = getArcicleText()
    # for text in arcText:
    #     Content = text['content']

    # Can't run both comment and article api at the same time.
    comm = getCommentFeed()
    print(comm)
    for c in comm:
        User_id = comm['user_display_name']
        Comment = comm['comment']




    item1 = Item(
        title = Title,
        author = Author,
        pubDate = datetime.datetime(2014, 12, 30, 14, 15),
        link = "http://localhost:5000/articles/recent/10",
        description = Content,
        comments = 3)

    # item2 = Item(
    #     title = Comment,
    #     author = User_id)

    feed = Feed(
        title = "Sample RSS Feed",
        link = "http://localhost:5000/articles/recent/10",
        description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
        language = "en-US",
        items = [item1])

    print(feed.rss())


if __name__ == '__main__':
    #getRequest()
    #getCommentFeed()
    RSSFeed()




######################################################################
# item1 = Item(
#     title = ,
#     author = "Santiago L. Valdarrama",
#     pubDate = datetime.datetime(2014, 12, 29, 10, 00),
#     link = "http://www.example.com/articles/2")
#
# item2 = Item(
#     title = "Second article",
#     link = "http://www.example.com/articles/2",
#     description = "This is the description of the second article",
#     author = "Santiago L. Valdarrama",
#     guid = Guid("http://www.example.com/articles/2"),
#     pubDate = datetime.datetime(2014, 12, 30, 14, 15))
#
# feed = Feed(
#     title = "Sample RSS Feed",
#     link = "http://www.example.com/rss",
#     description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
#     language = "en-US",
#     lastBuildDate = datetime.datetime.now(),
#     items = [item1, item2])
#
# print(feed.rss())
