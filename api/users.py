#!/usr/bin/python3


from flask import Flask, g, jsonify, Response, request
from flask_basicauth import BasicAuth
#from flask_cassandra import CassandraCluster
#from .db import master as DATABASE
import base64
import datetime
import hashlib
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, '..', 'db', 'db', 'users.db')

#cassandra = CassandraCluster()
#app.config['CASSANDRA_NODES'] = ['cassandra-c1.terbiumlabs.com']  # can be a string or list of nodes

app = Flask(__name__)
app.config["DEBUG"] = True
#DATABASE.init_app(app)
#basic_auth = auth.GetAuth()
#basic_auth = auth.GetAuth()
#basic_auth.init_app(app)

#DATABASE = '../db/db/users.db'


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


def user_exists(username, password):
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


@app.route('/users', methods=['GET'])
def get_all():
    query = "SELECT * FROM users"
    err, result = query_db(query)
    return jsonify(result)


@app.route('/users/new', methods=['POST'])
def create_user():
    if request.is_json:
        data = request.get_json()
        pass_hash = hashlib.md5(data["password"].encode())
        query = "INSERT INTO users(email, display_name, pass_hash) values(?, ?, ?)"
        query_args = (data["email"], data["display_name"], pass_hash.hexdigest())
        err, result = query_db(query, query_args)
        if err == False:
            resp = jsonify(result)
            resp.status_code = 201
            resp.headers['Location'] = "/users"
            return resp
        else:
            return result
    else:
        return ('No JSON', 400, {})


@app.route('/users', methods=['DELETE'])
#@basic_auth.required
def remove_user():
    if request.is_json:
        data = request.get_json()
        if user_exists(data["email"], data["password"]):
            query = "DELETE FROM users WHERE email = ? AND pass_hash = ?"
            query_args = (data["email"], hashlib.md5(data["password"].encode()).hexdigest())
            err, resp = query_db(query, query_args)
            return jsonify(resp)
        else:
            return not_found()
    else:
        return "Expected JSON"


@app.route('/users', methods=['PATCH'])
#@basic_auth.required
def change_password():
    if request.is_json:
        data = request.get_json()

        if user_exists(data["email"], data["password"]):
            query = "UPDATE users SET pass_hash = ? WHERE email = ? AND pass_hash = ?"
            query_args = (hashlib.md5(data["new_password"].encode()).hexdigest(),
                          data["email"],
                          hashlib.md5(data["password"].encode()).hexdigest())
            err, result = query_db(query, query_args)
            return jsonify(result)
        else:
            return not_found()
    else:
        return "Expected JSON"


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
