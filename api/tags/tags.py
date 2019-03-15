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
from flask.cli import FlaskCLI #this does not work but should
#from flask.cli import AppGroup #this works

app = flask.Flask(__name__)
app.config["DEBUG"] = True
FlaskCLI(app) #need this to run commands but givs an error

DATABASE = 'db.db'
#DATABASE = '../../db/master.db'

class auth(BasicAuth):
    def check_credentials(self, username, password):

        pass_hash = hashlib.md5(password.encode())
        query = "SELECT * FROM users WHERE email = ? AND pass_hash = ?"
        query_args = (username, pass_hash.hexdigest())

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(query, query_args)
        result = cursor.fetchall()
        conn.close()

        if len(result) > 0:
            return True
        else:
            return False

basic_auth = auth(app)

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


@app.route('/tags/from/<url>', methods=['GET'])
def retrive_tags(url):

    query = 'SELECT * FROM tags Where url = ?;'
    query_args = (url,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return not_found()

    return result

@app.route('/tags/url/<tag>', methods=['GET'])
def retrive_urls(tag):

    query = 'SELECT * FROM tags WHERE tag = ?;'
    #query = 'SELECT * FROM comments ORDER BY tag_id LIMIT ?'
    # note that ORDER BY should be by date
    query_args = (tag,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return "404"

    return result

#use postman or curl
@app.route('/tags/new', methods=['POST'])
@basic_auth.required
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
@basic_auth.required
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


@app.route('/tags/delete/<url>', methods=['DELETE'])
@basic_auth.required
def tag_delete(url):
    query = "DELETE FROM tags WHERE url = ?"
    query_args = (url,)

    result = query_db(query, query_args)
    if type(result) == flask.Response:
        return result
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
    basic_auth.init_app(app)
    app.run()


# How to test
#DELETE - curl -i -X DELETE http://localhost:5000/tags/delete/tag_id
#POST - use test_comments_api.tavern.yaml
