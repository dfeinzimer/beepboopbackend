#!/usr/bin/python3


import datetime
import hashlib
import sqlite3
import flask
import json
import uuid
from flask import g
from flask import Response
from flask import request, jsonify
from flask_basicauth import BasicAuth
import os


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, '..', 'db', 'db', 'articles.db')


app = flask.Flask(__name__)
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
Get a connection the sql db
This should be deprecated and removed as everything should be in Cassandra by
the end of project 3.
#############################################################################'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        #db.execute('pragma foreign_keys=ON')

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db


'''#############################################################################
Closes connection automatically
#############################################################################'''
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


'''#############################################################################
Run a query against the sql db
This should be deprecated and removed as everything should be in Cassandra by
the end of project 3.
#############################################################################'''
def query_db(query, args=(), one=False):
    try:
        cur = get_db()
        cursor = cur.cursor()
        article_id = {"article_id": ""}
        #using with automatically commits
        try:
            with cur:
                cursor.execute(query, args)
                rv = cursor.fetchall()
                # gets the rowID of the last inserted row so we can get the url
                # to the post
                article_id["article_id"] = str(cursor.lastrowid)

            cur.close()
        except Exception as err:
            return [{"error": str(err), "query": query,}]
        if cursor.rowcount == 0:
            return not_found()
        elif int(article_id["article_id"]) != 0:
            return article_id
        else:
            return (rv[0] if rv else None) if one else rv
    except Exception as err:
        err_list_dict = [{"error": str(err),
                        "query": query,}]

        return err_list_dict


'''#############################################################################
Routes
#############################################################################'''


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    resp.content_type = "applciation/json"
    return resp


'''#############################################################################
[TESTED, WORKING] Get all articles
#############################################################################'''
@app.route('/articles', methods=['GET'])
def all_articles():
    objects = []
    rows = session.execute('SELECT * FROM articles')
    for row in rows:
        result = {}
        result["article_date"] = row.article_date
        result["author"] = row.author
        result["content"] = row.content
        result["headline"] = row.headline
        result["last_modified"] = row.last_modified
        result["title"] = row.title
        result["user_display_name"] = row.user_display_name
        objects.append(result)
    resp = jsonify(objects)
    return resp


'''#############################################################################
[TESTED, WORKING] Post a new article
#############################################################################'''
@app.route('/articles', methods=['POST'])
def new_article():
    if request.is_json:
        content = request.get_json()
        id = uuid.uuid1()
        session.execute(
            """
            INSERT INTO articles (
                article_id,
                title, content,
                headline, author,
                article_date, last_modified, user_display_name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (id,
            content["title"], content["content"],
            content["headline"], content["author"],
            content["article_date"],str(datetime.date.today()),
            content['user_display_name'])
        )
        resp = json.dumps({"article_id":str(id)})
        #resp.status_code = 201
        return resp
    else:
        return "expected JSON"


'''#############################################################################
[TESTED, WORKING] Get an individual article by ID
#############################################################################'''
@app.route('/articles/<article_ID>', methods=['GET'])
def get_article(article_ID):
    objects = []
    query = f"SELECT * FROM articles WHERE article_id = {str(article_ID)}"
    rows = session.execute(query)
    for row in rows:
        result = {}
        result["article_date"] = row.article_date
        result["author"] = row.author
        result["content"] = row.content
        result["headline"] = row.headline
        result["last_modified"] = row.last_modified
        result["title"] = row.title
        result["user_display_name"] = row.user_display_name
        objects.append(result)

    resp = jsonify(objects)
    resp.headers['Last-Modified'] = f"{objects[0]['last_modified']}"

    if 'If-Modified-Since' in request.headers:
        if datetime.datetime.strptime(request.headers['If-Modified-Since'], "%Y-%m-%d") < datetime.datetime.strptime(objects[0]['last_modified'], "%Y-%m-%d"):
            return resp
        else :
            res = jsonify()
            res.status_code = 304
            return res
    else:
        return resp


'''#############################################################################
[TESTED, WORKING] Edit an individual article
#############################################################################'''
@app.route('/articles/<article_ID>', methods=['PATCH'])
def edit_article(article_ID):
    content = request.get_json()
    rows = session.execute('SELECT * FROM articles')
    found = False
    id = None
    for row in rows:
        if str(row.article_id) == article_ID:
            found = True
            id = row.article_id
    if found:
        session.execute("DELETE FROM articles WHERE article_id="+str(id))
        session.execute(
            """
            INSERT INTO articles (
                article_id,
                article_date,
                author,
                content,
                headline,
                last_modified,
                title,
                user_display_name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                id,
                content["article_date"],
                content["author"],
                content["content"],
                content["headline"],
                str(datetime.date.today()),
                content["title"],
                content["user_display_name"]
            )
        )
    resp = json.dumps({"article_id":str(id)})
    return resp


'''#############################################################################
[TESTED, WORKING] Delete an individual article
#############################################################################'''
@app.route('/articles/<article_ID>', methods=['DELETE'])
def delete_article(article_ID):
    rows = session.execute("DELETE FROM articles WHERE article_id="+str(article_ID))
    return ""


'''#############################################################################
[TESTED, WORKING] Get n most recent articles
#############################################################################'''
@app.route('/articles/recent/<num_of_articles>', methods=['GET'])
def get_recent_articles(num_of_articles):
    objects = []
    rows = session.execute("SELECT * FROM articles LIMIT " + str(num_of_articles))
    for row in rows:
        result = {}
        result["article_date"] = row.article_date
        result["article_id"] = str(row.article_id)
        result["author"] = row.author
        result["content"] = row.content
        result["headline"] = row.headline
        result["last_modified"] = row.last_modified
        result["title"] = row.title
        result["user_display_name"] = row.user_display_name
        objects.append(result)

    resp = jsonify(objects)
    resp.headers['Last-Modified'] = f"{objects[0]['last_modified']}"

    if 'If-Modified-Since' in request.headers:
        if datetime.datetime.strptime(request.headers['If-Modified-Since'], "%Y-%m-%d") < datetime.datetime.strptime(objects[0]['last_modified'], "%Y-%m-%d"):
            return resp
        else :
            res = jsonify()
            res.status_code = 304
            return res
    else:
        return resp


'''#############################################################################
[TESTED, WORKING] Get n most recent articles meta data
#############################################################################'''
@app.route('/articles/recent/meta/<num_of_articles>', methods=['GET'])
def get_recent_articles_metadata(num_of_articles):
    objects = []
    rows = session.execute("SELECT * FROM articles LIMIT " + str(num_of_articles))
    for row in rows:
        result = {}
        result["article_date"] = row.article_date
        result["article_id"] = str(row.article_id)
        result["author"] = row.author
        result["location"] = "articles/" + str(row.article_id)
        result["title"] = row.title
        result["user_display_name"] = row.user_display_name
        result["last_modified"] = row.last_modified
        objects.append(result)

    resp = jsonify(objects)
    resp.headers['Last-Modified'] = f"{objects[0]['last_modified']}"
    resp.headers["Content-Type"] = "json; charset=utf-8"

    if 'If-Modified-Since' in request.headers:
        if datetime.datetime.strptime(request.headers['If-Modified-Since'], "%Y-%m-%d") < datetime.datetime.strptime(objects[0]['last_modified'], "%Y-%m-%d"):
            return resp
        else :
            res = jsonify()
            res.status_code = 304
            return res
    else:
        return resp


if __name__ == '__main__':
    app.run()
