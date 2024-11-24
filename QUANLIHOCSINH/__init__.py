from datetime import timedelta

import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "hnt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:594362@localhost/QUANLIHOCSINH"
app.config["PAGE_SIZE"] = 1



# app.config['SESSION_COOKIE_NAME'] = 'my_session_cookie'
app.config['SESSION_COOKIE_HTTPONLY'] = True



db = SQLAlchemy(app = app )

login = LoginManager(app =app)



cloudinary.config(
    cloud_name = "ddkpaw2gy",
    api_key = "622254564989568",
    api_secret = "wAoO0Elvy5y-SWqpsjQNw43PRt0",
    secure=True
)

