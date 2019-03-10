from flask import Flask
app = Flask(__name__)

from api import articles
from api import comments
from api import users
