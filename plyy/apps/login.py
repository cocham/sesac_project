from functools import wraps
from flask import Flask, session, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'plyy_page'

def connect_db():
    conn = sqlite3.connect('plyy.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur


# def login_required(view):
#     @wraps(view)
#     def wrapped_view(*args, **kwargs):
#         if 'logged_in' in session and session['logged_in']:
#             return view(*args, **kwargs)
#         else:
#             return redirect(url_for('login'))
#     return wrapped_view

@app.route('/main',methods=['get','post'])
def main():
    return render_template('main.html')

@app.route('/myPage')
def mypage():
    return render_template('mypage.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn,cur = connect_db()
        id = request.form['userid']
        pw = request.form['userpw']

        cur.execute('''
                        SELECT u_email, u_pw
                        FROM USER
                        WHERE u_email = ? and u_pw = ?
                    ''',(id,pw))

        user = cur.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return redirect(url_for('main'))
        
        else:
            session['logged_in'] = False
    
    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)