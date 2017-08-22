# app/models.py
from app import db


class User(db.Model):
    """Class defining User model."""

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    bucketlists = db.relationship(
        'Bucketlist')
    session = db.relationship(
        'Session'
    )


class Bucketlist(db.Model):
    """Class defining Bucketlist model."""

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50), unique=True)
    status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    items = db.relationship(
        'BucketlistItems')


class BucketlistItems(db.Model):
    """Class defining Bucketlist items model."""

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(50), unique=True)
    status = db.Column(db.Boolean)
    bucket_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))
    bucketlist = db.relationship('Bucketlist',
                           backref=db.backref('bucketlistitems', cascade="all, delete-orphan"),
                           lazy='joined')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class Session(db.Model):
    """Class defining Session model."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.public_id))
    token = db.Column(db.String(256))
