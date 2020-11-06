# app.py
import os
from flask import Flask, request, render_template, redirect, url_for
import dbio.SQL.users as users
import dbio.SQL.feed as queries

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


def _byte_decode(text):
	return text.decode(encoding='UTF-8')


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
            return redirect(url_for('feed', username=username, location=location))
            
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


@app.route('/feed/<username>/<location>', methods=['GET', 'POST'])
def feed(username, location):
    post_info = {}
    query_result = queries.feed_query(username)
    for i in query_result:
        curr = {
            'name':_byte_decode(i[6]),
            'id':i[0],
            'message':_byte_decode(i[1]),
            'location':_byte_decode(i[2]),
            'tags':_byte_decode(i[3]),
            'likes':i[4],
            'dislikes':i[5]
        }
        post_info[i[0]] = curr
    posts = post_info.keys()

    #When loading the page initially
    if request.method == 'GET':
        return render_template(
            'feed.html',
            posts=posts,
            post_info=post_info
        )
    
    #If it's a POST request, check which type of submit we did
    if request.form["Submit Type"] == 'Make Post':
        message = request.form.get('message')
        post_location = location
        # location = request.form.get('location')
        tags = request.form.get('tags')
        queries.createpost(username, post_location, message, tags)
        
    elif request.form['Submit Type'] == 'Like':
        queries.likepost(username, request.form['postId'])
        
    elif request.form['Submit Type'] == 'Dislike':
        queries.likepost(username, request.form['postId'])
        
    return redirect(url_for('feed', username=username))
    

if __name__ == '__main__':
    app.run()
