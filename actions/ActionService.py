import pymongo

class ActionService:

    def __init__(self, connection_url="mongodb+srv://maitienthanh110402:Thanh101002@cluster0.u88s2mk.mongodb.net/", database_name="foody") -> None:
        self.connection_url = connection_url
        client = pymongo.MongoClient(self.connection_url)
        self.database = client[database_name]

    def get_top_names(self, num_objects, address_food):
        collection = self.database["mainContent"]
        res = collection.find({"Địa chỉ": { "$regex": f"{address_food}", "$options": "i" }}).sort("Đánh giá chung", -1)

        res = res[:num_objects]

        top_names = [{"name":obj["Tên quán"], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in res]
        return top_names
        
    