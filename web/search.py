# -*- coding: utf-8 -*-
"""

    Definition of the search requests

"""

from sets import Set
from flask import request, render_template
from flask.ext import login
from wtforms import Form, TextField, SelectField
from web.database import Category, Challenge
from web import webapp
from web import webdb as db


class SearchForm(Form):
    challenges = TextField('Challenges')
    categories = SelectField('Categories',
            choices=[(category.id, category.name) \
                    for category in db.session.query(Category).all()]
    )
    tags = TextField('Tags')

    def validate(self):
        return True

    def apply_request(self):
        challenges = db.session.query(Challenge).all()
        result = Set()
        for challenge in challenges:
            for title in self.challenges.data:
                if title in challenge.title:
                    result.update([challenge])
                    break
            for category in challenge.categories:
                if self.categories.data in category.name:
                    result.update([challenge])
                    break
            for label in self.tags.data.split():
                for tag in challenge.tags:
                    if label in tag.label:
                        result.update([challenge])
                        break
        return result


@webapp.route('/search/', methods=['GET', 'POST'])
def search():
    """Search request"""

    form = SearchForm(request.form)
    if form.validate_on_submit():
        results = form.apply_request()
        return render_template('search.html',
                results=results,
                user=login.current_user
        )

    return render_template('form.html',
            form=form,
            user=login.current_user
    )
