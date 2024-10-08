from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from sqlalchemy.exc import IntegrityError

from App.controllers import get_curr_game
from App.database import db
from App.models import UserGuess
from datetime import datetime


game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/game', methods=['GET'])
@jwt_required()
def game():
    current_user = jwt_current_user
    today = datetime.utcnow().date()
    curr_game = get_curr_game()

    if not curr_game:
        return jsonify({"error" : "An error has occured whilst accessing today's game"}), 500

    guesses = UserGuess.get_guesses(curr_game.id, jwt_current_user.id)
    curr_game_json = curr_game.get_json()

    # Please don't mind my whompy logic, I aint smart okii
    if guesses:
        attempts_left = curr_game.max_attempts - len(guesses)
    else:
        attempts_left = curr_game.max_attempts

    # Evaluate the last guess to get the guess results
    prev_guess = guesses[-1].guess if guesses else None
    verdict = curr_game.evaluateGuess(prev_guess) if prev_guess else None

    # Checking if the player has achieved victory!
    victory = None
    if verdict and verdict['bulls'] == 4:
        victory = "Congratulations! You've Obtained Victory!"
    elif (attempts_left == 0):
        victory = "You Have Lost. Chin Up And Return Tomorrow!"

    # Attaching labels to each digit in the guesses
    # Probably whomp logic but I tried :~)
    labeled_guesses = []
    if guesses and verdict:
        # Editted to use list comprehension - Sky
        labeled_guesses = [curr_game.attachLabels(guess.guess, curr_game.answer) for guess in guesses]
    
    return render_template('game.html', 
                            curr_game=curr_game_json, 
                            today=today, 
                            guesses=guesses, 
                            verdict=verdict,
                            victory=victory,
                            attempts_left=attempts_left,
                            labeled_guesses=labeled_guesses,
                            current_user=current_user)

@game_views.route('/evaluate_guess', methods=['POST'])
@jwt_required()
def evaluateGuess():
    user = jwt_current_user
    curr_game = get_curr_game()

    user_id = user.id
    game_id = curr_game.id
    guess_digits = []

    # Check if any digit is repeated
    for i in range(curr_game.answer_length):
        guess_digit = request.form.get(f'guess-digit-{i}')

        if guess_digit == '0' and i == 0:
            flash('Zero Cannot Be The First Number!')
            return redirect(request.referrer)

        if guess_digit in guess_digits:
            flash('No Duplicate Numbers!')
            return redirect(request.referrer)

        

        guess_digits.append(guess_digit)

    # Construct the guess string
    guess = ''.join(guess_digits)

    try:
        user_guess = UserGuess(user_id=user_id, game_id=game_id, guess=guess)
        db.session.add(user_guess)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Failed To Submit Guess."}), 400

    return redirect(request.referrer)

from flask import render_template_string, Markup

@game_views.route('/help_me', methods=['GET'])
@jwt_required()
def helpMe():
    tooltip = "Click Here To Go To How To Play Page"
    howtoplay_route = "/howtoplay"
    flash_message = ('<br>Shuriken - Correct<br>'
                     'Kunai - Correct, But...<br>'
                     'Smoke - Wrong<br>'
                     f'<a href="{howtoplay_route}" title="{tooltip}" style="color: #CD6240">Need More?</a>')
    flash(Markup(flash_message))
    return redirect(request.referrer)

