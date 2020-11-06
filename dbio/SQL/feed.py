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
    print(db)
    cursor = db.cursor(prepared=True)
    print(cursor)

    # 1. query based on user, grab posts that are visible to them
	
    # Query the feed based on the location of the user which can be passed in
 
    sql = """
        SELECT post_id, post_message, location, tags, likes, dislikes, u.username
        FROM Posts p NATURAL JOIN Users u
        WHERE u.username = %s
        ORDER BY post_id
    """

    number_of_rows = cursor.execute(sql, (user,))
    records = cursor.fetchall()
    print(records)


    cursor.close()
    db.close()

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

    post_id = int(calendar.timegm(time.gmtime()))
    
    # leaving out reply_ids because it's a new post.
    sql = """
        INSERT INTO Posts (post_id, author, location, post_message, tags, reply_ids, likes, dislikes) 
        VALUES (%s, %s, %s, %s, %s, "", 0, 0)
    """
    query_tuple = (post_id, user, location, post_message, tags)

    number_of_rows = cursor.execute(sql, query_tuple)
    print(number_of_rows)

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
    cursor.execute(sql, (post_id,))

    # Also need to incorporate posted_by relation
    sql = """
        DELETE FROM Posted_By WHERE post_id = %s
    """
    cursor.execute(sql, (post_id,))

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

    # check status of whether user has liked this post or not.
    sql = """
        SELECT liked
        FROM Post_Interaction
        WHERE post_id = %s AND username = %s
    """

    cursor.execute(sql, (post_id, user))
    records = cursor.fetchall() # this and the following if statement may need work, idk if i'm accessing the value correctly!
    print('YO MY RECORDS ARE:')    
    print(records)    

    if len(records) > 0: #We've interacted with this post before
        if records[0] == 1: #It's currently liked, need to unlike it
            print('I have liked this post!')
            sql = """
               UPDATE Posts p
               SET likes = likes - 1
               WHERE p.post_id = %s
            """
            cursor.execute(sql, (post_id,))

            # user has marked post as liked, can't like it again
            sql = """
                UPDATE Post_Interaction
                SET liked = 0
	        WHERE post_id = %s AND username = %s
            """
            cursor.execute(sql, (post_id, user))
        else:
            #Post is not liked, need to like 
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
    else:              #Has this post never been liked
        sql = """
            UPDATE Posts p
            SET likes = likes + 1
	    WHERE p.post_id = %s
        """

        cursor.execute(sql, (post_id,))
	
        #User likes the post for the first time
        sql = """
            INSERT INTO Post_Interaction (post_id, username, liked, disliked)
            VALUES (%s, %s, 1, 0)
        """

        cursor.execute(sql, (post_id, user))
    db.commit()
    cursor.close()
    db.close()

# test area
# run only one createpost at a time for now.
# createpost("nicklesimba", "Champaign", "ayo", "")
# createpost("someUser123", "Champaign", "what's goooood?", "test")
frontend_code = feed_query("nicklesimba") # more frontend code would follow to format and display it
print(frontend_code)
