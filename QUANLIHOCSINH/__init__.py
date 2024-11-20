

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "hnt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:594362@localhost/QUANLIHOCSINH"
app.config["PAGE_SIZE"] = 1

db = SQLAlchemy(app = app )

login = LoginManager(app =app)

