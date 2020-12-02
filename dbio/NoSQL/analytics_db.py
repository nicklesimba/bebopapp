import pymongo
import datetime

client = pymongo.MongoClient("mongodb://mongwell.duckdns.org:27017")
analyticsDB = client['BebopAnalytics']


class AnalyticsDB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongwell.duckdns.org:27017")
        self.db = self.client['BebopAnalytics']
        self.postDataColl = self.db['PostData']
    

    def add_new_post_data(self, postID, username, location, tags, timeOfDay, messageLength):
        document = {}
        document['post_id'] = postID
        document['username'] = username
        document['tod'] = timeOfDay
        document['location'] = location
        document['tag'] = tags
        document['post_length'] = messageLength
        document['post_date'] = datetime.datetime.fromtimestamp(int(postID)).strftime('%Y-%m-%d')

        self.postDataColl.insert_one(document)


    def collect_user_data(self, username):
        matchDict = {}
        projectDict = {}
        matchDict['username'] = username
        projectDict['_id'] = 0
        return self.postDataColl.find(matchDict, projectDict)
