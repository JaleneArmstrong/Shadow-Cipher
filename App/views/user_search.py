from flask import Blueprint, abort, render_template, jsonify, request, send_from_directory, flash, redirect, url_for

from App.database import db
from App.models import Game, User, UserGuess
from datetime import datetime

user_search_views = Blueprint('user_search_views', __name__, template_folder='../templates')

@user_search_views.route("/user_search")
def user_search():
    abort(501)
