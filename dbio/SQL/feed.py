from __future__ import print_function

import calendar
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
    cursor = db.cursor(prepared=True)

    # 1. query based on user, grab posts that are visible to them
    # Query the feed based on the location of the user which can be passed in
    
    ## This function is not fully implemented yet - it will display all the messages in the DB for now 
    ## This is the old code
    '''
    sql = """
        SELECT post_id, post_message, location, tags, likes, dislikes, u.username
        FROM Posts p NATURAL JOIN Users u
        WHERE u.username = %s
        ORDER BY post_id
    """
    '''
    # number of rows = cursor.execute(sql, (user,))
    
    ## This code is being used for the demo
    sql = """
        SELECT post_id, post_message, location, tags, likes, dislikes, author
        FROM Posts p
        ORDER BY post_id
    """

    number_of_rows = cursor.execute(sql)
    records = cursor.fetchall()


    cursor.close()
    db.close()

    # 2. take results, pass them to frontend for display
    return records

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
    cursor = db.cursor(prepared=True)

    post_id = int(calendar.timegm(time.gmtime()))
    
    sql = """
        INSERT INTO Posts (post_id, author, location, post_message, tags, reply_ids, likes, dislikes) 
        VALUES (%s, %s, %s, %s, %s, "", 0, 0)
    """
    query_tuple = (post_id, user, location, post_message, tags)

    number_of_rows = cursor.execute(sql, query_tuple)

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
    # print(db)
    cursor = db.cursor(prepared=True)
    # print(cursor)
    
    # leaving out reply_ids because it's a new post. Post 
    sql = """
        DELETE FROM Posts WHERE post_id = %s
    """
    cursor.execute(sql, (post_id,))

    # Also need to incorporate posted_by relation
    sql = """
        DELETE FROM Posted_By WHERE post_id = %s
    """
    cursor.execute(sql, (post_id,))

    db.commit()
    cursor.close()
    db.close()

def likepost(user, post_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)

    # check status of whether user has liked this post or not.
    sql = """
        SELECT liked
        FROM Post_Interaction
        WHERE post_id = %s AND username = %s
    """

    cursor.execute(sql, (post_id, user))
    records = cursor.fetchall()
    
    if len(records) > 0: # Post has been interacted with before
        if records[0]: # Post was already liked by the user, so unlike it
            # Decrement the likes in Posts
            sql = """
               UPDATE Posts p
               SET likes = likes - 1
               WHERE p.post_id = %s
            """
            cursor.execute(sql, (post_id,))

            # Unlike the post in Post_Interaction
            sql = """
               UPDATE Post_Interaction
               SET liked = 0
	           WHERE post_id = %s AND username = %s
            """
            cursor.execute(sql, (post_id, user))
            
            db.commit() # added 
            
        else: # Post has not been liked by the user
            # Increment the likes in Posts
            sql = """
               UPDATE Posts p
               SET likes = likes + 1
               WHERE p.post_id = %s
            """
            cursor.execute(sql, (post_id,))

            sql = """
               UPDATE Post_Interaction
               SET liked = 1
               WHERE post_id = %s AND username = %s
            """
            cursor.execute(sql, (post_id, user))
            
            db.commit() # added 
            
    else: # Post has not been interacted with until now
        # Increment the likes in Posts
        sql = """
           UPDATE Posts p
           SET likes = likes + 1
           WHERE p.post_id = %s
        """
        cursor.execute(sql, (post_id,))
	
        # User likes the post for the first time
        sql = """
            INSERT INTO Post_Interaction (post_id, username, liked, disliked)
            VALUES (%s, %s, 1, 0)
        """
        cursor.execute(sql, (post_id, user))
        
        db.commit() # added
        
    db.commit()
    cursor.close()
    db.close()
    
def dislikepost(user, post_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)

    # check status of whether user has liked this post or not.
    sql = """
        SELECT disliked
        FROM Post_Interaction
        WHERE post_id = %s AND username = %s
    """

    cursor.execute(sql, (post_id, user))
    records = cursor.fetchall()
    
    if len(records) > 0: # Post has been interacted with before
        if records[0]: # Post was already disliked by the user, so remove dislike
            # Decrement the dislikes in Posts
            sql = """
               UPDATE Posts p
               SET dislikes = dislikes - 1
               WHERE p.post_id = %s
            """
            cursor.execute(sql, (post_id,))

            # Remove dislike of the post in Post_Interaction
            sql = """
               UPDATE Post_Interaction
               SET disliked = 0
	           WHERE post_id = %s AND username = %s
            """
            cursor.execute(sql, (post_id, user))
            
            db.commit() # added 
            
        else: # Post has not been disliked by the user
            # Increment the disliked in Posts
            print("Post has been interacted with before, but not liked currently - liking post")
            sql = """
               UPDATE Posts p
               SET dislikes = dislikes + 1
               WHERE p.post_id = %s
            """
            cursor.execute(sql, (post_id,))

            sql = """
               UPDATE Post_Interaction
               SET disliked = 1
               WHERE post_id = %s AND username = %s
            """
            cursor.execute(sql, (post_id, user))
            
            db.commit() # added 
            
    else: # Post has not been interacted with until now
        # Increment the dislikes in Posts
        sql = """
           UPDATE Posts p
           SET dislikes = dislikes + 1
           WHERE p.post_id = %s
        """
        cursor.execute(sql, (post_id,))
	
        # User dislikes the post for the first time
        sql = """
            INSERT INTO Post_Interaction (post_id, username, liked, disliked)
            VALUES (%s, %s, 0, 1)
        """
        cursor.execute(sql, (post_id, user))
        
        db.commit() # added
        
    db.commit()
    cursor.close()
    db.close()

##  TEST AREA
# run only one createpost at a time for now.
# createpost("nicklesimba", "Champaign", "ayo", "")
# createpost("someUser123", "Champaign", "what's goooood?", "test")
# frontend_code = feed_query("nicklesimba") # more frontend code would follow to format and display it
# print(frontend_code)
