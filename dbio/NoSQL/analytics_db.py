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
        document['post_id'] = int(postID)
        document['username'] = username
        document['tod'] = timeOfDay
        document['location'] = location
        document['tags'] = tags
        document['post_length'] = messageLength
        document['post_date'] = datetime.datetime.fromtimestamp(int(postID)).strftime('%Y-%m-%d')
        document['likes'] = 0
        document['dislikes'] = 0

        self.postDataColl.insert_one(document)
    
    def update_likes_on_post(self, postID, likes):
        matchDict = {}
        setDict = {}
        matchDict['post_id'] = int(postID)
        setDict['likes'] = likes
        
        setDict = { "$set": setDict }

        self.postDataColl.update_one(matchDict, setDict)

    def update_dislikes_on_post(self, postID, dislikes):
        matchDict = {}
        setDict = {}
        matchDict['post_id'] = int(postID)
        setDict['dislikes'] = dislikes
        
        setDict = { "$set": setDict }

        self.postDataColl.update_one(matchDict, setDict)


    def collect_user_data(self, username):
        matchDict = {}
        projectDict = {}
        matchDict['username'] = username
        projectDict['_id'] = 0
        return self.postDataColl.find(matchDict, projectDict)

    def aggregate_location_data(self, username):
        matchDict = {}
        projectDict = {}
        groupDict = {}
        sortDict = {}

        matchDict['username'] = username
        groupDict['_id'] = "$location"
        groupDict['count'] = { "$sum" : 1 }
        projectDict['_id'] = 0
        projectDict['location'] = "$_id"
        projectDict['count'] = 1
        sortDict['location'] = 1

        matchDict = { "$match": matchDict }
        groupDict = { "$group": groupDict }
        projectDict = { "$project": projectDict }
        sortDict = { "$sort": sortDict }

        return list(self.postDataColl.aggregate([matchDict, groupDict, projectDict, sortDict]))

    def aggregate_tag_usage(self, username):
        matchDict = {}
        projectDict = {}
        groupDict = {}
        sortDict = {}

        matchDict['username'] = username
        groupDict['_id'] = "$tags"
        groupDict['count'] = { "$sum" : 1 }
        projectDict['_id'] = 0
        projectDict['tag'] = "$_id"
        projectDict['count'] = 1
        sortDict['count'] = 1

        unwindDict = { "$unwind": "$tags" }
        matchDict = { "$match": matchDict }
        groupDict = { "$group": groupDict }
        projectDict = { "$project": projectDict }
        sortDict = { "$sort": sortDict }

        return list(self.postDataColl.aggregate([unwindDict, matchDict, groupDict, projectDict, sortDict]))

    def aggregate_recent_posts(self, username):
        matchDict = {}
        projectDict = {}
        sortDict = {}

        matchDict['username'] = username
        projectDict['_id'] = 0
        sortDict['post_id'] = -1

        matchDict = { "$match": matchDict }
        projectDict = { "$project": projectDict }
        sortDict = { "$sort": sortDict }
        limitDict = { "$limit" : 5 }

        return list(self.postDataColl.aggregate([matchDict, projectDict, sortDict, limitDict]))
    
    def aggregate_post_timeOfDay(self, username):
        matchDict = {}
        projectDict = {}

        matchDict['username'] = username
        projectDict['_id'] = 0
        projectDict['tod'] = 1

        return list(self.postDataColl.find(matchDict, projectDict))
