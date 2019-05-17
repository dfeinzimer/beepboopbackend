#!/usr/bin/python3


# How to test
#DELETE - curl -i -X DELETE http://localhost:5000/tags/delete/tag_id
#POST - use test_comments_api.tavern.yaml


import datetime
import hashlib
import sqlite3
import flask
from flask import Flask, render_template
from flask import g
from flask import Response
from flask import request, jsonify
from flask_basicauth import BasicAuth
import click
import os
import json
import uuid


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, '..', 'db', 'db', 'tags.db')


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
Get a database connection.
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
Run a query against our db.
Can this be removed?
#############################################################################'''
def query_db(query, args=(), one=False):
    try:
        cur = get_db()
        cursor = cur.cursor()
        tag_id = {"tag_id": ""}

        #using with automatically commits
        try:
            with cur:
                cursor.execute(query, args)
                rv = cursor.fetchall()

                #gets the rowID of the last inserted row so we can get the url to the post
                tag_id["tag_id"] = str(cursor.lastrowid)

            cur.close()
        except Exception as err:
            return [{"error": str(err), "query": query,}]

        if cursor.rowcount == 0:
            return not_found()
        elif int(tag_id["tag_id"]) != 0:
            return tag_id
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
    message = [{
            'status': 404,
            'message': 'Not Found: ' + request.url
    }]
    resp = jsonify(message)
    resp.status_code = 404
    resp.content_type = "application/json"
    return resp


'''#############################################################################
[TESTED, WORKING] Get all tags
#############################################################################'''
@app.route('/tags/all', methods=['GET'])
def tags_all():
    objects = []
    rows = session.execute('SELECT * FROM tags')
    for row in rows:
        result = {}
        result["tag"] = row.tag
        result["url"] = row.url
        result["tag_id"] = str(row.tag_id)
        objects.append(result)
    resp = jsonify(objects)
    resp.status_code = 201
    return resp


'''#############################################################################
[TESTED, WORKING] Get all tags for article url x
#############################################################################'''
@app.route('/tags/url/<article_url>', methods=['GET'])
def retrive_tags(article_url):
    url = article_url.replace('=', '/')
    rows = session.execute("SELECT * FROM tags")
    count = 0
    objects = []
    result = {}
    for row in rows:
        result = {}
        if row.url == url:
            result["tag_id"] = str(row.tag_id)
            result["tag"] = row.tag
            result["url"] = row.url
            objects.append(result)
    resp = jsonify(objects)
    resp.status_code = 201
    return resp


'''#############################################################################
[TESTED, WORKING] Get a tag by its id
#############################################################################'''
@app.route('/tags/tag/<tag>', methods=['GET'])
def retrive_urls(tag):
    objects = []
    rows = session.execute("SELECT * FROM tags WHERE tag_id="+str(tag))
    for row in rows:
        result = {}
        result["tag"] = row.tag
        result["url"] = row.url
        result["tag_id"] = str(row.tag_id)
        objects.append(result)
    resp = jsonify(objects)
    resp.status_code = 201
    return resp


'''#############################################################################
[TESTED, WORKING] Post a new tag to a given article url
#############################################################################'''
@app.route('/tags', methods=['POST'])
def add_tag():
    if request.is_json:
        content = request.get_json()
        new_id = uuid.uuid1()
        new_tag = content["tag"]
        new_url = content["url"]
        session.execute(
            """
            INSERT INTO tags
            (
                tag_id,
                tag,
                url
            )
            VALUES (%s, %s, %s)
            """,
            (
                new_id,
                new_tag,
                new_url
            )
        )
        objects = []
        result = {}
        result["tag_id:"] = str(new_id)
        objects.append(result)
        resp = jsonify(objects)
        resp.status_code = 201
        return resp
    else:
        return "expected JSON"


'''#############################################################################
[TESTED, WORKING] Delete a tag by its article url and tag id
#############################################################################'''
@app.route('/tags/<tag_id>', methods=['DELETE'])
def tag_delete(tag_id):
    rows = session.execute("DELETE FROM tags WHERE tag_id="+tag_id)
    objects = []
    result = {}
    result["Status:"] = "OK"
    objects.append(result)
    resp = jsonify(objects)
    resp.status_code = 201
    return resp


'''#############################################################################
Flask custom commands
#############################################################################'''


@click.command()
@click.argument('tag')
@click.argument('url')
def new_tag(tag, url):
    if request.is_json:
        content = request.get_json()
        id = uuid.uuid1()
        session.execute(
            """
            INSERT INTO tags (
                tag_id,
                tag,
                url
            )
            VALUES (%s, %s, %s)
            """,
            (id,
            tag, url
            )
        )
        resp = json.dumps({"tag_id":str(id)})
        #resp.status_code = 201
        return resp
    else:
        return "expected JSON"

        # Project 2 code
        # query_args = (tag, url)
        # query = "INSERT INTO tags (tag, url) VALUES (?, ?)"
        #
        # result = query_db(query, query_args)
        # resp = jsonify(result)
        # resp.status_code = 201
        # resp.headers['Location'] = f"/project1/{result['tag_id']}"
        # return resp


@click.command()
@click.argument('url')
@click.argument('tag')
def add_existing_tag(url, tag):
    if request.is_json:
        content = request.get_json()
        id = uuid.uuid1()
        session.execute(
            """
            INSERT INTO tags (
                tag_id,
                url,
                tag
            )
            VALUES (%s, %s, %s)
            """,
            (id,
            url, tag
            )
        )
        resp = json.dumps({"tag_id":str(id)})
        #resp.status_code = 201
        return resp
    else:
        return "expected JSON"

    #Project 2 code
    # query_args = (tag, url,)
    # query = "INSERT INTO tags (tag, url) VALUES (?, ?)"
    #
    # result = query_db(query, query_args)
    # resp = jsonify(result)
    # resp.status_code = 201
    # resp.headers['Location'] = f"/project1/{result['tag_id']}"
    # return resp


@click.command()
@click.argument('url')
def delete_tag(url):
    rows = session.execute("DELETE FROM tags WHERE url="+str(url))
    return None

    #Project 2 code
    # query = "DELETE FROM tags WHERE url = ?"
    # query_args = (url,)
    #
    # result = query_db(query, query_args)
    # if type(result) == flask.Response:
    #     return result


if __name__ == '__main__':
    app.run()
