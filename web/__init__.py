# -*- coding: utf-8 -*-
"""

    Global definitions for the application 'web'.
    'web' defines the web portal for the members.

"""


from flask import Flask
from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy


# Flask init
webapp = Flask(__name__)
webapp.config.from_pyfile('config.cfg')
# Flask-SQLAlchemy init
webdb = SQLAlchemy(webapp)


# Import your definition files here
# For instance:
#   import web.database
# It will import web.database which contains the definition models of the
# database of the portal
import web.main
import web.database
import web.login
import web.challenges
import web.admin
import web.scores
import web.search
import web.user
