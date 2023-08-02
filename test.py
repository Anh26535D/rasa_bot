import pymongo

client = pymongo.MongoClient("mongodb+srv://maitienthanh110402:Thanh101002@cluster0.u88s2mk.mongodb.net/")

database = client["foody"]


def get_top_names(num_objects, address_food):
    collection = database["mainContent"]
    res = collection.find({"Địa chỉ": { "$regex": f"{address_food}", "$options": "i" }}).sort("Đánh giá chung", -1)

    res = res[:num_objects]

    top_names = [{"name":obj["Tên quán"], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in res]
    return top_names

print(get_top_names(5, "hà nội"))