import pymongo

client = pymongo.MongoClient("mongodb://mongwell.duckdns.org:27017")
analyticsDB = client['BebopAnalytics']


class AnalyticsDB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://mongwell.duckdns.org:27017")
        self.db = self.client['BebopAnalytics']
        self.postDataColl = self.db['PostData']
    

    def add_new_post_data(self, username, postID, timeOfDay):
        document = {}
        document['post_id'] = postID
        document['username'] = username
        document['tod'] = timeOfDay

        self.postDataColl.insert_one(document)


