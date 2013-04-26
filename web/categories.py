# -*- coding: utf-8 -*-
"""

    Definition of all the routes for Category

"""


from flask import render_template
from flask.ext import login
from web.database import Category
from web import webapp
from web import webdb as db


@webapp.route('/categories/')
def show_categories():
    """Query all the categories"""

    categories = db.session.query(Category).order_by(Category.name).all()

    return render_template('categories.html',
            categories=categories,
            user=login.current_user
    )


@webapp.route('/categories/<name>/')
def show_category(name):
    """Query one specific category"""

    category = db.session.query(Category).filter(Category.name==name).first()

    return render_template('category.html',
            category=category,
            user=login.current_user
    )
