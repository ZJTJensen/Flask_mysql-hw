from flask import Flask, render_template, redirect, request, session,flash
from mysqlconnection import MySQLConnector
import re, datetime
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key ="NEVER GOING TO GIVE YOU UP"
mysql = MySQLConnector(app, 'userdb')

@app.route('/', methods=["GET"])
def index():

    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    query = mysql.query_db("SELECT email, id, password FROM users")
    for users in query:
        if users['email'] == request.form['email'] and users['password'] == md5.new(request.form['password']).hexdigest():
            flash("YOU LOGGED IN")
            session.id = users['id']
            return render_template("success.html")
    flash("Wrong email or password")
    return redirect('/')
    


@app.route('/process', methods=['POST'])
def process():
    query = mysql.query_db("SELECT * FROM users")
    counter = 0
    time = datetime.datetime.now()
    time.strftime('%m/%d/%Y')
    messages=[]
    for email in query:
        if email['email'] == request.form['email']:
            flash("Emailadress already in use please try again")
            return redirect('/')
    if len(request.form['email'])<1 or len(request.form['first_name'])<1 or len(request.form['last_name'])<1 or len(request.form['password'])<1 or len(request.form['confirm_password'])<1:
        messages.append("inputs must be greater than 0")
        counter +=1 
    if not EMAIL_REGEX.match(request.form['email']):
        messages.append("Invalid Email adress")
        counter +=1 
    if not NAME_REGEX.match(request.form['last_name']):
        messages.append("Invalid name fiels")
        counter +=1 
    if not NAME_REGEX.match(request.form['first_name']):
        messages.append("Invalid name fiels")
        counter +=1 
    if len(request.form['password'])<8:
        messages.append("password must be longer than 8 charecters")
        counter +=1 
    if request.form['password'] != request.form['confirm_password']:
        messages.append("passowrd and confirm password must be the same ")
        counter +=1 
    if counter > 1:
        for message in range (0, len(messages)):
            flash(messages[message])
        return redirect('/')

    
    else:
        query ="INSERT INTO users(first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
        data = {
            'email':request.form['email'],
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'password':md5.new(request.form['password']).hexdigest()
        }
        mysql.query_db(query,data)
        flash ("All info is fine")
    return render_template('success.html')

app.run(debug=True)