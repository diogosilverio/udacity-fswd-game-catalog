import base64
from flask import request, flash, redirect, session

from catalog import app
from catalog.services.user_service import UserService
from catalog.services.facebook_service import FacebookService


@app.route('/login')
def login():
    code = request.args.get('code')

    user = UserService().fetch_or_create(FacebookService().authenticate(code))

    if user:
        new_session(user)
    else:
        session.clear

    return_path = request.referrer or '/'

    return redirect(return_path)


@app.route('/logout')
def logout():

    if 'user' in session:
        user = session['user']['name']
        session.pop('user', None)
        flash("Goodbye, %s!" % user, 'login')

    return redirect('/')


@app.route('/auth')
def facebook_login():
    return redirect(FacebookService().login_url())


def new_session(user):
    session['user'] = user.to_json()
    flash("Welcome, %s!" % user.name, 'login')
