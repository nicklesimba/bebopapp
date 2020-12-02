from __future__ import print_function

import mysql.connector as my

db = my.connect(
        host="localhost",
        database="bebop26dmnr_db", 
        user="bebop26dmnr_nicklesimba", 
        password="Yareyaredaze2643"  
)

cursor = db.cursor()

clear_post_interacts = """
   DELETE FROM Comment_Interaction
"""

number_of_rows = cursor.execute(clear_post_interacts)
print(number_of_rows)

db.commit()
db.close()
