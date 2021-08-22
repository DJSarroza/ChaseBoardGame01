
import secrets
import os
import utility
import ast
import copy

from sqlalchemy import func
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, GenerateStoryForm

# Game Session stuff
from flask_app.models import    User,                           \
                                Post,                           \
                                GameSessions

# Game Mechanics stuff
#from flask_app.models import


# ==================================================================================
# [1]   Web Application Page Routes

@app.route("/")
@app.route("/home")
def home():
    #random_hex = secrets.token_hex(24)

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', title='Home Page', posts=posts)

# ============================


@app.route("/about")
def about():
    return render_template('about.html', title='About ISLA.online')


# ============================


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #    flash(f'Attempting to register.', 'info')
    #    return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password
                    )
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created.', 'success')
        return redirect(url_for('login'))

    else:
        # flash(f'Registration Unsuccessful.','danger')
        pass

    return render_template('register.html', title='Register', form=form)


# ============================

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged-in.', 'info')
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login Successful', 'success')
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and/or password', 'danger')
    return render_template('login.html', title='Login', form=form)

# ============================

@app.route("/logout")
def logout():
    logout_user()
    flash(f'Logout Successful', 'success')
    return redirect(url_for('home'))

# ============================

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # posts = Post.query.order_by(Post.date_posted.desc()).all()
    # return render_template('home.html',title='Home Page',posts=posts)

    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html',
                           title='Account Information',
                           profile_image_file=profile_image_file,
                           form=form
                           )

# ============================

@app.route("/game_lobby")
@login_required
def game_lobby():

    if current_user.is_authenticated:
        current_username = current_user.username

        # [0] Arguments

        # [1] Initial Queries
        found_game_sessions = db.session.query(GameSessions) \
            .filter(GameSessions.host_username == current_username) \
            .filter(GameSessions.status not in ["CLOSED", "CANCELLED"]) \
            .distinct() \
            .order_by(GameSessions.date_created.desc()) \
            .all()

        if found_game_sessions:
            session_code = found_game_sessions[0].session_code
        else:
            session_code = ""
        return render_template('game_lobby.html',
            title='Game Lobby',
            current_username=current_username,
            session_code=session_code)


    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        return render_template('home.html', title='Home Page', posts=posts)

# ============================

@app.route("/game_board")
@login_required
def game_board():
    return render_template('game_board.html', title='Game Board')

# ============================

# ==================================================================================
# [2]   API Endpoints
# [2.1] + Game Session APIs

@app.route('/_create_game_session')
@login_required
def create_game_session():
    if current_user.is_authenticated:
        current_username = current_user.username

        # [0] Arguments
        #domain_id = request.args.get('domain_id')

        # [1] Initial Queries
        found_game_sessions = db.session.query(GameSessions) \
            .filter(GameSessions.host_username == current_username) \
            .filter(GameSessions.status not in ["CLOSED", "CANCELLED"]) \
            .distinct() \
            .order_by(GameSessions.date_created.asc()) \
            .all()

        print("[DEBUG] --------")
        if not found_game_sessions:
            print(datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S") + ": No sessions found for '"+current_username+"', creating a game session.")

            new_game_session_code = secrets.token_urlsafe(4).upper()
            new_game_session = GameSessions(
                session_code = new_game_session_code,
                host_username = current_username
            )
            db.session.add(new_game_session)

            current_username = current_user.username
            found_user = db.session.query(User) \
                .filter(User.username == current_username) \
                .first()

            found_user.joined_game_session = new_game_session_code
            db.session.commit()

        else:
            print(datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S") + ": Found existing sessions for '" + current_username + "': ")
            for something in found_game_sessions:
                print("    " + something.session_code + " : " + something.status)

        print("[END DEBUG] ----")

        return jsonify(result=str(0))

    else:
        abort(400)

# ==============
@app.route('/_join_game_session')
@login_required
def join_game_session():
    if current_user.is_authenticated:
        # [0] Arguments
        game_session_code = request.args.get('game_session_code')

        # [1] Initial Queries
        current_username = current_user.username
        found_user = db.session.query(User) \
            .filter(User.username == current_username) \
            .first()

        found_user.joined_game_session = game_session_code
        db.session.commit()

        #return render_template('game_board.html', title='Game Board')
        #return redirect(url_for('game_board'))
        return jsonify(result=str(0))

    else:
        abort(400)


# [2.2] + Game Mechanics APIs


# [2.X] + Reporting and Analytics APIs



# ============================
