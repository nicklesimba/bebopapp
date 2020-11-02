# app.py
import os
from flask import Flask, request, render_template, redirect, url_for

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
    
    ## pass these as params to db query function
    ## if usr and pword are in db, redirect to user feed with the location information
    ## if not, display error message and suggest registration  

    return render_template('login.html', error=error)
