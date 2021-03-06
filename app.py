# app.py
import os
from flask import Flask, request, render_template, redirect, url_for
import dbio.SQL.users as users
import dbio.SQL.feed as queries
from dbio.NoSQL import analytics_db
import gensim 
from gensim.models import Word2Vec 
import gensim.downloader as api
import json

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

model = gensim.models.KeyedVectors.load('local.model')
mongo = analytics_db.AnalyticsDB()
sort_type = "comment_id"

def _byte_decode(text):
	return text.decode(encoding='UTF-8')


@app.route('/')
def index():
    return redirect(url_for('login'))
    
# login page
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
            #update user's location with their new login location
            queries.update_user_location(username, location)
            ## redirect to feed page with location information
            return redirect(url_for('feed', username=username, location=location, search_tag="None"))
            
        else:
            error = "Invalid Username or Password"
            return render_template('login.html', error=error)
        
    elif 'Register' in request.form:
        try:
            users.create_user(username, password, location)
            return redirect(url_for('feed', username=username, location=location, search_tag="None"))
            
        except (TypeError, RuntimeError) as e:
            error = e.args[0]
            return render_template('login.html', error=error)
            
    else:
        error = "Something went wrong"
        return render_template('login.html', error=error)

# user feed
@app.route('/feed/<username>/<location>/searchtag<search_tag>', methods=['GET', 'POST'])
def feed(username, location, search_tag):
    print("SEARCH TAG: ", search_tag)
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
        if search_tag == "None":
            post_info[i[0]] = curr
        else:
            for j in curr['tags'].split(','):
                if search_tag.lower() == j.lower().strip():
                    post_info[i[0]] = curr
    posts = post_info.keys()

    if request.method == 'GET':
        return render_template(
            'feed.html',
            posts=posts,
            post_info=post_info,
            curr_user=username,
            search_tag=search_tag
        )
    
    if request.form["Submit Type"] == 'Make Post':
        print("Current user created a post")
        message = request.form.get('message')
        post_location = location
        tags = request.form.get('tags')
        queries.createpost(username, post_location, message, tags)
        
    elif request.form['Submit Type'] == 'Like':
        print("Current user liked a post")
        queries.likepost(username, request.form['postId'])
        
    elif request.form['Submit Type'] == 'Dislike':
        print("Current user dislked a post")
        queries.dislikepost(username, request.form['postId'])
    
    elif request.form['Submit Type'] == 'Delete':
        print("Current user deleted a post")
        queries.deletepost(request.form['postId'])
    
    elif request.form['Submit Type'] == '(my info)':
        print('Redirecting to user page', username, location)
        return redirect(url_for('user_page', username=username, location=location, search_tag="None"))
        
    elif request.form['Submit Type'] == 'Search Tag':
        return redirect(url_for('feed', username=username, location=location, search_tag=request.form['search_tag']))

    elif request.form['Submit Type'] == 'Clear Tag':
        return redirect(url_for('feed', username=username, location=location, search_tag="None"))

    elif request.form['Submit Type'] == 'View Replies':
        print("Current user is viewing a post's replies")
        print(request.form['postId'])
        return redirect(url_for('comments_feed', username=username, location=location, postid=request.form['postId']))
        
    return redirect(url_for('feed', username=username, location=location, search_tag="None"))

# view replies
@app.route('/comments/<username>/<location>/<postid>', methods=['GET', 'POST'])
def comments_feed(username, location, postid):
    ## load the replies based on postid
    global sort_type
    comment_info = {}
    query_result = queries.comments_feed_query(postid, sort_type)

    for i in query_result:
        curr = {
            'name': _byte_decode(i[1]),
            'id': i[0],
            'message': _byte_decode(i[2]),
            'likes': i[3],
            'dislikes': i[4]
        }
        comment_info[i[0]] = curr
    comments = comment_info.keys()
    
    ## gets the information of the post whose replies you wanted to see
    original = queries.post_info_query(postid)
    original_post_author = _byte_decode(original[0])
    original_post_message = _byte_decode(original[1])
    
    if request.method == 'GET':
        print("yeehaw")
        return render_template(
            'comment_feed.html',
            author=original_post_author,
            message=original_post_message,
            comments=comments,
            comment_info=comment_info,
            curr_user=username
        )
    
    if request.form['Submit Type'] == 'Make Reply':
        print("Current user is replying to a post")
        message = request.form.get('message')
        score = model.wmdistance(original_post_message, message)
        print("Comment relevancy: ", score)
        queries.createcomment(postid, username, message, score)
    
    elif request.form['Submit Type'] == 'Like':
        print("Current user liked a reply to a post")
        queries.likecomment(username, request.form['commentId'])
    
    elif request.form['Submit Type'] == "Dislike":
        print("Current user disliked a reply to a post")
        queries.dislikecomment(username, request.form['commentId'])
    
    elif request.form['Submit Type'] == "Delete":
        print("Current user deleted their reply to a post")
        queries.deletecomment(request.form['commentId'])
    
    elif request.form['Submit Type'] == "Recency":
        print("Current user sorting post replies by recency")
        sort_type = "comment_id"

    elif request.form['Submit Type'] == "Likes":
        print("Current user sorting post replies by likes")
        sort_type = "likes"

    elif request.form['Submit Type'] == "Relevancy":
        print("Current user sorting post replies by relevancy")
        sort_type = "relevancy"

    elif request.form['Submit Type'] == '(back)':
        sort_type = "comment_id"
        return redirect(url_for('feed', username=username, location=location, search_tag="None"))

    
    print(query_result)
    return redirect(url_for('comments_feed', username=username, location=location, postid=postid))
        
    

@app.route('/user/<username>/<location>', methods=['GET', 'POST'])
def user_page(username, location):
    location_dict = mongo.aggregate_location_data(username)
    tag_dict = mongo.aggregate_tag_usage(username)
    recent_dict = mongo.aggregate_recent_posts(username)
    time_dict = mongo.aggregate_post_timeOfDay(username)
    location_dict = [i for i in location_dict if len(i['location']) > 1]
    total = 0
    for i in range(len(location_dict)):
        location_dict[i]['count'] = int(location_dict[i]['count'])
        total += location_dict[i]['count']
    location_labels = [i['location'] for i in location_dict]
    tod_counts = {"Early Morning":0, "Morning":0, "Afternoon":0, "Evening":0}
    for i in time_dict:
        if int(i['tod']) < 21600:
            tod_counts["Early Morning"] += 1
        elif int(i['tod']) < 43200:
            tod_counts["Morning"] += 1
        elif int(i['tod']) < 64800:
            tod_counts["Afternoon"] += 1
        else:
            tod_counts["Evening"] += 1
    tag_counts = {}
    tag_labels = [i['tag'] for i in tag_dict]
    print(tag_counts)

    if request.method == 'GET':
        return render_template(
            'user_page.html', 
            username=username, 
            location=location,
            location_dict=location_dict,
            tag_counts=tag_dict,
            recent_dict=recent_dict,
            tod_counts=tod_counts,
            location_labels=location_labels,
            tod_labels=["Early Morning", "Morning", "Afternoon", "Evening"],
            tag_labels=tag_labels
        )
    if request.form['Submit Type'] == '(back)':
        return redirect(url_for('feed', username=username, location=location, search_tag="None"))

if __name__ == '__main__':
    app.run()
