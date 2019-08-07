from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
import json
import sqlite3

conn = sqlite3.connect('goat.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
(id integer primary key autoincrement, username text, password text)''')

c.execute('''CREATE TABLE IF NOT EXISTS shoes
             (id integer primary key autoincrement, brand text, price int, url text, user_id integer, foreign key (user_id) references user(id))''')

conn.commit()

app = Flask(__name__, static_url_path='')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/add_shoe')
def add_shoe():
    if request.cookies.get('user_id') == '':
        return redirect('/login_page', 302)
    return render_template('add_shoe.html')

@app.route('/profile')
def profile():
    # check if user is not logged in, if they are not, send them to login page
    if request.cookies.get('user_id') == '':
        return redirect('/login_page', 302)
    else:
        return render_template('profile.html')

@app.route('/logout')
def logout():
    resp = make_response('logged_out')
    resp.set_cookie('user_id',  '')
    return resp

@app.route('/all_user_shoes')
def all_user_shoes():
    user_id = int(request.cookies.get('user_id'))
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    c.execute("select * from shoes where user_id = ?", (user_id,))
    all_shoes = c.fetchall()
    return json.dumps(all_shoes)

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/register_page')
def register_page():
    return render_template('register_page.html')

@app.route('/delete_shoe', methods = ['POST'])
def delete_shoe():
    print(request.form)
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    shoe_id=request.form["id"]
    c.execute("DELETE FROM SHOES WHERE id = ?", (shoe_id,))
    conn.commit()
    
    return "buy"

@app.route('/all_shoes')
def all_shoes():
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    c.execute("select * from shoes")
    all_shoes = c.fetchall()
    return json.dumps(all_shoes)

@app.route('/register', methods=['POST'])
def register():
    # save new shoe in database
    print(request.form)
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    username=request.form["username"]
    password=request.form["password"]
    c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    resp = make_response(redirect('/profile', 302))
    resp.set_cookie('user_id', str(c.lastrowid))
    return resp

@app.route('/login', methods=['POST'])
def login():
    # save new shoe in database
    print(request.form)
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    username=request.form["username"]
    password=request.form["password"]
    c.execute("SELECT * from users where username = ? and password = ?", (username, password))
    user = c.fetchone()
    print(user)
    if user is not None:
        resp = make_response(redirect('/profile', 302))
        resp.set_cookie('user_id', str(user[0]))
        return resp
    else:
        return "error"

@app.route('/post_new_shoe', methods=['POST'])
def post_new_shoe():
    # save new shoe in database
    print(request.form)
    conn = sqlite3.connect('goat.db')
    c = conn.cursor()
    brand=request.form["shoe_brand"]
    price=request.form["shoe_price"]
    user_id = int(request.cookies.get('user_id'))
    c.execute("INSERT INTO shoes(brand, price, user_id) VALUES (?, ?, ?)", (brand, price, user_id))
    conn.commit()
    return redirect('/profile', 302)

if __name__ == '__main__':
    app.run()

