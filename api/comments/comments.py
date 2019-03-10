import datetime
import hashlib
import sqlite3
import flask
from flask import g
from flask import Response
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATABASE = '../../db/master.db'

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
        comment_id = {"comment_id": ""}

        #using with automatically commits
        try:
            with cur:
                cursor.execute(query, args)
                rv = cursor.fetchall()

                #gets the rowID of the last inserted row so we can get the url to the post
                comment_id["comment_id"] = str(cursor.lastrowid)

            cur.close()
        except Exception as err:
            return [{"error": str(err), "query": query,}]

        if cursor.rowcount == 0:
            return not_found()
        elif int(comment_id["comment_id"]) != 0:
            return comment_id
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

# app.route('/', methods=['GET','POST'])
# def home():
#     return '''<h1>Comments microservice</h1>
# <p>A prototype API for posting, retrieving, and deleting comments.</p>'''
#

@app.route('/comments/all', methods=['GET'])
def comments_all():

    query = 'SELECT * FROM comments;'
    query_args = ("")

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return not_found()

    return result

@app.route('/comments/nth_comment/<int:nth>', methods=['GET'])
def get_nth_comments(nth):

    query = 'SELECT * FROM comments WHERE comment_id BETWEEN 0 AND ?;'
    #query = 'SELECT * FROM comments ORDER BY comment_id LIMIT ?'
    # note that ORDER BY should be by date
    query_args = (nth,)

    resp = query_db(query, query_args)
    result = jsonify(resp)

    if len(resp) > 0:
        result.status_code = 200
        result.content_type = "application/json"
    else:
        return "404"

    return result

#use postman or curl
@app.route('/comments/post', methods=['POST'])
def post_comment():
     if request.is_json:
        content = request.get_json()

        query_args = (content["user_id"], content["comment"], str(datetime.date.today()))
        query = "INSERT INTO comments (user_id, comment, comment_date) VALUES (?, ?, ?)"

        result = query_db(query, query_args)
        resp = jsonify(result)
        resp.status_code = 201
        resp.headers['Location'] = f"/project1/{result['comment_id']}"
        return resp
     else:
        return "expected JSON"



@app.route('/comments/delete/<int:comment_ID>', methods=['DELETE'])
def comment_delete(comment_ID):
    query = "DELETE FROM comments WHERE comment_id = ?"
    query_args = (comment_ID,)

    result = query_db(query, query_args)
    if type(result) == flask.Response:
        return result
    else:
        resp = jsonify(result)
        resp.status_code = 200
        resp.content_type = "application/json"
        return resp


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
