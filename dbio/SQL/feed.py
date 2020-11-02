from __future__ import print_function

import mysql.connector as my
import time

# func - feed_query
# desc - takes in a username and returns most recent posts within the user's area.
# args - user - username for feed query
# ret  - returns records for frontend code to use
def feed_query(user):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    print(db)
    cursor = db.cursor(prepared=True)
    print(cursor)

    # 1. query based on user, grab posts that are visible to them

    # I think we'd also wanna return post_id in case someone clicks on the post so we can also query replies afterward based off the post_id
    sql = """
        SELECT post_id, post_message, location, tags, likes, dislikes, u.username
        FROM Posts p NATURAL JOIN Users u
        WHERE u.username = %s
    """

    number_of_rows = cursor.execute(sql, user) # might need to be in format of a user string
    records = cursor.fetchall()
    print(records)


    cursor.close()
    db.close()

    # 1.5
    # I think we'd also want to sort by post date. most recent to least recent! so this should replace the above query when the database structure supports it. 
    # sql = """
    #     SELECT p.post_id, p.post_message, p.location, p.tags, p.likes, p.dislikes, p.date
    #     FROM Posts p NATURAL JOIN Users u
    #     WHERE u.username = %s
    #     ORDER BY p.date
    # """

    # 2. take results, pass them to frontend for display
    return records;

# func - createpost
# desc - takes in a username and post info, then adds the respective entry to Post and Posted_By tables
# args - username + all the post info
# ret  - N/A, just updates db table Post and Posted_By
def createpost(user, location, post_message, tags):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    print(db)
    cursor = db.cursor(prepared=True)
    print(cursor)

    post_id = time.time()
    
    # leaving out reply_ids because it's a new post.
    sql = """
        INSERT INTO Posts (post_id, location, post_message, tags, reply_ids, likes, dislikes) 
        VALUES (%s, %s, %s, %s, "", 0, 0)
    """
    query_tuple = (post_id, location, post_message, tags)

    number_of_rows = cursor.execute(sql, query_tuple)
    print(records)

    # Also need to incorporate posted_by relation
    sql = """
        INSERT INTO Posted_By (post_id, username) 
        VALUES (%s, %s)
    """
    query_tuple = (post_id, username)

    number_of_rows = cursor.execute(sql, query_tuple)
    print(records)

    db.commit()
    cursor.close()
    db.close()

# func - deletepost
# desc - takes in a username and post_id, then deletes Post and Posted_By entry
# args - user - the current user
#        post_id - the timestamp of the post that should be deleted
# ret  - N/A, just updates db table Post and Posted_By
def deletepost(user, post_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    print(db)
    cursor = db.cursor(prepared=True)
    print(cursor)
    
    # leaving out reply_ids because it's a new post. Post 
    sql = """
        DELETE FROM Posts WHERE post_id = %s
    """

    number_of_rows = cursor.execute(sql, post_id)
    print(records)

    # Also need to incorporate posted_by relation
    sql = """
        DELETE FROM Posted_By WHERE post_id = %s
    """

    number_of_rows = cursor.execute(sql, post_id)
    print(records)

    db.commit()
    cursor.close()
    db.close()

# func - deletepost
# desc - takes in a username and post_id, then deletes Post and Posted_By entry
# args - user - the current user
#        post_id - the timestamp of the post that should be deleted
# ret  - N/A, just updates db table Post and Posted_By
def likepost(user, post_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    print(db)
    cursor = db.cursor(prepared=True)
    print(cursor)
    
    # leaving out reply_ids because it's a new post. Post 
    sql = """
        UPDATE Post
        SET likes = likes + 1
    """

    number_of_rows = cursor.execute(sql, post_id)
    print(records)

    # user has marked post as liked, can't like it again
    sql = """
        UPDATE Posted_By
        SET liked_post = 1
    """

    number_of_rows = cursor.execute(sql, post_id)
    print(records)

    db.commit()
    cursor.close()
    db.close()

# test area
createpost("nicklesimba", "Champaign", "ayo", "")
createpost("someUser123", "Champaign", "what's goooood?", "test")
frontend_code = feed_query("nicklesimba") # more frontend code would follow to format and display it
print(frontend_code)

# to do section
'''
frontend actions that would require backend queries:
view feed [x]
create post [x]
delete post [x]
like/dislike post [ ]
'''

# [post1, post2, post3, ...]
