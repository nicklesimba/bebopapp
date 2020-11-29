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

    sql = """
        SELECT DISTINCT locations
        FROM Users
        WHERE username = %s
    """

    cursor.execute(sql, (user,))
    user_loc = cursor.fetchone()
    string_user_loc = user_loc[0].decode()
    print(string_user_loc)

    ## This code is being used for the demo
    sql = """
        SELECT post_id, post_message, location, tags, likes, dislikes, author
        FROM Posts p
        WHERE p.location = %s
        ORDER BY post_id DESC
    """

    number_of_rows = cursor.execute(sql, (string_user_loc,))
    records = cursor.fetchall()


    cursor.close()
    db.close()

    # 2. take results, pass them to frontend for display
    return records
    
# Gets all the comments for a post
# order_type should be a string equal to "comment_id", "likes", or "relevancy"
def comments_feed_query(postid, order_type):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)
    
    if order_type == "comment_id":
        sql = """
        SELECT comment_id, author, comment_message, likes, dislikes
        FROM Comments c
        WHERE c.post_id = %s
        ORDER BY comment_id DESC
        """
    elif order_type == "likes":
        sql = """
        SELECT comment_id, author, comment_message, likes, dislikes
        FROM Comments c
        WHERE c.post_id = %s
        ORDER BY likes DESC
        """
    elif order_type == "relevancy":
        sql = """
        SELECT comment_id, author, comment_message, likes, dislikes
        FROM Comments c
        WHERE c.post_id = %s
        ORDER BY relevancy DESC
        """
        
    number_of_rows = cursor.execute(sql, (postid,))
    records = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return records
    
# Gets the basic info for a post
def post_info_query(postid):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"
    )
    cursor = db.cursor(prepared=True)
    
    sql = """
        SELECT author, post_message
        FROM Posts p
        WHERE p.post_id = %s
    """
    
    post = cursor.execute(sql, (postid,))
    record = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return record
    
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

def createcomment(postid, user, message):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"
    )
    cursor = db.cursor(prepared=True)
    
    comment_id = int(calendar.timegm(time.gmtime()))
    
    sql = """
        INSERT INTO Comments (post_id, comment_id, author, comment_message, likes, dislikes)
        VALUES (%s, %s, %s, %s, 0, 0)
    """
    query_tuple = (postid, comment_id, user, message)
    
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
    cursor = db.cursor(prepared=True)
    
    sql = """
        DELETE FROM Posts WHERE post_id = %s
    """
    cursor.execute(sql, (post_id,))

    db.commit()
    cursor.close()
    db.close()
    
def deletecomment(comment_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)
    
    sql = """
        DELETE FROM Comments WHERE comment_id = %s
    """
    cursor.execute(sql, (comment_id,))
    
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
        if records[0][0] == 1: # Post was already liked by the user, so unlike it
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
            
        ## Check if the user has also disliked the post, if so - remove their dislike and decrement the total dislikes
        sql = """
            SELECT disliked
            FROM Post_Interaction
            WHERE post_id = %s AND username = %s
        """
        cursor.execute(sql, (post_id, user))
        records = cursor.fetchall()
        if len(records) > 0:
            if records[0][0] == 1: # Post was already disliked by the user, so remove dislike
                sql = """
                    UPDATE Post_Interaction
                    SET disliked = 0
                    WHERE post_id = %s AND username = %s
                """
                cursor.execute(sql, (post_id, user))
                sql = """
                    UPDATE Posts p
                    SET dislikes = dislikes - 1
                    WHERE p.post_id = %s
                """
                cursor.execute(sql, (post_id,))
                
                 
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

    # check status of whether user has disliked this post or not.
    sql = """
        SELECT disliked
        FROM Post_Interaction
        WHERE post_id = %s AND username = %s
    """

    cursor.execute(sql, (post_id, user))
    records = cursor.fetchall()
    
    if len(records) > 0: # Post has been interacted with before
        if records[0][0] == 1: # Post was already disliked by the user, so remove dislike
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
            
        ## Check if the user has also liked the post, if so - remove their like and decrement the total likes
        sql = """
            SELECT liked
            FROM Post_Interaction
            WHERE post_id = %s AND username = %s
        """
        cursor.execute(sql, (post_id, user))
        records = cursor.fetchall()
        if len(records) > 0:
            if records[0][0] == 1: # Post was already liked by the user, so remove like
                sql = """
                    UPDATE Post_Interaction
                    SET liked = 0
                    WHERE post_id = %s AND username = %s
                """
                cursor.execute(sql, (post_id, user))
                sql = """
                    UPDATE Posts p
                    SET likes = likes - 1
                    WHERE p.post_id = %s
                """
                cursor.execute(sql, (post_id,))
            
            
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
        
        
    db.commit()
    cursor.close()
    db.close()


def update_user_location(user, location):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)

    sql = """
        UPDATE Users U
        SET locations = %s
        WHERE U.username = %s
    """

    cursor.execute(sql, (location, user))

    db.commit()
    cursor.close()
    db.close()


