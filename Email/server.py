from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app, 'emails')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emails', methods = ['POST'])
def create():
    query = mysql.query_db("SELECT email FROM emails")    
    nope = []
    for email in query:
        if email['email'] == request.form['email']:
            
            flash("Invalid Email Adress please check that you spelt it correctly and do not have a account already set up")
            return redirect('/')
    if not EMAIL_REGEX.match(request.form['email']):
        nope.append(flash("Invalid Email Adress please check that you spelt it correctly and do not have a account already set up"))
        return redirect('/')
    else:
        query ="INSERT INTO emails(email) VALUES (:email)"
        data = {
            'email': request.form['email']
        }
        
        mysql.query_db(query,data)
        emails_list=mysql.query_db("SELECT email FROM emails")
        return render_template('succuess.html', all_emails = emails_list)


app.run(debug=True)