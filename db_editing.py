from __future__ import print_function

import MySQLdb as my

db = my.connect(
    host="localhost", 
    user="bebop26dmnr_nicklesimba", 
    passwd="Yareyaredaze2643", 
    db="bebop26dmnr_db" 
)
cursor = db.cursor()

clear_post_interacts = """
   DELETE *
   FROM Post_Interaction
"""

number_of_rows = cursor.execute(clear_post_interacts)
print(number_of_rows)

db.commit()
db.close()
