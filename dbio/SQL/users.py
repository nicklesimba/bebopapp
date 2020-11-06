import mysql.connector as connector

HOST="localhost"
DATABASE="bebop26dmnr_db"
USER="bebop26dmnr_nicklesimba"
PASSWORD="Yareyaredaze2643"  
USERNAME_LENGTH = 100
LOCATIONS_LENGTH = 255
PROF_PIC_URL_LENGTH = 255
PASSWORD_LENGTH = 255

createQuery = """
	INSERT INTO Users (username, locations, prof_pic_url, password)
		VALUES (%s, %s, %s, %s);
"""

checkNameQuery = """ SELECT username
	FROM Users
	WHERE username = %s
"""

def create_user(username, password, location, prof_pic_url=""): # may need more fields later
	"""
	Create a new user to store in the Users table.
	:param string username: Username login of new user being created.
	:param string password: Password to check on login of this user.
	:param string location: Starting location of user.
	:param string prof_pic_url: Profile picture link.
	:return: 
	"""

	# connect to the database
	db = connector.connect(
		host=HOST,
		database=DATABASE,
		user=USER,
		password=PASSWORD
	)

	# check parameter size for insertion into database
	if (len(username) > USERNAME_LENGTH):
		errStr = "Username exceeds " + str(USERNAME_LENGTH) + " characters."
		raise TypeError(errStr)
	elif (len(password) > PASSWORD_LENGTH):
		errStr = "Password exceeds " + str(PASSWORD_LENGTH) + " characters."
		raise TypeError(errStr)
	elif (len(location) > LOCATIONS_LENGTH):
		errStr = "Location exceeds " + str(LOCATIONS_LENGTH) + " characters."
		raise TypeError(errStr)
	elif (len(prof_pic_url) > PROF_PIC_URL_LENGTH):
		errStr = "Profile picture URL exceeds " + str(PROF_PIC_URL_LENGTH) + " characters."
		raise TypeError(errStr)

	cursor = db.cursor(buffered=True)
	cursor.execute(checkNameQuery, (username, ))
	numRows = cursor.rowcount
	cursor.close()

	if (numRows > 0):
		db.close()
		raise RuntimeError("Username taken.")
	else:
		cursor = db.cursor(buffered=True)
		cursor.execute(createQuery, (username, location, prof_pic_url, password))
		cursor.close()
		db.commit()
		db.close()

		


searchQuery = """
	SELECT username
	FROM Users
	WHERE username = %s AND password = %s
"""

def check_login(username, password):
	"""
	Check the login info by querying the database for the provided username and password.
	:param string username: Username of login to check.
	:param string password: Password of login to check.
	:return bool: True, if username-password combination exists in database,
			False if either does not
	"""

	# connect to the database
	db = connector.connect(
		host=HOST,
		database=DATABASE,
		user=USER,
		password=PASSWORD
	)

	cursor = db.cursor(buffered=True)

	cursor.execute(searchQuery, (username, password))
	numRows = cursor.rowcount

	# cleanup
	cursor.close()
	db.close()

	if (numRows == 1):
		return True
	else:
		return False
