# -*- coding: utf-8 -*-
"""

    Define the models of the database, using SQLAlchemy.

"""


import time
from web import webdb as db


# Many-to-many relationship between User and Challenge (for authors)
created = db.Table('created',
        db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Many-to-many relationship between User and Challenge (for scores)
validated = db.Table('validated',
        db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


# Many-to-many relationship between Category and Challenge
categories = db.Table('categories',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
        db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
)


# Many-to-many relationship between Tag and Challenge
tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    salt = db.Column(db.String(32), default=str(time.time()))
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    # Contains the list of challenges created by the user
    created = db.relationship('Challenge', secondary=created,
            backref=db.backref('authors', lazy='dynamic'))

    # Contains the list of challenges validated by the user
    validated = db.relationship('Challenge', secondary=validated,
            backref=db.backref('validated', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.admin

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "User('%s')" % (self.username)


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.Integer, nullable=False)
    requirement = db.Column(db.Integer)
    flag = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(256), nullable=False)

    categories = db.relationship('Category', secondary=categories,
            backref=db.backref('challenges', lazy='dynamic'))

    tags = db.relationship('Tag', secondary=tags,
            backref=db.backref('challenges', lazy='dynamic'))

    def __repr__(self):
        return "Challenge('%s')" % (self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return "Category('%s')" % (self.name)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64))

    def __repr__(self):
        return "Tag('%s')" % (self.label)


# Creation of the database
db.create_all()
