#!/usr/bin/python3

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
#from flask.cli import AppGroup #this works

app = flask.Flask(__name__)
app.config["DEBUG"] = True


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, '..', 'db', 'db', 'tags.db')


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

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db

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


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/tags/all', methods=['GET'])
def comments_all():

    query = 'SELECT * FROM tags;'
    query_args = ("")

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return not_found()

    return result


@app.route('/tags/url/<article_url>', methods=['GET'])
def retrive_tags(article_url):

    new_url = article_url.replace('=', '/')

    query = 'SELECT * FROM tags Where url = ?;'
    query_args = (new_url,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return not_found()

    return result

@app.route('/tags/tag/<tag>', methods=['GET'])
def retrive_urls(tag):

    query = 'SELECT * FROM tags WHERE tag = ?;'
    query_args = (tag,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"

        return result
    else:
        return not_found()


#use postman or curl
@app.route('/tags', methods=['POST'])
def add_tag():
     if request.is_json:
        content = request.get_json()

        query_args = (content["tag"], content["url"])
        query = "INSERT INTO tags (tag, url) VALUES (?, ?)"

        result = query_db(query, query_args)
        resp = jsonify(result)
        resp.status_code = 201
        resp.headers['Location'] = f"/project1/{result['tag_id']}"
        return resp
     else:
        return "expected JSON"


@click.command()
@click.argument('tag')
@click.argument('url')
def new_tag(tag, url):
        query_args = (tag, url)
        query = "INSERT INTO tags (tag, url) VALUES (?, ?)"

        result = query_db(query, query_args)
        resp = jsonify(result)
        resp.status_code = 201
        resp.headers['Location'] = f"/project1/{result['tag_id']}"
        return resp


#use postman or curl
@app.route('/tags/existing/<url>', methods=['POST'])
def add_tag_existing(url):
     if request.is_json:
        content = request.get_json()

        query_args = (content["tag"], url,)
        query = "INSERT INTO tags (tag, url) VALUES (?, ?)"

        result = query_db(query, query_args)
        resp = jsonify(result)
        resp.status_code = 201
        resp.headers['Location'] = f"/project1/{result['tag_id']}"
        return resp
     else:
        return "expected JSON"

@click.command()
@click.argument('url')
@click.argument('tag')
def add_existing_tag(url, tag):
    query_args = (tag, url,)
    query = "INSERT INTO tags (tag, url) VALUES (?, ?)"

    result = query_db(query, query_args)
    resp = jsonify(result)
    resp.status_code = 201
    resp.headers['Location'] = f"/project1/{result['tag_id']}"
    return resp


@app.route('/tags', methods=['DELETE'])
def tag_delete():

    content = request.get_json()

    query = "DELETE FROM tags WHERE url = ? AND tag = ?"
    query_args = (content["url"], content["tag"])

    result = query_db(query, query_args)
    if type(result) == flask.Response:
        return jsonify(result)
    else:
        resp = jsonify(result)
        resp.status_code = 200
        resp.content_type = "application/json"
        return resp

@click.command()
@click.argument('url')
def delete_tag(url):
    query = "DELETE FROM tags WHERE url = ?"
    query_args = (url,)

    result = query_db(query, query_args)
    if type(result) == flask.Response:
        return result

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run()


# How to test
#DELETE - curl -i -X DELETE http://localhost:5000/tags/delete/tag_id
#POST - use test_comments_api.tavern.yaml
