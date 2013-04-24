# -*- coding: utf-8 -*-
"""

    Definition of all the routes for Challenge

"""


from flask import request, render_template, redirect, url_for
from flask.ext import wtf, login
from web.database import Challenge, Category, Tag
from web import webapp
from web import webdb as db


class NewChallengeForm(wtf.Form):
    title = wtf.TextField('Title', [
        wtf.validators.Required(),
        wtf.validators.Length(max=64)
    ])
    description = wtf.TextAreaField('Description')
    level = wtf.SelectField('Level', [
            wtf.validators.Required(),
            wtf.validators.Length(max=1)
        ],
        choices=[(i, i) for i in range(1, 6)],
    )
    requirement = wtf.TextField('Requirement')
    flag = wtf.TextField('Flag', [
        wtf.validators.Required(),
        wtf.validators.Length(max=256)
    ])
    url = wtf.TextField('URL', [
        wtf.validators.Required(),
        wtf.validators.Length(max=256)
    ])
    categories = wtf.SelectField('Categories',
        choices=[(categorie.id, categorie.name) \
            for categorie in db.session.query(Category).all()]
    )
    tags = wtf.SelectField('Tags',
        choices=[(tag.id, tag.label) \
            for tag in db.session.query(Tag).all()]
    )

    def validate(self):
        # None is a string? o0
        if self.categories.data and self.categories.data != 'None':
            for id in self.categories.data:
                if not db.session.query(Category).filter_by(id=id).first():
                    return False
        # None is a string? o0
        if self.tags.data and self.tags.data != 'None':
            for id in self.tags.data:
                if not db.session.query(Tag).filter_by(id=id).first():
                    return False
        return True

    def apply_request(self):
        new_challenge = Challenge()
        new_challenge.title = self.title.data
        new_challenge.description = self.description.data
        new_challenge.level = self.level.data
        new_challenge.requirement = self.requirement.data
        new_challenge.flag = self.flag.data
        new_challenge.url = self.url.data
        if self.categories.data != 'None':
            categories = [
                    db.session.query(Category).filter_by(id=id).first() \
                            for id in self.categories.data
            ]
            new_challenge.categories = categories
        if self.tags.data != 'None':
            tags = [
                    db.session.query(Tag).filter_by(id=id).first() \
                            for id in self.tags.data
            ]
            new_challenge.tags = tags
        new_challenge.users = [login.current_user]
        db.session.add(new_challenge)
        db.session.commit()


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


@webapp.route('/challenges/new/', methods=['GET', 'POST'])
def manage_challenge():
    if not login.current_user.is_authenticated():
        return redirect(url_for('index'))

    form = NewChallengeForm(request.form)
    if form.validate_on_submit():
        form.apply_request()
        return 'Ok'

    return render_template('form.html', form=form)