def likecomment(user, comment_id):    
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)

    # check status of whether user has liked this comment or not.
    sql = """
        SELECT liked
        FROM Comment_Interaction
        WHERE comment_id = %s AND username = %s
    """

    cursor.execute(sql, (comment_id, user))
    records = cursor.fetchall()
    
    if len(records) > 0: # Comment has been interacted with before
        if records[0][0] == 1: # Comment was already liked by the user, so unlike it
            # Decrement the likes in Comments
            sql = """
               UPDATE Comments c
               SET likes = likes - 1
               WHERE c.comment_id = %s
            """
            cursor.execute(sql, (comment_id,))

            # Unlike the comment in Comment_Interaction
            sql = """
               UPDATE Comment_Interaction
               SET liked = 0
	           WHERE comment_id = %s AND username = %s
            """
            cursor.execute(sql, (comment_id, user))
            
            
        else: # Comment has not been liked by the user
            # Increment the likes in Comment
            sql = """
               UPDATE Comments c
               SET likes = likes + 1
               WHERE c.comment_id = %s
            """
            cursor.execute(sql, (comment_id,))

            sql = """
               UPDATE Comment_Interaction
               SET liked = 1
               WHERE comment_id = %s AND username = %s
            """
            cursor.execute(sql, (comment_id, user))
            
        ## Check if the user has also disliked the comment, if so - remove their dislike and decrement the total dislikes
        sql = """
            SELECT disliked
            FROM Comment_Interaction
            WHERE comment_id = %s AND username = %s
        """
        cursor.execute(sql, (comment_id, user))
        records = cursor.fetchall()
        if len(records) > 0:
            if records[0][0] == 1: # Comment was already disliked by the user, so remove dislike
                sql = """
                    UPDATE Comment_Interaction
                    SET disliked = 0
                    WHERE comment_id = %s AND username = %s
                """
                cursor.execute(sql, (comment_id, user))
                sql = """
                    UPDATE Comments c
                    SET dislikes = dislikes - 1
                    WHERE c.comment_id = %s
                """
                cursor.execute(sql, (comment_id,))
                
                 
    else: # Comment has not been interacted with until now
        # Increment the likes in Comments
        sql = """
           UPDATE Comments c
           SET likes = likes + 1
           WHERE c.comment_id = %s
        """
        cursor.execute(sql, (comment_id,))
	
        # User likes the comment for the first time
        sql = """
            INSERT INTO Comment_Interaction (comment_id, username, liked, disliked)
            VALUES (%s, %s, 1, 0)
        """
        cursor.execute(sql, (comment_id, user))
        
    
    db.commit()
    cursor.close()
    db.close()
    
def dislikecomment(user, comment_id):
    db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
    )
    cursor = db.cursor(prepared=True)

    # check status of whether user has disliked this comment or not.
    sql = """
        SELECT disliked
        FROM Comment_Interaction
        WHERE comment_id = %s AND username = %s
    """

    cursor.execute(sql, (comment_id, user))
    records = cursor.fetchall()
    
    if len(records) > 0: # Comment has been interacted with before
        if records[0][0] == 1: # Comment was already disliked by the user, so remove dislike
            # Decrement the dislikes in Comments
            sql = """
               UPDATE Comments c
               SET dislikes = dislikes - 1
               WHERE c.comment_id = %s
            """
            cursor.execute(sql, (comment_id,))

            # Remove dislike of the comment in Comment_Interaction
            sql = """
               UPDATE Comment_Interaction
               SET disliked = 0
	           WHERE comment_id = %s AND username = %s
            """
            cursor.execute(sql, (comment_id, user))
            
            
        else: # Comment has not been disliked by the user
            # Increment the disliked in Comments
            print("Comment has been interacted with before, but not liked currently - liking Comment")
            sql = """
               UPDATE Comments c
               SET dislikes = dislikes + 1
               WHERE c.comment_id = %s
            """
            cursor.execute(sql, (comment_id,))

            sql = """
               UPDATE Comment_Interaction
               SET disliked = 1
               WHERE comment_id = %s AND username = %s
            """
            cursor.execute(sql, (comment_id, user))
            
        ## Check if the user has also liked the post, if so - remove their like and decrement the total likes
        sql = """
            SELECT liked
            FROM Comment_Interaction
            WHERE comment_id = %s AND username = %s
        """
        cursor.execute(sql, (comment_id, user))
        records = cursor.fetchall()
        if len(records) > 0:
            if records[0][0] == 1: # Comment was already liked by the user, so remove like
                sql = """
                    UPDATE Comment_Interaction
                    SET liked = 0
                    WHERE comment_id = %s AND username = %s
                """
                cursor.execute(sql, (comment_id, user))
                sql = """
                    UPDATE Comments c
                    SET likes = likes - 1
                    WHERE c.comment_id = %s
                """
                cursor.execute(sql, (comment_id,))
            
            
    else: # Comment has not been interacted with until now
        # Increment the dislikes in Comments
        sql = """
           UPDATE Comments c
           SET dislikes = dislikes + 1
           WHERE c.comment_id = %s
        """
        cursor.execute(sql, (comment_id,))
        # User dislikes the comment for the first time
        sql = """
            INSERT INTO Comment_Interaction (comment_id, username, liked, disliked)
            VALUES (%s, %s, 0, 1)
        """
        cursor.execute(sql, (comment_id, user))
        
        
    db.commit()
    cursor.close()
    db.close()


##  TEST AREA
# run only one createpost at a time for now.
# createpost("nicklesimba", "Champaign", "ayo", "")
# createpost("someUser123", "Champaign", "what's goooood?", "test")
# frontend_code = feed_query("nicklesimba") # more frontend code would follow to format and display it
# print(frontend_code)
# feed_query("nicklesimba")
