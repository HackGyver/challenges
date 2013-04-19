# -*- cpding: utf-8 *-*
"""

    Definition of all the routes for Challenge

"""


from flask import render_template
from web.database import Challenge
from web import webapp
from web import webdb as db


@webapp.route('/challenges/')
def show_challenges():
    """Query all the challenges"""

    challenges = db.session.query(Challenge).all()

    return render_template('challenges.html', challenges=challenges)


@webapp.route('/challenges/<int:id>')
def show_challenge(id):
    """Query one specific challenge"""

    challenge = db.session.query(Challenge).filter(Challenge.id==id).first()

    return render_template('challenge.html', challenge=challenge)
