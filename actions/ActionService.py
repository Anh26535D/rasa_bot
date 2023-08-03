import pymongo

# ONG THE TUNG
# def get_top_food(top_names_count, food_name):
# def get_top_names_with_food(top_names_count, food_name, address_food):
# def get_food_name(food_name):
# def get_address_food(address_food):
# def get_food_name_with_address(food_name, address_food):

# DAM VIET ANH
# def get_food_name_with_price_address(food_name, start_price, end_price, address_food):
# def get_food_name_with_type_price(food_name, price_type, start_price):
# def get_address_price(address_food, start_price, end_price):
# def get_address_type_price(address_food, price_type, start_price):
# def get_price(start_price, end_price):
# def get_type_price(price_type, start_price):

# LE DUY ANH
# def get_food_name_with_time_address(food_name, start_time, end_time, address_food):
# def get_food_name_with_type_time_address(food_name, start_time, week_day, address_food):
# def get_food_name_with_now_address(food_name, address_food):
# def get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food):
# def get_time_address(start_time, end_time, address_food):
# def convert_price(price_str):
# def parse_time(time_str):
# def compare_times(time_str1, time_str2):


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
    

        
    