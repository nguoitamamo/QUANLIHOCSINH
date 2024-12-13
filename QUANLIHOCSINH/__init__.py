

import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "hnt"

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True


# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:594362@localhost/QUANLIHOCSINHFINAL"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/QUANLIHOCSINHFINAL" % quote('Admin@123')
app.config["PAGE_SIZE"] = 1

app.config["MAX_SS_LOP"] = 40

# app.config['SESSION_COOKIE_NAME'] = 'my_session_cookie'
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.config["15PHUT"] = 0.2
app.config["1TIET"] = 0.3
app.config["CUOIKY"] = 0.5

app.config["MAX_15PHUT"] = 5
app.config["MAX_1TIET"] = 3





db = SQLAlchemy(app = app )

login = LoginManager(app =app)



cloudinary.config(
    cloud_name = "ddkpaw2gy",
    api_key = "622254564989568",
    api_secret = "wAoO0Elvy5y-SWqpsjQNw43PRt0",
    secure=True
)

