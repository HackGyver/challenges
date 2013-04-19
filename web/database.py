# -*- coding: utf-8 -*-
"""

    Define the models of the database, using SQLAlchemy.

"""


from web import webdb as db


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    def __repr__(self):
        return "<User('%s')>" % (self.username)


# Creation of the database
db.create_all()
