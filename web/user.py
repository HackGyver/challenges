# -*- coding: utf-8 -*-
"""

    Define the reoutes, forms, etc. to manage user's profile

"""

from flask import request, render_template, url_for, redirect, flash
from flask.ext import wtf, login
from web import webapp
from web import webdb as db
from database import User


class SettingsForm(wtf.Form):
    new_password = wtf.PasswordField('New password', [
        wtf.validators.Required(),
        wtf.validators.Length(max=256)
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
        return redirect(url_for('index'), user=login.current_user)

    form = SettingsForm(request.form)
    if form.validate_on_submit():
        form.apply_request()
        flash('Password updated', 'success')
        return redirect(url_for('show_settings', user=login.current_user))

    return render_template('form.html',
            form=form,
            user=login.current_user
    )
