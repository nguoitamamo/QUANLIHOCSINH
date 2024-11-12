from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "hnt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:594362@localhost/QUANLIHOCSINH"

db = SQLAlchemy(app = app )

login = LoginManager(app =app)

