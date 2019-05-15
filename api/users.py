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
import base64

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, '..', 'db', 'db', 'users.db')


app = flask.Flask(__name__)
app.config["DEBUG"] = True


#DATABASE.init_app(app)
#basic_auth = auth.GetAuth()
#basic_auth = auth.GetAuth()
#basic_auth.init_app(app)
#DATABASE = '../db/db/users.db'



'''#############################################################################
Setup Cassandra, connect to a cluster and keyspace.
#############################################################################'''
from cassandra.cluster import Cluster
from cassandra import ReadTimeout
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('beepboopbackend')




class auth(BasicAuth):
    def check_credentials(self, username, password):
        pass_hash = hashlib.md5(password.encode())
        objects = []
        rows = session.execute('SELECT * FROM users')
        for row in rows:
            result = {}
            result["email"] = row.email
            result["display_name"] = row.display_name
            result["pass_hash"] = row.pass_hash
            objects.append(result)
            if len(objects) > 0:
                return True
            else:
                return False

        # Project 2 code
        # pass_hash = hashlib.md5(password.encode())
        # query = "SELECT * FROM users WHERE email = ? AND pass_hash = ?"
        # query_args = (username, pass_hash.hexdigest())
        # conn = sqlite3.connect(DATABASE)
        # cursor = conn.cursor()
        # cursor.execute(query, query_args)
        # result = cursor.fetchall()
        # conn.close()
        # if len(result) > 0:
        #     return True
        # else:
        #     return False

basic_auth = auth(app)


def user_exists(username, password):
        objects = []
        rows = session.execute('SELECT * FROM users')
        for row in rows:
            result = {}
            result["email"] = row.email
            result["display_name"] = row.display_name
            result["pass_hash"] = row.pass_hash
            objects.append(result)
            if len(objects) > 0:
                return True
            else:
                return False

        # Project 2 code
        # pass_hash = hashlib.md5(password.encode())
        # query = "SELECT * FROM users WHERE email = ? AND pass_hash = ?"
        # query_args = (username, pass_hash.hexdigest())
        # conn = sqlite3.connect(DATABASE)
        # cursor = conn.cursor()
        # cursor.execute(query, query_args)
        # result = cursor.fetchall()
        # conn.close()
        # if len(result) > 0:
        #     return True
        # else:
        #     return False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
    db.row_factory = make_dicts
    return db


# Closes database connection automatically
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db()
    cursor = cur.cursor()
    try:
        # Autocommit by using 'with'
        with cur:
            cursor.execute(query, args)
            rv = cursor.fetchall()
        cur.close()
    except Exception as err:
        error = [{"error": str(err), "query": query,}]
        if error[0]["error"].split(' ')[0] == "UNIQUE":
            resp = jsonify(error)
            resp.status_code = 409
            return True, resp
        else:
            return False, not_found()
    return (False, rv[0] if rv else False, None) if one else False, rv


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

def unauth():
    message = {
            'status': 401,
            'message': 'Unauthorized'
    }
    resp = jsonify(message)
    resp.status_code = 401
    resp.content_type = "application/json"
    return resp


'''#############################################################################
[TESTED, WORKING] Get all users
#############################################################################'''
@app.route('/users', methods=['GET'])
def get_all():
    objects = []
    rows = session.execute('SELECT * FROM users')
    for row in rows:
        result = {}
        result["email"] = row.email
        result["display_name"] = row.display_name
        result["pass_hash"] = row.pass_hash
        objects.append(result)
    return json.dumps(objects)


'''#############################################################################
[TESTED, WORKING] Create a new user
#############################################################################'''
@app.route('/users/new', methods=['POST'])
def create_user():
    if request.is_json:
        content = request.get_json()
        pass_hash = hashlib.md5(content["password"].encode())
        id = uuid.uuid1()
        session.execute(
        """
        INSERT INTO users (
            user_id,
            email,
            display_name,
            pass_hash
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            id,
            content["email"],
            content["display_name"],
            str(pass_hash.hexdigest())
        ))
        resp = json.dumps({"user_id":str(id)})
        return resp
    else:
        return "Expected JSON"


'''#############################################################################
[TESTED, WORKING] Delete a user
#############################################################################'''
@app.route('/users', methods=['DELETE'])
#@basic_auth.required
def remove_user():
    content = request.get_json()
    rows = session.execute('SELECT * FROM users')
    found = False
    id = None
    for row in rows:
        if row.email == content["email"]:
            found = True
            id = str(row.user_id)
    if found:
        session.execute("DELETE FROM users WHERE user_id="+id)
    return ""


'''#############################################################################
[TESTED, WORKING] Change a password
#############################################################################'''
@app.route('/users', methods=['PATCH'])
#@basic_auth.required
def change_password():
    content = request.get_json()
    rows = session.execute('SELECT * FROM users')
    found = False
    id = None
    for row in rows:
        if row.email == content["email"]:
            found = True
            id = row.user_id
            display_name = row.display_name
    if found:
        session.execute("DELETE FROM users WHERE user_id="+str(id))
        pass_hash = hashlib.md5(content["new_password"].encode())
        session.execute(
            """
            INSERT INTO users (
                user_id,
                email,
                display_name,
                pass_hash
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                id,
                content["email"],
                display_name,
                str(pass_hash.hexdigest())
            )
        )
    resp = json.dumps({"user_id":str(id)})
    return resp


@app.route('/auth', methods=['GET'])
@basic_auth.required
def auth():
    return ""
    # data = request.authorization

    # if user_exists(data["username"], data["password"]):
    #     return jsonify()
    # else:
    #     return unauth()


if __name__ == '__main__':
    basic_auth.init_app(app)
    app.run()
