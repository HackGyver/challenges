# -*- coding: utf-8 -*-
"""

    Define the routes, forms, etc. for login stuff.

"""


import hashlib
import time
from flask import request, render_template, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField
from flask.ext import login
from web import webapp
from web import webdb as db
from database import User


class LoginForm(Form):
    username = TextField('Username', [
        validators.Required(),
        validators.Length(max=64)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(max=256)
    ])

    def validate(self):
        user = self.get_user()

        if user is None:
            self.username.errors = tuple(['Unknow username'])
            return False

        hash_password = hashlib.sha512()
        hash_password.update(user.salt + self.password.data)
        if user.password != hash_password.hexdigest():
            self.password.errors = tuple(['Invalid password'])
            return False

        return True

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()


class RegistrationForm(Form):
    username = TextField('Username', [
        validators.Required(),
        validators.Length(max=64)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(max=256)
    ])

    def validate(self):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            self.username.errors = tuple(['Username already registered'])
            return False

        return True


# Flask-Login init
def init_login():
    login_manager = login.LoginManager()
    login_manager.setup_app(webapp)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@webapp.route('/login/', methods=['GET', 'POST'])
def login_view():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()
        login.login_user(user)
        flash('You were logged in', 'info')
        return redirect(url_for('show_challenges'))

    return render_template('form.html', form=form)


@webapp.route('/register/', methods=['GET', 'POST'])
def register_view():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User()

        form.populate_obj(user)
        user.salt = str(time.time())

        hash_password = hashlib.sha512()
        hash_password.update(user.salt + user.password)
        user.password = hash_password.hexdigest()

        db.session.add(user)
        db.session.commit()

        login.login_user(user)
        flash('You were registered', 'info')
        return redirect(url_for('show_challenges'))

    return render_template('form.html', form=form)


@webapp.route('/logout/')
def logout_view():
    login.logout_user()
    flash('You were logged out', 'info')
    return redirect(url_for('show_challenges'))


# Init Flask-Login
init_login()
