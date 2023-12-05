from flask import *
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS, cross_origin

current_directory = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(current_directory, '../templates')
static_folder = os.path.join(current_directory, '../static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
CORS(app)

path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'rpg.db')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)