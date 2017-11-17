"""Entire flask app."""
from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from functools import wraps
import json
import os
from passlib.hash import pbkdf2_sha256 as hasher
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
auth = HTTPTokenAuth(scheme='Token')
db = SQLAlchemy(app)


from .models import Task, Profile


@app.route('/api/v1')
def index():
    """List of routes for this API."""
    output = {
        'info': 'GET /api/v1',
        'register': 'POST /api/v1/accounts',
        'single profile detail': 'GET /api/v1/accounts/<username>',
        'edit profile': 'PUT /api/v1/accounts/<username>',
        'delete profile': 'DELETE /api/v1/accounts/<username>',
        'login': 'POST /api/v1/accounts/login',
        'logout': 'GET /api/v1/accounts/logout',
        "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
        "create task": 'POST /api/v1/accounts/<username>/tasks',
        "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
        "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
        "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
    }
    response = jsonify(output)
    return response


def get_profile(username):
    """Check if the requested profile exists."""
    return Profile.query.filter_by(username=username).first()


@auth.verify_token
def verify_token(token):
    if token:
        username = token.split(':')[0]
        profile = get_profile(username)
        return True


def authenticate(response, profile):
    token = f'{profile.username}:{profile.token}'
    response.set_cookie('auth_token', value=token)
    return response


@app.route('/secret')
@auth.login_required
def secret():
    return jsonify({'status': 'success'})


@app.route('/api/v1/accounts', methods=['POST'])
def register():
    """Add a new user profile if it doesn't already exist."""
    needed = ['username', 'email', 'password', 'password2']
    if all([key in request.form for key in needed]):
        username = request.form['username']
        profile = get_profile(username)
        if not profile:
            if request.form['password'] == request.form['password2']:
                new_profile = Profile(
                    username=username,
                    email=request.form['email'],
                    password=hasher.hash(request.form['password']),
                    date_joined=datetime.now(),
                    token=secrets.token_urlsafe(64)
                )
                db.session.add(new_profile)
                db.session.commit()

                response = Response(
                    response=json.dumps({"msg": 'Profile created'}),
                    status=201,
                    mimetype="application/json"
                )
                return authenticate(response, new_profile)

            response = jsonify({"error": "Passwords don't match"})
            response.status_code = 400
            return response

        response = jsonify({'error': f'Username "{username}" is already taken'})
        response.status_code = 400
        return response

    response = jsonify({'error': 'Some fields are missing'})
    response.status_code = 400
    return response


@app.route('/api/v1/accounts/login', methods=['POST'])
def login():
    """Authenticate a user."""
    needed = ['username', 'password']
    if all([key in request.forms for key in needed]):
        profile = get_profile(request.forms['username'])
        if profile and hasher.verify(request.forms['password'], profile.password):
            response = Response(
                response=json.dumps({'msg': 'Authenticated'}),
                mimetype="application/json",
                status=200
            )
            return authenticate(response, profile)
        response.status_code = 400
        return {'error': 'Incorrect username/password combination.'}
    response.status_code = 400
    return {'error': 'Some fields are missing'}


@app.route('/api/v1/accounts/logout')
def logout():
    """Log a user out."""
    return jsonify({'msg': 'Logged out.'})


@app.route('/api/v1/accounts/<username>')
@auth.login_required
def profile_detail(username):
    profile = get_profile(username)
    if profile:
        response = Response(
            mimetype="application/json",
            response=json.dumps(profile.to_dict()),
        )
        return authenticate(response, profile)
    response = Response(
        mimetype="application/json",
        response=json.dumps({'error': 'You do not have permission to access this profile.'}),
        status=403
    )
    return response

# @app.route('/api/v1/accounts/<username>/tasks')
# def index(username):
#     pass

# @app.route('/api/v1/accounts/<username>/tasks/<task_id:\d+>')
# def index(username, task_id):
#     pass
