from flask import Flask, redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('register.html')



@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/sightings")


@app.route('/user/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email/password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password.")
        return redirect('/')
    

    session['user_id'] = user_in_db.id
    return redirect('/sightings')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

