# -*- coding: utf-8 -*-
"""

    Definition of the admin views

"""


from flask.ext import admin, login
from flask.ext.admin.contrib import sqlamodel
from web import webapp
from web import webdb as db
from database import User, Challenge, Category, Tag


# TODO: - add view specifications for each model view
class UserAdminView(sqlamodel.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session):
        super(UserAdminView, self).__init__(User, session)

class ChallengeAdminView(sqlamodel.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # Invisible column in the list view
    column_exclude_list = ['description']

    def __init__(self, session):
        super(ChallengeAdminView, self).__init__(Challenge, session)


class CategoryAdminView(sqlamodel.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session):
        super(CategoryAdminView, self).__init__(Category, session)


class TagAdminView(sqlamodel.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session):
        super(TagAdminView, self).__init__(Tag, session)


class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create admin
admin = admin.Admin(webapp, 'Admin Panel', index_view=MyAdminIndexView())
# Add views
admin.add_view(UserAdminView(db.session))
admin.add_view(ChallengeAdminView(db.session))
admin.add_view(CategoryAdminView(db.session))
admin.add_view(TagAdminView(db.session))
