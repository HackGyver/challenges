# -*- coding: utf-8 -*-
"""

    Definition of all the routes for Category

"""


from flask import render_template
from web.database import Category
from web import webapp
from web import webdb as db


@webapp.route('/categories/')
def show_categories():
    """Query all the categories"""

    categories = db.session.query(Category).order_by(Category.name).all()

    return render_template('categories.html', categories=categories)


@webapp.route('/categories/<int:id>')
def show_category(id):
    """Query one specific category"""

    category = db.session.query(Category).filter(Category.id==id).first()

    return render_template('category.html', category=category)
