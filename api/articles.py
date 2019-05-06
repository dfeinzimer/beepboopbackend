#!/usr/bin/python3

import datetime
import hashlib
import sqlite3
import flask
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
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')
'''#############################################################################
Older Cassandra implementation possibly no longer necessary
#############################################################################'''
from flask_cassandra import CassandraCluster
cassandra = CassandraCluster()
app.config['CASSANDRA_NODES'] = ['172.17.0.2']

#gets a connection to our DB
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


#closes connection automatically
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#run a query against our db
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

                #gets the rowID of the last inserted row so we can get the url to the post
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


#----------------------------------------ROUTES----------------------------------------
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


#Get all articles
@app.route('/articles', methods=['GET'])
def all_articles():
    query = "SELECT * FROM articles"
    resp = query_db(query)
    result = jsonify(resp)

    return result


#Post a new article
@app.route('/articles', methods=['POST'])
def new_article():
    if request.is_json:
        content = request.get_json()

        query_args = (content["title"], content["content"], content["headline"], content["author"], content["article_date"], str(datetime.date.today()), content['user_display_name'])
        query = "INSERT INTO articles (title, content, headline, author, article_date, last_modified, user_display_name) VALUES (?, ?, ?, ?, ?, ?, ?)"

        result = query_db(query, query_args)
        resp = jsonify(result)
        resp.status_code = 201
        resp.headers['Location'] = f"/articles/{result['article_id']}"
        return resp
    else:
        return "expected JSON"


#Get an individual article by ID
@app.route('/articles/<article_ID>', methods=['GET'])
def get_article(article_ID):

    query = "SELECT * FROM articles WHERE article_id = ?"
    query_args = (article_ID,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return not_found()

    return result


#edit an individual article
@app.route('/articles/<article_ID>', methods=['PATCH'])
def edit_article(article_ID):

    if request.is_json:

        query = "UPDATE articles SET "
        query_args = []
        content = request.get_json()

        for key, value in content.items():
            query += key + " = ?, "
            query_args.append(value)

        query += "last_modified = ? WHERE article_id = ?"
        query_args.append(str(datetime.date.today()))
        query_args.append(article_ID)

        result = query_db(query, query_args)

        if type(result) == flask.Response:
            return result
        else:
            resp = jsonify(result)
            resp.status_code = 200
            resp.content_type = "application/json"
            return resp

    else:
        return "Expected JSON"


#delete an individual article
@app.route('/articles/<article_ID>', methods=['DELETE'])
def delete_article(article_ID):
    query = "DELETE FROM articles WHERE article_id = ?"
    query_args = (article_ID,)

    result = query_db(query, query_args)
    if type(result) == flask.Response:
        return result
    else:
        resp = jsonify(result)
        resp.status_code = 200
        resp.content_type = "application/json"
        return resp


#Get n most recent articles
@app.route('/articles/recent/<num_of_articles>', methods=['GET'])
def get_recent_articles(num_of_articles):
    query = "SELECT * FROM articles ORDER BY article_date DESC LIMIT ?"
    query_args = (num_of_articles,)

    result = query_db(query, query_args)
    resp = jsonify(result)
    resp.status_code = 200
    resp.content_type = "application/json"
    return resp


#Get n most recent articles meta data
@app.route('/articles/recent/meta/<num_of_articles>', methods=['GET'])
def get_recent_articles_metadata(num_of_articles):
    query = "SELECT article_id, title, author, user_display_name, article_date FROM articles ORDER BY article_date DESC LIMIT ?"
    query_args = (num_of_articles,)

    result = query_db(query, query_args)

    for d in result:
        article_id = d["article_id"]
        d["location"] = f"articles/{article_id}"

    resp = jsonify(result)
    resp.status_code = 200
    resp.content_type = "application/json"
    return resp


if __name__ == '__main__':
    app.run()
