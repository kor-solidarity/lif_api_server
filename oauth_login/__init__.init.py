from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import datetime
from itsdangerous import URLSafeSerializer

UPLOAD_SERVER = 'static'


app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://:' \
                                        '@localhost:4406' \
                                        '/?charset=utf8'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '',
        'secret': ''
    },
    'twitter': {
        'id': '',
        'secret': ''
    },
    'google': {
        'id': '',
        'secret': ''
    }
}

# 메일 시스템 폐지
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True


db = SQLAlchemy(app)
mail = Mail(app)

mail_serial = URLSafeSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager(app)
login_manager.login_view = None

from .player import views, admin, queues, find_enemy
