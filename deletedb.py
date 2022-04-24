import pymongo

client = pymongo.MongoClient("mongodb+srv://freddieswift:NyNdZtz0lWSby7fh@cluster0.ny6zd.mongodb.net/sscDatabase?retryWrites=true&w=majority")
db = client["sscDatabase"]
collection = db["scrapingResult"]

collection.delete_many({})