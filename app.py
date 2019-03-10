#! flask/bin/python
from flask import Flask

app = Flask(__name__)

from api import articles
from api import comments
from api import users

@app.route('/')
def index():
    return "Hello there!"

if __name__ == '__main__':
    app.run(debug=True)
