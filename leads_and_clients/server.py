from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
mysql = connectToMySQL('mydb')

@app.route('/')
def index():
    all_leads = mysql.query_db("SELECT * FROM leads")
    print("Fetched all leads", all_leads)
    return render_template('index.html', leads = all_leads)

if __name__ == "__main__":
    app.run(debug=True)