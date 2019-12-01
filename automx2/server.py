"""
Flask server application.
"""
from flask import Flask

from automx2.config import config
from automx2.model import db
from automx2.views.autoconfig import MailConfig
from automx2.views.database import InitDatabase
from automx2.views.site import SiteRoot

MOZILLA_CONFIG_ROUTE = '/mail/config-v1.1.xml'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri()
app.config['SQLALCHEMY_ECHO'] = config.db_echo()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.add_url_rule('/', view_func=SiteRoot.as_view('root'), methods=['GET'])
app.add_url_rule('/initdb/', view_func=InitDatabase.as_view('initdb'), methods=['GET'])
app.add_url_rule(MOZILLA_CONFIG_ROUTE, view_func=MailConfig.as_view('mailcfg'), methods=['GET'])

db.init_app(app)