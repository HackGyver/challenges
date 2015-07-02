# -*- coding: utf-8 -*-
"""

    Define the reoutes, forms, etc. to manage user's profile

"""

from flask import request, render_template, url_for, redirect, flash
from flask.ext import login
from flask.ext.wtf import Form
from wtforms import PasswordField, validators
from web import webapp
from web import webdb as db
from database import User, Challenge


class SettingsForm(Form):
    new_password = PasswordField('New password', [
        validators.Required(),
        validators.Length(max=256)
    ])

    def validate(self):
        if not self.new_password or not self.new_password.data:
            self.new_password.errors = tuple(['Enter a new password'])
            return False

        return True

    def apply_request(self):
        login.current_user.password = self.new_password.data
        db.session.add(login.current_user)
        db.session.commit()


@webapp.route('/settings/', methods=['GET', 'POST'])
def show_settings():
    """Settings management"""

    if not login.current_user.is_authenticated():
        flash('You must be authenticated', 'error')
        return redirect(url_for('show_challenges'), user=login.current_user)

    form = SettingsForm(request.form)
    if form.validate_on_submit():
        form.apply_request()
        flash('Password updated', 'success')
        return redirect(url_for('show_settings', user=login.current_user))

    return render_template('form.html',
            form=form,
            user=login.current_user
    )


@webapp.route('/validate/<int:id>/', methods=['POST'])
def validate_challenge(id):
    """Test if it is the right flag and validate the challenge"""

    challenge = db.session.query(Challenge).filter(Challenge.id==id).first()
    if not challenge:
        flash('Challenge not found', 'error')
    else:
        if request.method == 'POST':
            if request.form.has_key('flag') \
                    and request.form['flag'] == challenge.flag:
                login.current_user.validated.append(challenge)
                db.session.add(login.current_user)
                db.session.commit()
                flash('Challenge validated', 'success')
            else:
                flash('Incorrect flag', 'error')
    return redirect(url_for('show_challenge', id=id))
