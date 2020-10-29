from __future__ import print_function

import MySQLdb as my

db = my.connect(
    host="localhost", 
    user="bebop26dmnr_nicklesimba", 
    passwd="Yareyaredaze2643", 
    db="bebop26dmnr_db" 
)

print(db)

cursor = db.cursor(prepared=True)

print(cursor)
'''
This is an attempt at one of the two advanced backend queries we're supposed to do. Stuff in "quotes" is example data to make it clear.
This query would essentially take the username "simha3", query for post_id in the Posted_By table NATURAL JOIN'd with Posts table.
This yields Posts that are created by "simha3". Then we can GROUP BY location "Champaign" and only keep posts made by "simha3" in "Champaign".
Finally, we can return the AVG(likes+dislikes) to get the average score of a user's posts in a particular location. 
'''
# https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/ 
# i'm using this for reference on parameterized queries. if i screw up use this link lol

sql = """
    SELECT (AVG(likes)+AVG(dislikes)) AS avgRatingInLoc, username
    FROM Posts p NATURAL JOIN Posted_By pb
    WHERE pb.username = %s AND p.location = %s
    GROUP BY p.location
"""

query_tuple = ("nicklesimba", "Champaign")

number_of_rows = cursor.execute(sql, query_tuple)
print(number_of_rows)

db.commit()
db.close()

