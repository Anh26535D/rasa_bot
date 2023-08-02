import pymongo

client = pymongo.MongoClient("mongodb+srv://maitienthanh110402:Thanh101002@cluster0.u88s2mk.mongodb.net/")
if "foody" in client.list_database_names():
    database = client["foody"]
    print(database.list_collection_names())