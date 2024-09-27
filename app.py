from flask import Flask,render_template,redirect,request, session,url_for,flash
import sqlite3
from flask_session import Session
from datetime import datetime

app=Flask(__name__)

app.secret_key='your_key'
app.config['SESSION_TYPE']='filesystem'
Session(app)

ADMIN_CREDENTIALS ={
    'Admin':'admin123',
    'Elango':'Elango@220'
}

def init_db():
    conn=sqlite3.connect('database.db')
    cursor =conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT NOT NULL,
                   phone INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    name=request.form['name'];
    email=request.form['email'];
    phone=request.form['phone'];
    
    conn=sqlite3.connect('database.db')
    cursor =conn.cursor()
    cursor.execute('INSERT INTO users(name,email,phone) VALUES(?,?,?)',(name,email,phone))
    conn.commit()
    conn.close()

    flash(f"Thank you {name} to provide your details. A Detail information send to the {email} please check it.")
    return redirect(url_for('index'))
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method =='POST':
        username =request.form['username']
        password =request.form['password']

        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username]==password:
            session['logged_in'] =True
            flash('Successfully logged in!')
            return redirect(url_for('result'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You have been Logged out.')
    return redirect(url_for('login'))

@app.route('/result')
def result():
    if not session.get('logged_in'):
        flash('you need to log in to access this page')
        return redirect(url_for('login'))
    
    conn=sqlite3.connect('database.db')
    cursor =conn.cursor()
    cursor.execute('SELECT * FROM users')
    data=cursor.fetchall()
    conn.close()

    return render_template('result.html',data=data)


if __name__=='__main__':
    init_db()
    app.run(debug=True)