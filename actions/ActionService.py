import pymongo
import random
from datetime import datetime


class ActionService:

    list_over = ['trên', 'hơn', 'lớn hơn', 'cao hơn', 'nhiều hơn',
                 'nhiều h', 'sau', 'trở đi', 'trở ra', 'trở lên']
    list_under = ['dưới', 'ít hơn', 'thấp hơn', 'nhỏ hơn',
                  'kém hơn', 'kém h', 'trước', 'trở lại', 'trở xuống', 'trở về']
    list_middle = ['hiện tại', 'lúc này', 'bây giờ', 'đang',
                   'đamg mở', 'đang bán', 'bây giờ', "bây", "giờ"]

    def __init__(self, connection_url="mongodb+srv://damanh1211:AH8Gos6j2TQqakoD@foodycluster.brwq9u2.mongodb.net/", database_name="foody") -> None:
        self.connection_url = connection_url
        client = pymongo.MongoClient(self.connection_url)
        self.database = client[database_name]

    def parse_time(self, time_str):
        formats = ["%Hh%Mp", "% Hh%M", "%Hg%Mp",
                   "%Hgiờ%Mphút", "%H giờ", "%H:%M", "%Hh"]
        standardized_format = "%H:%M"

        for fmt in formats:
            try:
                parsed_time = datetime.strptime(
                    time_str, fmt).strftime(standardized_format)
                return parsed_time
            except ValueError:
                pass

        raise ValueError(time_str + " Invalid time format")

    def compare_times(self, time_str1, time_str2):
        time1 = self.parse_time(time_str1)
        time2 = self.parse_time(time_str2)

        return time1 <= time2

    def convert_price(self, shorthand_price):
        if isinstance(shorthand_price, str):
            price_pr = shorthand_price.replace(",", "").replace(
                "đ", "").replace(".", "").strip()
            if price_pr.endswith('k'):
                return int(price_pr[:-1]) * 1000
            return int(price_pr)
        return shorthand_price

    def get_spots_by_foodname_address(self, food_name="", address_food="", use_sort=False, use_limit=0):
        collection = self.database["EaterySpots"]

        pipeline = [
            {
                "$lookup":
                {
                    "from": "MenuItems",
                    "localField": "ID",
                    "foreignField": "ID",
                    "as": "items"
                }
            },
            {"$unwind": "$items"},
            {
                "$match":
                    {
                        "$and": [
                            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}},
                            {"items.Thông tin đồ ăn của quán": {"$elemMatch": {
                                "$or": [
                                    {"Tên đồ ăn": {
                                        "$regex": f"{food_name}", "$options": "i", }},
                                    {"Loại đồ ăn": {
                                        "$regex": f"{food_name}", "$options": "i", }},
                                ],
                            },
                            }
                            }
                        ]
                    }
            },
            {"$addFields": {
                "name": "$Tên quán",
                "address": "$Địa chỉ",
                "link":  "$Url"
            }
            },
            {"$project": {"name": 1, "address": 1, "link": 1, "_id": 0}},
        ]

        if use_sort:
            pipeline.append({"$sort": {"Đánh giá chung": -1}},)

        if use_limit > 0:
            pipeline.append({"$limit": use_limit})

        try:
            res = list(collection.aggregate(pipeline))
        except:
            res = []

        return res

    def get_food_name_with_price_address(self, food_name, start_price, end_price, address_food="", num_objects=5):
        start_price = self.convert_price(start_price)
        end_price = self.convert_price(end_price)

        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        objs = []
        for obj in result:
            if (len(objs) < num_objects):
                id_obj = obj["ID"]
                food_in_obj = self.database["MenuItems"].find({"ID": id_obj})[
                    0]
                foods = food_in_obj["Thông tin đồ ăn của quán"]
                for food in foods:
                    if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                        price = self.convert_price(food['Giá'])
                        if (price >= start_price and price <= end_price):
                            objs.append(obj)
                            break
        top_names = [{"name": obj['Tên quán'],
                      "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
        return top_names

    def get_food_name_with_type_price(self, food_name, price_type, start_price, address_food="hà nội"):
        if price_type in self.list_over:
            end_price = float("inf")
            list = self.get_food_name_with_price_address(
                food_name, start_price, end_price, address_food)
            if list is not None or len(list) > 0:
                if len(list) > 5:
                    list = random.sample(list, 5)
                return list
        elif price_type in self.list_under:
            end_price = start_price
            start_price = 0
            list = self.get_food_name_with_price_address(
                food_name, start_price, end_price, address_food)
            if list is not None or len(list) > 0:
                if len(list) > 5:
                    list = random.sample(list, 5)
                return list
        else:
            return []

    def get_address_price(self, address_food, start_price, end_price, num_objects=5):
        start_price = self.convert_price(start_price)
        end_price = self.convert_price(end_price)

        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        objs = []

        for obj in result:
            if (len(objs) < num_objects):
                id_obj = obj["ID"]
                food_in_obj = self.database["MenuItems"].find({"ID": id_obj})[
                    0]
                foods = food_in_obj["Thông tin đồ ăn của quán"]
                for food in foods:
                    price = self.convert_price(food['Giá'])
                    if (price >= start_price and price <= end_price):
                        food['Tên đồ ăn'] = food['Tên đồ ăn']
                        food['Giá'] = food['Giá']
                        food['Tên quán'] = obj['Tên quán']
                        food['Địa chỉ'] = obj['Địa chỉ']
                        food['Url'] = obj['Url']
                        objs.append(food)

        if objs is not None or len(objs) > 0:
            if len(objs) > 10:
                objs = random.sample(objs, 10)

        return objs

    def get_address_type_price(self, address_food, price_type, start_price):
        if price_type in self.list_over:
            end_price = float("inf")
            list = self.get_address_price(address_food, start_price, end_price)
            return list
        elif price_type in self.list_under:
            end_price = 0
            list = self.get_address_price(address_food, start_price, end_price)
            return list
        else:
            return []

    def get_price(self, start_price, end_price, num_objects=5):
        start_price = self.convert_price(start_price)
        end_price = self.convert_price(end_price)

        collection = self.database["EaterySpots"]
        result = collection.find().sort("Đánh giá chung", -1)
        objs = []

        for obj in result:
            if (len(objs) < num_objects):
                id_obj = obj["ID"]
                food_in_obj = self.database["MenuItems"].find({"ID": id_obj})[
                    0]
                foods = food_in_obj["Thông tin đồ ăn của quán"]
                for food in foods:
                    price = self.convert_price(food['Giá'])
                    if (price >= start_price and price <= end_price):
                        food['Tên đồ ăn'] = food['Tên đồ ăn']
                        food['Giá'] = food['Giá']
                        food['Tên quán'] = obj['Tên quán']
                        food['Địa chỉ'] = obj['Địa chỉ']
                        food['Url'] = obj['Url']
                        objs.append(food)

        if objs is not None or len(objs) > 0:
            if len(objs) > 10:
                objs = random.sample(objs, 10)

        return objs

    def get_type_price(self, price_type, start_price):
        if price_type in self.list_over:
            end_price = float("inf")
            list = self.get_price(start_price, end_price)
            return list
        elif price_type in self.list_under:
            end_price = 0
            list = self.get_price(start_price, end_price)
            return list
        else:
            return []

    def get_food_name_with_time_address(self, food_name, start_time, end_time, address_food):
        objs = []
        number = 0
        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        for obj in result:
            have_food = False
            time_obj = []
            id_obj = obj["ID"]
            food_in_obj = self.database["MenuItems"].find({"ID": id_obj})[0]
            food_in_obj_time = self.database["OperatingHours"].find({"ID": id_obj})[
                0]
            foods = food_in_obj["Thông tin đồ ăn của quán"]
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    have_food = True
                    break
            if have_food:
                times = food_in_obj_time["Thời gian đặt hàng"]
                if times and len(times) > 0:
                    for time in times:
                        if isinstance(time, dict):
                            if self.compare_times(time["Start_time"], start_time) and self.compare_times(end_time, time["End_time"]):
                                time_obj.append(str(time["Week_day"]))
                                number += 1

                if len(time_obj) > 0:
                    obj['time'] = time_obj
                    objs.append(obj)

        if objs is not None or len(objs) > 0:
            if len(objs) > 5:
                objs = random.sample(objs, 5)
        for obj in objs:
            obj['name'] = obj['Tên quán']
            obj['address'] = obj['Địa chỉ']
            obj['link'] = obj['Url']
            time_list = []
            for time_obj in obj['time']:
                if time_obj == "1":
                    time_list.append("Thứ 2")
                elif time_obj == "2":
                    time_list.append("Thứ 3")
                elif time_obj == "3":
                    time_list.append("Thứ 4")
                elif time_obj == "4":
                    time_list.append("Thứ 5")
                elif time_obj == "5":
                    time_list.append("Thứ 6")
                elif time_obj == "6":
                    time_list.append("Thứ 7")
                elif time_obj == "7":
                    time_list.append("Chủ nhật")
            obj['time'] = ", ".join(time_list)

        top_names = [{"name": obj['name'], "address":obj["address"],
                      "link": obj["link"], "time": obj["time"]} for obj in objs]
        return top_names

    def get_food_name_with_type_time_address(self, food_name, start_time, week_day, address_food):
        objs = []
        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        for obj in result:
            have_food = False
            id_obj = obj["ID"]
            food_in_obj = self.database["MenuItems"].find({"ID": id_obj})[0]
            food_in_obj_time = self.database["OperatingHours"].find({"ID": id_obj})[
                0]
            foods = food_in_obj["Thông tin đồ ăn của quán"]
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    have_food = True
                    break
            if have_food:
                times = food_in_obj_time['Thời gian đặt hàng']
                if times and len(times) > 0:
                    for time in times:
                        if isinstance(time, dict):
                            if self.compare_times(time["Start_time"], start_time) and self.compare_times(start_time, time["End_time"]) and week_day == time["Week_day"]:
                                objs.append(obj)
                                break

        if objs is not None or len(objs) > 0:
            if len(objs) > 5:
                objs = random.sample(objs, 5)

        top_names = [{"name": obj['Tên quán'],
                      "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
        return top_names

    def get_food_name_with_now_address(self, food_name, address_food):
        current_time = datetime.now()
        start_time = current_time.strftime("%H:%M")
        week_day = current_time.weekday()
        list = self.get_food_name_with_type_time_address(
            food_name, start_time, week_day, address_food)
        return list

    def get_food_name_with_type_time_address1(self, food_name, start_time, time_type, address_food):
        if time_type in self.list_over:
            end_time = "23:59"
            list = self.get_food_name_with_time_address(
                food_name, start_time, end_time, address_food)
            return list
        elif time_type in self.list_under:
            end_time = "00:00"
            list = self.get_food_name_with_time_address(
                food_name, start_time, end_time, address_food)
            return list

    def get_time_address(self, start_time, end_time, address_food):
        objs = []
        number = 0
        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        for obj in result:
            time_obj = []
            id_obj = obj["ID"]
            times = self.database["OperatingHours"].find({"ID": id_obj})[0]
            if times and len(times) > 0:
                for time in times:
                    if isinstance(time, dict):
                        if self.compare_times(time["Start_time"], start_time) and self.compare_times(end_time, time["End_time"]):
                            time_obj.append(str(time["Week_day"]))
                            number += 1

            if len(time_obj) > 0:
                obj['time'] = time_obj
                objs.append(obj)

        if objs is not None or len(objs) > 0:
            if len(objs) > 10:
                objs = random.sample(objs, 10)
        for obj in objs:
            obj['name'] = obj['Tên quán']
            obj['address'] = obj['Địa chỉ']
            obj['link'] = obj['Url']
            time_list = []
            for time_obj in obj['time']:
                if time_obj == "1":
                    time_list.append("Thứ 2")
                elif time_obj == "2":
                    time_list.append("Thứ 3")
                elif time_obj == "3":
                    time_list.append("Thứ 4")
                elif time_obj == "4":
                    time_list.append("Thứ 5")
                elif time_obj == "5":
                    time_list.append("Thứ 6")
                elif time_obj == "6":
                    time_list.append("Thứ 7")
                elif time_obj == "7":
                    time_list.append("Chủ nhật")
            obj['time'] = ", ".join(time_list)

        top_names = [{"name": obj['name'], "address":obj["address"],
                      "link": obj["link"], "time": obj["time"]} for obj in objs]
        return top_names

    def get_address_now(self, address_food):
        current_time = datetime.now()
        start_time = current_time.strftime("%H:%M")
        week_day = current_time.weekday()
        collection = self.database["EaterySpots"]
        result = collection.find(
            {"Địa chỉ": {"$regex": f"{address_food}", "$options": "i"}}).sort("Đánh giá chung", -1)
        objs = []
        for obj in result:
            id_obj = obj["ID"]
            times = self.database["OperatingHours"].find({"ID": id_obj})[0]
            if times and len(times) > 0:
                for time in times:
                    if isinstance(time, dict):
                        if self.compare_times(time["Start_time"], start_time) and self.compare_times(start_time, time["End_time"]) and week_day == time["Week_day"]:
                            objs.append(obj)
                            break
        if objs is not None or len(objs) > 0:
            if len(objs) > 5:
                objs = random.sample(objs, 5)

        top_names = [{"name": obj['Tên quán'],
                      "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
        return top_names
