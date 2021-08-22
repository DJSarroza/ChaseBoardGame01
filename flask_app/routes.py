
import secrets
import os
import utility
import ast
import copy

from sqlalchemy import func

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from flask_app.models import    User,                           \
                                Post



# ==================================================================================
@app.route("/")
@app.route("/home")
def home():
    #random_hex = secrets.token_hex(24)

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', title='Home Page', posts=posts)

# ==================================================================================

@app.route("/about")
def about():
    return render_template('about.html', title='About ISLA.online')


# ==================================================================================
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


# ==================================================================================
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



# ==================================================================================
@app.route("/logout")
def logout():
    logout_user()
    flash(f'Logout Successful', 'success')
    return redirect(url_for('home'))



