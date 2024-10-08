import os
sensei = os.environ.get('SENSEI')
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.models import db
from App.controllers import create_user

from.index import index_views
from .game import game_views

from App.models import User

from App.controllers import (
    login,
    create_user
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''

@auth_views.route('/init', methods=['GET'])
def init():
    guess_digits = []

    for i in range(14):
        guess_digit = request.args.get(str(i))
        if guess_digit is not None:
            guess_digits.append(guess_digit)

    if guess_digits:
        guess_digits_str = ''.join(guess_digits)

        if guess_digits_str == sensei:
            db.drop_all()
            db.create_all()
            create_user('bob', 'bobpass')
            return render_template('201.html'), 201
        else:
            return render_template('401.html'), 401
    else:
        return render_template('401.html'), 401

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route('/login', methods=['POST'])
def login_action():
    response = None
    username = request.form['username']
    password = request.form['password']
    token = login(username, password)
    if token == None:
        flash('Bad Username Or Password Given'), 401
        response = redirect(url_for('index_views.index_page'))
        return response
    else:
        flash('Login Successful!')
        response = redirect(url_for('game_views.game'))
        set_access_cookies(response, token) 
        return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index_page')) 
    flash("Logged Out Successfully!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    user = create_user(data['username'], data['password'])
    
    if user:
        flash('Sign Up Successful!')
        response = redirect(url_for('index_views.login_page'))
    else:
        flash('Username Already Taken! Please Try Again'), 400
        response = redirect(url_for('index_views.signup_page'))
 
    return response

# '''
# API Routes
# '''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response
