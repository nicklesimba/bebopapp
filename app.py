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
            return redirect(url_for('feed', username=username, location=location))
            
        else:
            error = "Invalid Username or Password"
            return render_template('login.html', error=error)
        
    elif 'Register' in request.form:
        try:
            users.create_user(username, password, location)
            return redirect(url_for('feed', username=username, location=location))
            
        except (TypeError, RuntimeError) as e:
            error = e.args[0]
            return render_template('login.html', error=error)
            
    else:
        error = "Something went wrong"
        return render_template('login.html', error=error)

# user feed
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

    if request.method == 'GET':
        return render_template(
            'feed.html',
            posts=posts,
            post_info=post_info,
            curr_user=username
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
    
    elif request.form['Submit Type'] == 'My Info':
        print('Redirecting to user page', username, location)
        return redirect(url_for('user_page', username=username, location=location))
        
    elif request.form['Submit Type'] == 'View Replies':
        print("Current user is viewing a post's replies")
        print(request.form['postId'])
        return redirect(url_for('comments_feed', username=username, location=location, postid=request.form['postId']))
        
    return redirect(url_for('feed', username=username, location=location))
    
# view replies
@app.route('/feed/<username>/<location>/<postid>', methods=['GET', 'POST'])
def comments_feed(username, location, postid):
    ## load the replies based on postid
    sort_flag = 0
    comment_info = {}
    query_result = queries.comments_feed_query(postid, "comment_id") 
    # ^^^ ^^^ ^^^ README: COMMENTS_FEED_QUERY FUNCTION ^^^ ^^^ ^^^
    # second hardcoded argument needs to be replaced with result of dropdown menu. here's what should go for each dropdown option, all are sorted DESC.
    # "sort by likes"     ==> "likes"
    # "sort by relevancy" ==> "relevancy"
    # "sort by recency" ==> "comment_id"

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
        queries.createcomment(postid, username, message)
    
    elif request.form['Submit Type'] == 'Like':
        print("Current user liked a reply to a post")
        queries.likecomment(username, request.form['commentId'])
    
    elif request.form['Submit Type'] == "Dislike":
        print("Current user disliked a reply to a post")
        queries.dislikecomment(username, request.form['commentId'])
    
    elif request.form['Submit Type'] == "Delete":
        print("Current user deleted their reply to a post")
        queries.deletecomment(request.form['commentId'])

    elif request.form['Submit Type'] == "SortRecency":
        print("Current user sorting post replies by recency")
        query_result = queries.comments_feed_query(postid, "comment_id")
        sort_flag = 1
        

    elif request.form['Submit Type'] == "SortLikes":
        print("Current user sorting post replies by likes")
        query_result = queries.comments_feed_query(postid, "likes")
        sort_helper(query_result, postid, username)
        sort_flag = 1
        
    # One more here for SortRelevancy
    
    if sort_flag:
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
            return render_template(
                'comment_feed.html',
                author=original_post_author,
                message=original_post_message,
                comments=comments,
                comment_info=comment_info,
                curr_user=username
            )

    elif request.form['Submit Type'] == 'Back':
        return redirect(url_for('feed', username=username, location=location))
    
    return redirect(url_for('comments_feed', username=username, location=location, postid=postid))
        
    

@app.route('/user/<username>/<location>', methods=['GET', 'POST'])
def user_page(username, location):
    if request.method == 'GET':
        return render_template('user_page.html', username=username, location=location)
    if request.form['Submit Type'] == 'Back':
        return redirect(url_for('feed', username=username, location=location))

if __name__ == '__main__':
    app.run()
