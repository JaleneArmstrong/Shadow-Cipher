from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/sensei', methods=['GET'])
def admin():
    return render_template('sensei.html')

# Moved From login.py view
@index_views.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

# Moved From signup.py view
@index_views.route('/signup_page', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@index_views.route('/healthcheck', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})