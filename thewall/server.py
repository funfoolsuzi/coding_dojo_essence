from flask import Flask, render_template, render_template_string, request, redirect, flash, session
import md5
import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
# Create a class that will give us an object that we can use to connect to a database


class MySQLConnection(object):
    def __init__(self, app, db):
        config = {
            'host': 'localhost',
            'database': db,  # we got db as an argument
            'user': 'codingdojo',
            'password': '12345678',
            'port': '3306'  # change the port to match the port your SQL server is running on
        }
        # this will use the above values to generate the path to connect to your sql database
        DATABASE_URI = "mysql://{}:{}@127.0.0.1:{}/{}".format(
            config['user'], config['password'], config['port'], config['database'])
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        # establish the connection to database
        self.db = SQLAlchemy(app)
    # this is the method we will use to query the database

    def query_db(self, query, data=None):
        result = self.db.session.execute(text(query), data)
        if query[0:6].lower() == 'select':
            # if the query was a select
            # convert the result to a list of dictionaries
            list_result = [dict(r) for r in result]
            # return the results as a list of dictionaries
            return list_result
        elif query[0:6].lower() == 'insert':
            # if the query was an insert, return the id of the
            # commit changes
            self.db.session.commit()
            # row that was inserted
            return result.lastrowid
        else:
            # if the query was an update or delete, return nothing and commit changes
            self.db.session.commit()
# This is the module method to be called by the user in server.py. Make sure to provide the db name!


def MySQLConnector(app, db):
    return MySQLConnection(app, db)


app = Flask(__name__)
app.secret_key = "seckey"

conn = MySQLConnector(app, 'the_wall')


@app.route("/")
def index():
    messages = conn.query_db('''SELECT messages.message, messages.created_at, CONCAT(users.first_name," ",users.last_name) as name, messages.id
    FROM messages
    JOIN users ON users.id=messages.users_id
    ORDER BY messages.created_at DESC
    ''')
    for message in messages:
        message['comments'] = conn.query_db('''SELECT comments.comment, comments.created_at, CONCAT(users.first_name," ",users.last_name) as name
        FROM comments
        JOIN users ON users.id=comments.users_id
        WHERE comments.messages_id=:m_id
        ORDER BY comments.created_at DESC
        ''',{'m_id':message["id"]})
    return render_template("/index.html", messages=messages)


@app.route("/wall")
def wall():
    try:
        session["user"]
    except:
        flash("not logged in")
        return redirect("/")
    return render_template_string('''
    You are logged in!
    <form action="/logout" method="post">
        <input hidden name="action" value="logout" />
        <input type="submit" value="Log Out!" />
    </form>
    ''')

@app.route("/users", methods=["post"])
def register():
    bad = False
    if len(request.form['first_name']) < 2:
        flash("First Name needs to be 2 charater long")
        bad = True
    if len(request.form['last_name']) < 2:
        flash("Last Name needs to be 2 character long")
        bad = True
    if not re.compile(r'.+@.+\..+').search(request.form['email']):
        flash("Bad email format")
        bad = True
    if not request.form['password'] == request.form['c_password']:
        flash("passwords dont match")
        bad = True
    if len(request.form['password']) < 8:
        flash("password needs to be at least 8 character long")
        bad = True
    if(bad):
        return redirect("/")
    id = conn.query_db('''INSERT INTO users(first_name,last_name,email,password)
    VALUES(:fname, :lname, :email, :password)
    ''', {
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'email': request.form['email'],
        'password': md5.new(request.form['password']).hexdigest()
    })
    res = conn.query_db('''SELECT id, email, first_name, last_name 
    FROM users
    WHERE id=:id
    ''', {
        'id': id
    })
    session['user'] = res[0]
    return redirect("/")


@app.route("/login", methods=["post"])
def login():
    hashed = unicode(md5.new(request.form['password']).hexdigest())
    res = conn.query_db('''SELECT id, email, first_name, last_name 
    FROM users
    WHERE email=:email AND password=:password
    ''', {
        'email': request.form['email'],
        'password': hashed
    })
    if not res:
        flash("bad login")
        return redirect("/login")
    session["user"] = res[0]
    return redirect("/")

@app.route("/logout", methods=["post"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/message", methods=["post"])
def create_message():
    try:
        conn.query_db('''INSERT INTO messages(message, users_id)
        VALUES (:msg, :id)
        ''', {
            'msg':request.form["message"],
            'id':session["user"]['id']
        })
    except:
        flash("something went wrong, couldn't insert data")
    return redirect("/")

@app.route("/comments/<msg_id>", methods=["post"])
def create_comment(msg_id):
    try:
        conn.query_db('''INSERT INTO comments(comment, messages_id, users_id)
        VALUES (:cm, :m_id, :u_id)
        ''', {
            'cm':request.form["comment"],
            'm_id':msg_id,
            'u_id':session["user"]["id"]
        })
    except:
        flash("something went wrong, couldn't insert data")
    return redirect("/")


app.run(debug=True)
