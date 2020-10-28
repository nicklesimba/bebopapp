from __future__ import print_function

import MySQLdb as my

db = my.connect(
    host="localhost", 
    user="bebop26dmnr_nicklesimba", 
    passwd="Yareyaredaze2643", 
    db="bebop26dmnr_db" 
)

print(db)

cursor = db.cursor()

print(cursor)

sql = """
    INSERT INTO Users (username, locations, prof_pic_url, password) 
    VALUES ("nicklesimba", "Urbana", "nikhil.com", "nikhils_password"), ("rammk1999", "Champaign", "ram.com", "rams_password"), ("MondoLongwell", "Champaign", "mondo.com", "maanus_password"), ("DivsB", "Champaign", "divyabhati.com", "divyas_password")
"""

number_of_rows = cursor.execute(sql)
print(number_of_rows)

sql = """
    INSERT INTO Posts (post_id, location, post_message, reply_ids, likes, dislikes)
    VALUES (1, "Champaign", "This is the 1st message put into the application", "", 0, 0)
"""

number_of_rows = cursor.execute(sql)
print(number_of_rows)

db.commit()
db.close()

