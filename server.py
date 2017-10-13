from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import time
import re

app = Flask(__name__)
app.secret_key = "waow"
mysql = MySQLConnector(app,'emaildb')

@app.route('/')
def index():
    # query = "SELECT * FROM friends"
    # year = mysql.query_db("SELECT YEAR('created_at') FROM friends")
    # friends = mysql.query_db(query)
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def create():
    email = request.form['email']
    data ={'email': email}
    query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
    check = "SELECT * FROM emails"
    print mysql.query_db(check)

    my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    for i in (mysql.query_db(check)):
        if i['email'] == email:
            flash("email already in database")
            return redirect('/')
    if not my_re.match(email):
        flash("bad email")
    else:
        print "good email"
        mysql.query_db(query, data)
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def success():
    query = "SELECT email, created_at FROM emails"
    emails = mysql.query_db(query)

    return render_template("success.html", emails = emails)





@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])

    

app.run(debug=True)
