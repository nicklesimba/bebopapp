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


@app.route('/feed')
def feed():
    posts = ['post1','post2','post3','post4','post5']
    post_info = {
        'post1':{'name':'divya', 'text':'yoyoyoyo what up boi', 'likes':2, 'views':4},
        'post2':{'name':'nikhil', 'text':'i hate CS 411!', 'likes':1001201, 'views':10310359},
        'post3':{'name':'nikhil', 'text':'hi', 'likes':21, 'views':45},
        'post4':{'name':'maanu', 'text':'Hello world, my name is Maanu', 'likes':-102, 'views':45102},
        'post5':{'name':'ram', 'text':'lol!', 'likes':0, 'views':10},
    }
    return render_template(
        'feed.html',
        posts=posts,
        post_info=post_info
    )

if __name__ == '__main__':
    app.run()