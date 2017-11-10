from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re, datetime
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key ="NEVER GOING TO GIVE YOU UP"
mysql = MySQLConnector(app, 'usersdb')


@app.route('/', methods=["GET"])
def index():

    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    query = mysql.query_db("SELECT * FROM users")
    for users in query:
        if users['email'] == request.form['email'] and users['password'] == md5.new(request.form['password']).hexdigest():
            flash("YOU LOGGED IN")
            session['id'] = users['id'] 
            return redirect("/wall")
    flash("Wrong email or password")
    return redirect('/')

@app.route('/wall' )
def wall():
    query = mysql.query_db("SELECT messages.message AS message, messages.id as messages_id, messages.created_at AS message_time, users.first_name as user FROM messages JOIN users ON messages.users_id = users.id")
    print query
    query2 = mysql.query_db("SELECT comments.comment AS comment, comments.created_at AS comment_time, users.first_name as user, messages.id AS messages_id FROM comments JOIN messages on comments.messages_id = messages.id JOIN  users ON comments.users_id = users.id")
    print query2
    return render_template('wall.html', query=query, query2=query2)

@app.route('/messages', methods=["POST"])
def messages():
    query=("INSERT INTO messages (message, users_id, created_at, updatedat) VALUES (:message, :users_id, NOW(),NOW())")
    data={
        'message' :request.form['message'],
        'users_id' :session['id']
    }
    mysql.query_db(query, data)
    return redirect('/wall')
@app.route('/comment', methods=["POST"])
def comment():
    query=("INSERT INTO comments (comment, users_id, messages_id, created_at, updated_at) VALUES (:comment, :messages_id, :users_id, NOW(),NOW())")
    data={
        'comment' :request.form['comment'],
        'users_id' :session['id'],
        'messages_id' :request.form['messages_id']
    }
    mysql.query_db(query, data)
    return redirect('/wall')
    


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
        query2 = ("SELECT users.id FROM users WHERE email = '{}'").format(request.form['email'])
        data2 = {
            'email': request.form["email"]
        }
        id_result = mysql.query_db(query2)
        session['id'] = int(id_result[0]['id'])
        flash ("All info is fine")
    return redirect('/wall')

app.run(debug=True)