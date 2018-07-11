from flask import Flask, render_template, session, request, redirect, flash
from flask_bcrypt import Bcrypt 
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[A-Za-z0-9]*$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "registrationKey"
mysql = connectToMySQL('registration')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/registration', methods=['POST'])
def registration():
    query ="SELECT email FROM users WHERE email = %(email)s;"
    data = { 'email' : request.form['email']}
    result = mysql.query_db(query, data)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    print(pw_hash)
    
    if result:
        flash('Email Already Exists!', 'email')
    elif len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email')

    if len(request.form['first_name']) < 2:
        flash('First Name cannot be blank!', 'first_name')
    if request.form['first_name'].isalpha() == False:
        flash('First Name must be characters only!', 'first_name')
    
    if len(request.form['last_name']) < 2:
        flash('Last Name cannot be blank!', 'last_name')
    if request.form['last_name'].isalpha() == False:
        flash('Last Name must be characters only!', 'last_name')

    if len(request.form['password']) < 8:
        flash('Password does not meet requirements!', 'password')
    if not PASSWORD_REGEX.match(request.form['password']):
        flash('Password does not meet requirements!', 'password')

    if request.form['confirm_password'] != request.form['password']:
        flash('Passwords do not match!', 'password', 'confirm_password')

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password_hash)s, NOW(), NOW());"
        dataPass = { "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'], 
            "email" : request.form['email'],
            "password_hash" : pw_hash,
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'] }
    
        mysql.query_db(query, dataPass)
        session["first_name"] = request.form['first_name']
        session["last_name"] = request.form['last_name']
        session["email"] = request.form['email']
        session["password"] = request.form['password']
        session["confirm_password"] = request.form['confirm_password']
        return redirect('/success')

@app.route('/success')
def success():
    print('You Have Successfully Registered!')
    return render_template('success.html')

@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['email'] = result[0]['id']
            return redirect('/success')

    flash("You could not be logged in")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)