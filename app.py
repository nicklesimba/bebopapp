# app.py
import os
from flask import Flask, request, render_template, redirect, url_for
import dbio.SQL.users as users
import dbio.SQL.feed as queries

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/')
def index():
    return ' test world!'
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    error = None
    username = request.form.get('username')
    password = request.form.get('password')
    location = request.form.get('location')
    
    if 'Login' in request.form:
        valid = users.check_login(username, password)
        if valid:
            ## redirect to feed page with location information
            error = "Login worked: need to redirect"
            return render_template('login.html', error=error)
            
        else:
            error = "Invalid Username or Password"
            return render_template('login.html', error=error)
        
    elif 'Register' in request.form:
        try:
            users.create_user(username, password, location)
            error = "Registration worked: need to redirect"
            return render_template('login.html', error=error)
        except (TypeError, RuntimeError) as e:
            error = e.args[0]
            return render_template('login.html', error=error)
            
    else:
        error = "Something went wrong"
        return render_template('login.html', error=error)


@app.route('/feed')
def feed():
    post_info = {}
    user = 'nicklesimba'
    query_result = queries.feed_query(user)
    for i in query_result:
        curr = {
            'name':i[6],
            'id':i[0],
            'message':i[1],
            'location':i[2],
            'tags':i[3],
            'likes':i[4],
            'dislikes':i[5]
        }
        post_info[i[0]] = curr
    posts = post_info.keys()
    return render_template(
        'feed.html',
        posts=posts,
        post_info=post_info
    )

if __name__ == '__main__':
    app.run()
