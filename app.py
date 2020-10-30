# app.py
import os
from flask import Flask, request, render_template, redirect, url_for

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

@app.route('/')
def index():
    return render_template('login.html') #' test world!'
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = request.form['username']
    password = request.form['password']
    location = request.form['location']
    
    return render_template('login.html', error=error)
