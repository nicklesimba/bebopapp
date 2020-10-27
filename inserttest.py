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
    VALUES ("nicklesimba", "Champaign", "haskellcurry.com", "nikhils_password"), ("rammk1999", "Champaign", "ram.com", "rams_password")
"""

number_of_rows = cursor.execute(sql)

print(number_of_rows)

db.close()

