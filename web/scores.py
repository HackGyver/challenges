# -*- coding: utf-8 -*-
"""

    Definition of the scores

"""


from flask import render_template
from flask.ext import login
from web.database import User, Challenge
from web import webapp
from web import webdb as db


@webapp.route('/scores/')
def show_scores():
    """Query all the users for displaying the scores"""

    users = db.session.query(User).all()
    scores = {}
    scores.update({user.id: sum([challenge.level \
            for challenge  in user.validated]) \
        for user in users
    })

    return render_template('scores.html',
            users=users,
            scores=scores,
            user=login.current_user
    )


@webapp.route('/scores/<int:id>')
def show_score(id):
    """Query a specific user for displaying his score"""

    spe_user = db.session.query(User).filter(User.id==id).first()
    score = sum([challenge.level for challenge in spe_user.validated])

    return render_template('score.html',
            spe_user=spe_user,
            score=score,
            user=login.current_user
    )
