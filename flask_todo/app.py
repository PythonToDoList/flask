"""Entire flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

DATE_FMT = '%d/%m/%Y %H:%M:%S'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    note = db.Column(db.Unicode)
    creation_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    profile = db.relationship("Profile", back_populates='tasks')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'creation_date': self.creation_date.strftime(DATE_FMT),
            'due_date': self.due_date.strftime(DATE_FMT) if self.due_date else None,
            'completed': self.completed,
            'profile_id': self.profile_id
        }

    def __repr__(self):
        return "<Task: {} | owner: {}>".format(self.name, self.profile.username)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    tasks = db.relationship("Task", back_populates='profile')

    def to_dict(self):
        """Get the object's properties as a dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined.strftime(DATE_FMT),
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __repr__(self):
        return "<Profile: {} | tasks: {}>".format(self.username, len(self.tasks))


@app.route('/api/v1')
def index():
    pass

@app.route('/api/v1/accounts')
def index():
    pass

@app.route('/api/v1/accounts/login')
def index():
    pass

@app.route('/api/v1/accounts/logout')
def index():
    pass

@app.route('/api/v1/accounts/<username>')
def index():
    pass

@app.route('/api/v1/accounts/<username>/tasks')
def index():
    pass

@app.route('/api/v1/accounts/<username>/tasks/<id:\d+>')
def index():
    pass
