# app.py
import os
from flask import Flask, request, render_template, redirect, url_for
import dbio.SQL.feed as queries

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/')
def index():
    return ' test world!'


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
