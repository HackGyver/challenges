# -*- coding: utf-8 -*-
"""

    Main file for the web portal.

"""


from flask import render_template
from flask.ext import login
from web import webapp


@webapp.route('/')
def index():
    return render_template('index.html', user=login.current_user)
