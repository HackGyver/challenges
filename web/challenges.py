# -*- coding: utf-8 -*-
"""

    Definition of all the routes for Challenge

"""


from flask import render_template
from flask.ext import login
from web.database import Challenge, Category
from web import webapp
from web import webdb as db


@webapp.route('/challenges/')
def show_challenges():
    """Query all the categories (which contains the challenges)"""

    categories = db.session.query(Category).all()

    return render_template('challenges.html', categories=categories)


@webapp.route('/challenges/<int:id>')
def show_challenge(id):
    """Query one specific challenge"""

    challenge = db.session.query(Challenge).filter(Challenge.id==id).first()

    return render_template('challenge.html',
            challenge=challenge,
            user=login.current_user
    )
