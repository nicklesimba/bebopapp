# app.py
import os
from flask import Flask, request, render_template, redirect, url_for
import dbio.SQL.users.py as users

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
            error = "Need to redirect - change this later"
            return render_template('login.html', error=error)
            
        else:
            error = "Invalid Username or Password"
            return render_template('login.html', error=error)
        
    elif 'Register' in request.form:
        try:
            users.create_user(username, password, location)
        except (TypeError, RuntimeError) as e:
            error = e.args[0]
            return render_template('login.html', error=error)
            
    else:
        error = "Something went wrong"
        return render_template('login.html', error=error)
