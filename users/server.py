from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key ="memes"
mysql = MySQLConnector(app,'friends')


@app.route('/')
def index():
    query = "SELECT Name, Age, CONCAT(MONTHNAME(newfriends.Datecreated), ' ', DAYNAME(newfriends.Datecreated), ' ', YEAR(newfriends.Datecreated)) AS date FROM newfriends"                           # define your query
    newfriends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=newfriends) 

@app.route('/newfriends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO newfriends (Name, Age, Datecreated) VALUES (:Name, :Age, NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'Name': request.form['Name'],
             'Age': request.form['Age'],          
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)