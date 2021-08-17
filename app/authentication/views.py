from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, LoginForm
from ..email import mail_message
from .. import db
from . import authentication

@authentication.route('/', methods = ['GET', 'POST'])
def login():
    
    if request.form:
        uname = request.form['username']
        password = request.form['password']

        if uname != "" or password !="":
            user = User.query.filter_by(username = uname).first()
            # print(user.username)
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.home'))
            else:
                flash('Invalid username or password')
        else:
            flash('Please fill in proper details')

    title = "Login"
    return render_template('authentication/login.html', title = title)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))

@authentication.route('/register', methods = ['GET', 'POST'])
def register():
    if request.form:
        fname = request.form['firstName']
        print(fname)
        lname = request.form['lastName']
        uname = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpass = request.form['confirmPassword']

        if not email or not email.strip() or '@' not in email:
            flash('Please put in a valid email')
        elif fname != "" or lname != "" or uname != "" or password != "" or cpass != "":
            if uname == User.query.filter_by(username = uname).first():
                flash('Please pick a different username')
            elif password == cpass:
                password1 = generate_password_hash(password)
                user = User(firstname = fname, secondname = lname, username = uname, email = email, secured_password = password1)
                db.session.add(user)
                db.session.commit()
                mail_message("Karibu Thoughts", "email/karibu", user.email, user = user)
                return redirect(url_for('authentication.login'))
            else:
                flash('Your passwords do not match')
        else:
            flash("Fill all the fields")

    title = "New Account"
    return render_template('authentication/registration.html', title = title)







    


