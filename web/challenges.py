# -*- coding: utf-8 -*-
"""

    Definition of all the routes for Challenge

"""


from ast import literal_eval
from flask import request, render_template, redirect, url_for, flash
from flask.ext import wtf, login
from web.database import Challenge, Category, Tag
from web import webapp
from web import webdb as db


class ManageChallengeForm(wtf.Form):
    id = wtf.HiddenField('', [
        wtf.validators.Required()
    ])
    title = wtf.TextField('Title', [
        wtf.validators.Required(),
        wtf.validators.Length(max=64)
    ])
    description = wtf.TextAreaField('Description')
    # TODO:
    #   -field must be a number
    #   -number must be a valid level value
    level = wtf.SelectField('Level', [
            wtf.validators.Required(),
            wtf.validators.Length(max=1)
        ],
        choices=[(i, i) for i in range(1, 6)],
    )
    # TODO:
    #   -field must be a number
    #   -number must be a valid challenge id
    requirement = wtf.TextField('Requirement')
    flag = wtf.TextField('Flag', [
        wtf.validators.Required(),
        wtf.validators.Length(max=256)
    ])
    url = wtf.TextField('URL', [
        wtf.validators.Required(),
        wtf.validators.Length(max=256)
    ])
    # TODO: enable multiple selection
    categories = wtf.SelectField('Categories',
        choices=[(categorie.id, categorie.name) \
            for categorie in db.session.query(Category).all()]
    )
    # TODO: enable multiple selection
    tags = wtf.SelectField('Tags',
        choices=[(tag.id, tag.label) \
            for tag in db.session.query(Tag).all()]
    )

    def validate(self):
        if not self.title or not self.title.data:
            self.title.errors = tuple(['This field is required.'])
            return False

        if not self.level or not self.level.data:
            self.level.errors = tuple(['This field is required.'])
            return False

        if not self.flag or not self.flag.data:
            self.flag.errors = tuple(['This field is required.'])
            return False

        if not self.url or not self.url.data:
            self.url.errors = tuple(['This field is required.'])
            return False

        if self.id.data \
                and literal_eval(self.id.data):
            challenge = db.session.query(Challenge).filter_by(id=self.id.data).first()
            if not challenge:
                self.id.errors = tuple(['Unknow challenge'])
                return False
            elif not login.current_user in challenge.authors:
                self.id.errors = tuple([
                    'You are not the author of the challenge'
                ])
                return False

        if self.categories.data \
                and literal_eval(self.categories.data):
            for id in self.categories.data:
                if not db.session.query(Category).filter_by(id=id).first():
                    self.categories.errors = tuple([
                        'Unknown category'
                    ])
                    return False

        if self.tags.data and self.tags.data != 'None' \
                and literal_eval(self.tags.data):
            for id in self.tags.data:
                if not db.session.query(Tag).filter_by(id=id).first():
                    self.tags.errors = tuple([
                        'Unknow tag'
                    ])
                    return False
        return True

    def apply_request(self):
        new_challenge = None
        if self.id.data and literal_eval(self.id.data):
            new_challenge = \
                    db.session.query(Challenge).filter_by(id=self.id.data).first()
        if not new_challenge:
            new_challenge = Challenge()
        new_challenge.title = self.title.data
        new_challenge.description = self.description.data
        new_challenge.level = self.level.data
        new_challenge.requirement = self.requirement.data
        new_challenge.flag = self.flag.data
        new_challenge.url = self.url.data
        if self.categories.data != 'None' \
                and literal_eval(self.categories.data):
            categories = [
                    db.session.query(Category).filter_by(id=id).first() \
                            for id in self.categories.data
            ]
            new_challenge.categories = categories
        if self.tags.data != 'None' and literal_eval(self.tags.data):
            tags = [
                    db.session.query(Tag).filter_by(id=id).first() \
                            for id in self.tags.data
            ]
            new_challenge.tags = tags
        new_challenge.authors.append(login.current_user)
        db.session.add(new_challenge)
        db.session.commit()


@webapp.route('/challenges/')
def show_challenges():
    """Query all the categories (which contains the challenges)"""

    categories = db.session.query(Category).all()

    return render_template('challenges.html',
            categories=categories,
            user=login.current_user
    )


@webapp.route('/challenges/<int:id>')
def show_challenge(id):
    """Query one specific challenge"""

    challenge = db.session.query(Challenge).filter(Challenge.id==id).first()

    return render_template('challenge.html',
            challenge=challenge,
            user=login.current_user
    )


@webapp.route('/challenges/new/', methods=['GET', 'POST'])
def create_challenge():
    if not login.current_user.is_authenticated():
        flash('You must be authenticated', 'error')
        return redirect(url_for('index'), user=login.current_user)

    form = ManageChallengeForm(request.form)
    if form.validate_on_submit():
        form.apply_request()
        flash('New challenges has been created', 'success')
        return redirect(url_for('show_challenges'), user=login.current_user)

    return render_template('form.html',
            form=form,
            user=login.current_user
    )


@webapp.route('/challenges/edit/<int:id>', methods=['GET', 'POST'])
def edit_challenge(id):
    if not login.current_user.is_authenticated():
        flash('You must be authenticated', 'error')
        return redirect(url_for('index'), user=login.current_user)

    challenge = db.session.query(Challenge).filter(Challenge.id==id).first()
    if not challenge:
        flash('Unknow challenge', 'warning')
        return redirect(url_for('index'), user=login.current_user)

    if not login.current_user in challenge.authors:
        flash("You can't edit this challenge", 'warning')
        return redirect(url_for('index'), user=login.current_user)

    form = ManageChallengeForm(request.form, obj=challenge)
    if form.validate_on_submit():
        form.apply_request()
        flash('Challenge has been edited', 'info')
        return redirect(url_for('show_challenge', id=id))

    return render_template('form.html',
            form=form,
            user=login.current_user
    )
