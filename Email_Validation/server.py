from flask import Flask, render_template, session, request, redirect, flash
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "emailKey"
mysql = connectToMySQL('emaildb')

@app.route('/')
def index():
    #debugHelp("INDEX METHOD")
    all_emails = mysql.query_db("SELECT * FROM emails")
    print("Fetched all emails", all_emails)
    return render_template('index.html', emails = all_emails)

@app.route('/create_email', methods=['POST'])
def create():   
    query ="SELECT email FROM emails WHERE email = %(email)s;"
    data = { 'email' : request.form['email']}
    result = mysql.query_db(query, data)

    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email') 
    elif result:
        flash('Email Already Exists!', 'email')
    
    data = {
             'email': request.form['email'],
           }
    #debugHelp('INDEX METHOD')
    if '_flashes' in session.keys():
        return redirect("/")
    else:
        query = "INSERT INTO emails (email, created_at) VALUES (%(email)s, NOW());"
        mysql.query_db(query, data)
        session["email"] = request.form['email']
        return redirect('/success')

@app.route('/success')
def success():
    all_emails = mysql.query_db("SELECT * FROM emails")
    print("Fetched all emails", all_emails)
    return render_template('success.html', emails = all_emails)

if __name__ == "__main__":
    app.run(debug=True)