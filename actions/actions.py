# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import csv, json
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

# Đọc file JSON
with open("D:\Project2\RasaChatbot\data\data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    data = sorted(data, key=lambda item: item.get("Đánh giá chung", 0), reverse=True)

list_over = ['trên', 'hơn', 'lớn hơn', 'cao hơn', 'nhiều hơn', 'nhiều h', 'sau', 'trở đi', 'trở ra', 'trở lên']
list_under = ['dưới', 'ít hơn', 'thấp hơn', 'nhỏ hơn', 'kém hơn', 'kém h', 'trước', 'trở lại', 'trở xuống', 'trở về']
list_middle = ['hiện tại', 'lúc này', 'bây giờ', 'đang', 'đamg mở', 'đang bán', 'bây giờ', "bây", "giờ"]

def get_top_names(top_names_count, address_food):
    objsTop = []
    number = 0
    min_overallRating = float(0)
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            if number <= top_names_count:
                min_overallRating = float(obj['Đánh giá chung'])
                objsTop.append(obj)
                number += 1
                continue
            else:
                if float(obj['Đánh giá chung']) == min_overallRating:
                    objsTop.append(obj)
                    continue
                else:
                    break
    randomObjs = []
    if number < top_names_count:
        randomObjs = objsTop
    else:
        randomObjs = random.sample(objsTop, top_names_count)

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in randomObjs]
    return top_names

def get_top_food(top_names_count, food_name):
    objsTop = []
    number = 0
    min_overallRating = float(0)
    for obj in data:
        if number > top_names_count and float(obj['Đánh giá chung']) < min_overallRating:
            break
        foods = obj['Thông tin đồ ăn của quán']
        for food in foods:
            if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                min_overallRating = float(obj['Đánh giá chung'])
                objsTop.append(obj)
                number += 1
                break

    randomObjs = []
    if number < top_names_count:
        randomObjs = objsTop
    else:
        randomObjs = random.sample(objsTop, top_names_count)

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in randomObjs]
    return top_names

def get_top_names_with_food(top_names_count, food_name, address_food):
    objsTop = []
    number = 0
    min_overallRating = float(0)
    for obj in data:
        if number > top_names_count and float(obj['Đánh giá chung']) < min_overallRating:
            break
        if address_food.lower() in obj['Địa chỉ'].lower():
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    min_overallRating = float(obj['Đánh giá chung'])
                    objsTop.append(obj)
                    number += 1
                    break

    randomObjs = []
    if number < top_names_count:
        randomObjs = objsTop
    else:
        randomObjs = random.sample(objsTop, top_names_count)

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in randomObjs]
    return top_names

def get_food_name(food_name):
    lists = []
    for obj in data:
        foods = obj['Thông tin đồ ăn của quán']
        for food in foods:
            if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                lists.append(obj)
                break
    if lists and len(lists) > 5:
        lists = random.sample(lists, 5)
    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in lists]
    return top_names

def get_address_food(address_food):
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            objs.append(obj)
    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    return top_names

def get_food_name_with_address(food_name, address_food):
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    objs.append(obj)
                    break

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    return top_names

def get_food_name_with_price_address(food_name, start_price, end_price, address_food):
    start_price = convert_price(start_price)
    end_price = convert_price(end_price)
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    price = convert_price(food['Giá'])
                    if (price >= start_price and price <= end_price) or (price <= start_price and price >= end_price):
                        objs.append(obj)
                        break
    if objs is not None or len(objs) > 0:
        if len(objs)>5:
            objs = random.sample(objs, 5)
    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    return top_names
  
# def get_food_name_with_price(food_name, start_price, end_price):
    # start_price = convert_price(start_price)
    # end_price = convert_price(end_price)
    # objs = []
    # for obj in data:
    #         foods = obj['Thông tin đồ ăn của quán']
    #         for food in foods:
    #             if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
    #                 price = convert_price(food['Giá'])
    #                 if (price >= start_price and price <= end_price) or (price <= start_price and price >= end_price):
    #                     objs.append(obj)
    #                     break

    # if objs is not None or len(objs) > 0:
    #     if len(objs)>5:
    #         objs = random.sample(objs, 5)
    # top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    # return top_names

def get_food_name_with_type_price(food_name, price_type, start_price):
    address_food = ""
    if price_type in list_over:
        end_price = float("inf")
        list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
        if list is not None or len(list) > 0:
            if len(list)>5:
                list = random.sample(list, 5)
            return list
    elif price_type in list_under:
        end_price = 0
        list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
        if list is not None or len(list) > 0:
            if len(list)>5:
                list = random.sample(list, 5)
            return list
    else:
        return []
    
def get_address_price(address_food, start_price, end_price):
    start_price = convert_price(start_price)
    end_price = convert_price(end_price)
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            # select_food = []
            for food in obj['Thông tin đồ ăn của quán']:
                price = convert_price(food['Giá'])
                if (price >= start_price and price <= end_price) or (price <= start_price and price >= end_price):

                    food['Tên đồ ăn'] = food['Tên đồ ăn']
                    food['Giá'] = food['Giá']
                    food['Tên quán'] = obj['Tên quán']
                    food['Địa chỉ'] = obj['Địa chỉ']
                    food['Url'] = obj['Url']
                    objs.append(food)

    if objs is not None or len(objs) > 0:
        if len(objs)>10:
            objs = random.sample(objs, 10)

    return objs

def get_address_type_price(address_food, price_type, start_price):
    if price_type in list_over:
        end_price = float("inf")    
        list = get_address_price(address_food, start_price, end_price)
        return list
    elif price_type in list_under:
        end_price = 0
        list = get_address_price(address_food, start_price, end_price)
        return list
    else:
        return []

def get_price(start_price, end_price):
    start_price = convert_price(start_price)
    end_price = convert_price(end_price)
    objs = []
    for obj in data:
        for food in obj['Thông tin đồ ăn của quán']:
            price = convert_price(food['Giá'])
            if (price >= start_price and price <= end_price) or (price <= start_price and price >= end_price):
                food['Tên đồ ăn'] = food['Tên đồ ăn']
                food['Giá'] = food['Giá']
                food['Tên quán'] = obj['Tên quán']
                food['Địa chỉ'] = obj['Địa chỉ']
                food['Url'] = obj['Url']
                objs.append(food)

    if objs is not None or len(objs) > 0:
        if len(objs)>10:
            objs = random.sample(objs, 10)

    return objs

def get_type_price(price_type, start_price):
    if price_type in list_over:
        end_price = float("inf")
        list = get_price(start_price, end_price)
        return list
    elif price_type in list_under:
        end_price = 0
        list = get_price(start_price, end_price)
        return list
    else:
        return []

def get_food_name_with_time_address(food_name, start_time, end_time, address_food):
    objs = []
    number = 0 
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            have_food = False
            time_obj = []
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    have_food = True
                    break
            if have_food:
                times = obj['Thời gian đặt hàng']
                if times and len(times) > 0:
                    for time in times:
                            if isinstance(time, dict):
                                if compare_times(time["Start_time"], start_time) and compare_times(end_time, time["End_time"]):
                                    time_obj.append(str(time["Week_day"]))
                                    number += 1

                if len(time_obj) > 0:
                    obj['time'] = time_obj
                    objs.append(obj)

    if objs is not None or len(objs) > 0:
        if len(objs)>5:
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

    top_names = [{"name":obj['name'], "address":obj["address"], "link": obj["link"], "time": obj["time"]} for obj in objs]
    return top_names

def get_food_name_with_type_time_address(food_name, start_time, week_day, address_food):
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            have_food = False
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    have_food = True
                    break
            if have_food:
                times = obj['Thời gian đặt hàng']
                if times and len(times) > 0:
                    for time in times:
                            if isinstance(time, dict):
                                if compare_times(time["Start_time"], start_time) and compare_times(start_time, time["End_time"]) and week_day==time["Week_day"]:
                                    objs.append(obj)
                                    break

    if objs is not None or len(objs) > 0:
        if len(objs)>5:
            objs = random.sample(objs, 5)

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    return top_names

# def get_food_name_with_type_time_address(food_name, start_time, end_time, address_food):
    objs = []
    number = 0 
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            have_food = False
            time_obj = []
            foods = obj['Thông tin đồ ăn của quán']
            for food in foods:
                if food_name.lower() in food['Tên đồ ăn'].lower() or food_name.lower() in food['Loại đồ ăn'].lower():
                    have_food = True
                    break
            if have_food:
                times = obj['Thời gian đặt hàng']
                if times and len(times) > 0:
                    for time in times:
                            if isinstance(time, dict):
                                if compare_times(time["Start_time"], start_time) and compare_times(end_time, time["End_time"]):
                                    time_obj.append(str(time["Week_day"]))
                                    number += 1

                if len(time_obj) > 0:
                    obj['time'] = time_obj
                    objs.append(obj)

    if objs is not None or len(objs) > 0:
        if len(objs)>5:
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

    top_names = [{"name":obj['name'], "address":obj["address"], "link": obj["link"], "time": obj["time"]} for obj in objs]
    return top_names

def get_food_name_with_now_address(food_name, address_food):
        current_time = datetime.now()
        start_time = current_time.strftime("%H:%M")
        week_day = current_time.weekday()
        list = get_food_name_with_type_time_address(food_name, start_time, week_day, address_food)
        return list

def get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food):
    if time_type in list_over:
        end_time = "23:59"
        list = get_food_name_with_time_address(food_name, start_time, end_time, address_food)
        return list
    elif time_type in list_under:
        end_time = "00:00"
        list = get_food_name_with_time_address(food_name, start_time, end_time, address_food)
        return list

def get_time_address(start_time, end_time, address_food):
    objs = []
    number = 0 
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            time_obj = []
            times = obj['Thời gian đặt hàng']
            if times and len(times) > 0:
                for time in times:
                        if isinstance(time, dict):
                            if compare_times(time["Start_time"], start_time) and compare_times(end_time, time["End_time"]):
                                time_obj.append(str(time["Week_day"]))
                                number += 1

            if len(time_obj) > 0:
                obj['time'] = time_obj
                objs.append(obj)

    if objs is not None or len(objs) > 0:
        if len(objs)>10:
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

    top_names = [{"name":obj['name'], "address":obj["address"], "link": obj["link"], "time": obj["time"]} for obj in objs]
    return top_names

def get_address_now(address_food):
    current_time = datetime.now()
    start_time = current_time.strftime("%H:%M")
    week_day = current_time.weekday()
    objs = []
    for obj in data:
        if address_food.lower() in obj['Địa chỉ'].lower():
            times = obj['Thời gian đặt hàng']
            if times and len(times) > 0:
                for time in times:
                        if isinstance(time, dict):
                            if compare_times(time["Start_time"], start_time) and compare_times(start_time, time["End_time"]) and week_day==time["Week_day"]:
                                objs.append(obj)
                                break
    if objs is not None or len(objs) > 0:
        if len(objs)>5:
            objs = random.sample(objs, 5)

    top_names = [{"name":obj['Tên quán'], "address":obj["Địa chỉ"], "link": obj["Url"]} for obj in objs]
    return top_names

def convert_price(price_str):
    if isinstance(price_str, str):
        price_pr = price_str.replace(",", "").replace("đ", "").replace(".", "").strip()
        if price_pr.endswith('k'):
            return int(price_pr[:-1]) * 1000
        return int(price_pr)
    return price_str

def parse_time(time_str):
    formats = ["%Hh%Mp", "%Hh%M", "%Hg%Mp", "%Hgiờ%Mphút", "%H giờ", "%H:%M", "%Hh"]
    standardized_format = "%H:%M"

    for fmt in formats:
        try:
            parsed_time = datetime.strptime(time_str, fmt).strftime(standardized_format)
            return parsed_time
        except ValueError:
            pass
    
    raise ValueError(time_str + " Invalid time format")

def compare_times(time_str1, time_str2):
    time1 = parse_time(time_str1)
    time2 = parse_time(time_str2)

    if time1 <= time2:
        return True
    else:
        return False


class ActionTopRateAddress(Action):
    def name(self) -> Text:
        return "action_top_rate_address"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        address_food = None
        number_top_res = None
        food_name = None

        entities = tracker.latest_message.get("entities", [])
        for e in entities:
            if e["entity"] == "address_food":
                address_food = e["value"]
            if e["entity"] == "number_top_res":
                number_top_res = e["value"]
            if e["entity"] == "food_name":
                food_name = e["value"]
            
        number_top_res_count = number_top_res and int(number_top_res) or 5    

        if address_food == None and food_name == None:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm quán ăn ở đâu?")
        elif address_food == None and food_name:
            top_names = get_top_food(number_top_res_count, food_name)
            if len(top_names) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa có dữ liệu về món ăn " + food_name)
            elif number_top_res != None:
                dispatcher.utter_message(text="Em xin gợi ý top "+ number_top_res +" quán ăn có món " + food_name + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
            else:
                dispatcher.utter_message(text="Em xin gợi ý vài quán ăn có món " + food_name + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
        elif address_food and food_name == None:
            top_names = get_top_names(number_top_res_count, address_food)
            if len(top_names) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa có dữ liệu về quán ăn tại " + address_food)
            elif number_top_res:
                dispatcher.utter_message(text="Em xin gợi ý top "+ number_top_res +" quán ăn tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
            else:
                dispatcher.utter_message(text="Em xin gợi ý top vài quán ăn tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
        else:
            top_names = get_top_names_with_food(number_top_res_count, food_name, address_food)
            if len(top_names) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa có dữ liệu về quán ăn tại " + address_food)
            elif number_top_res:
                dispatcher.utter_message(text="Em xin gợi ý top "+ number_top_res +" quán ăn có món " + food_name + " tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
            else:
                dispatcher.utter_message(text="Em xin gợi ý top vài quán ăn có món " + food_name + " tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))

        return []


class ActionFoodNameWithAddress(Action):
    def name(self) -> Text:
        return "action_food_name_with_address"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        food_name = None
        start_price = None
        end_price = None
        price_type = None
        address_food = None
        number = 0

        entities = tracker.latest_message.get("entities", [])
        for e in entities:
            if e["entity"] == "food_name":
                food_name = e["value"]
            if e["entity"] == "start_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "end_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "price_type":
                price_type = e["value"]
            if e["entity"] == "address_food":
                address_food = e["value"]

        if food_name and start_price and end_price and address_food: 
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
        elif food_name and start_price and price_type and address_food:
            list = get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and address_food:
            list = get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and end_price:
            address_food = ""
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and price_type:
            list = get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif address_food and start_price and end_price:
            list = get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif address_food and start_price and price_type:
            list = get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and end_price:
            list = get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and price_type:
            list = get_type_price(price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"*Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        else:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm món ăn gì hay ở đâu?")


        return []


class ActionFoodNameWithPrice(Action):
    def name(self) -> Text:
        return "action_food_name_with_price"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        food_name = None
        start_price = None
        end_price = None
        price_type = None
        address_food = None
        number = 0

        entities = tracker.latest_message.get("entities", [])
        for e in entities:
            if e["entity"] == "food_name":
                food_name = e["value"]
            if e["entity"] == "start_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "end_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "price_type":
                price_type = e["value"]
            if e["entity"] == "address_food":
                address_food = e["value"]

        if food_name and start_price and end_price and address_food: 
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
        elif food_name and start_price and price_type and address_food:
            list = get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and address_food:
            list = get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and end_price:
            address_food = ""
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and price_type:
            list = get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif address_food and start_price and end_price:
            list = get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif address_food and start_price and price_type:
            list = get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and end_price:
            list = get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and price_type:
            list = get_type_price(price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        else:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm món ăn gì hay ở đâu?")


        return []


class ActionFoodNameWithPriceAddress(Action):
    def name(self) -> Text:
        return "action_food_name_with_price_address"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        food_name = None
        start_price = None
        end_price = None
        price_type = None
        address_food = None
        number = 0

        entities = tracker.latest_message.get("entities", [])
        for e in entities:
            if e["entity"] == "food_name":
                food_name = e["value"]
            if e["entity"] == "start_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "end_price":
                if number == 0:
                    start_price = e["value"]
                    number += 1
                else:
                    end_price = e["value"]
            if e["entity"] == "price_type":
                price_type = e["value"]
            if e["entity"] == "address_food":
                address_food = e["value"]

        if food_name and start_price and end_price and address_food: 
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
        elif food_name and start_price and price_type and address_food:
            list = get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and address_food:
            list = get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and end_price:
            address_food = ""
            list = get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and price_type:
            list = get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif address_food and start_price and end_price:
            list = get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif address_food and start_price and price_type:
            list = get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and end_price:
            list = get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and price_type:
            list = get_type_price(price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        else:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm món ăn gì hay ở đâu?")


        return []


class ActionFoodTime(Action):
    def name(self) -> Text:
        return "action_food_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        food_name = None
        start_time = None
        end_time = None
        time_type = None
        address_food = None
        number = 0
        
        entities = tracker.latest_message.get("entities", [])
        for e in entities:
            if e["entity"] == "food_name":
                food_name = e["value"]
            if e["entity"] == "start_time":
                if number==0:
                    start_time = e["value"]
                    number += 1
                else:
                    end_time = e["value"]
            if e["entity"] == "end_time":
                if number==0:
                    start_time = e["value"]
                    number += 1
                else:
                    end_time = e["value"]
            if e["entity"] == "time_type":
                time_type = e["value"]
            if e["entity"] == "address_food":
                address_food = e["value"]
            if e["entity"] == "number_top_res":
                if number == 0:
                    start_time = e["value"]
                    number += 1
                else:
                    end_time = e["value"]
            if e["entity"] == "start_price":
                if number == 0:
                    start_time = e["value"]
                    number += 1
                else:
                    end_time = e["value"]
            if e["entity"] == "end_price":
                if number == 0:
                    start_time = e["value"]
                    number += 1
                else:
                    end_time = e["value"]
            
        if food_name and start_time and end_time and address_food:
            temp_objs = get_food_name_with_time_address(food_name, start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}, \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and address_food and time_type in list_middle:
            temp_objs = get_food_name_with_now_address(food_name, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in temp_objs]))
        elif food_name and address_food and time_type and start_time:
            temp_objs = get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào khung giờ " + time_type + " " + start_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào khung giờ " + time_type + " " + start_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}, \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and start_time and end_time:
            address_food = ""
            temp_objs = get_food_name_with_time_address(food_name, start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']} , \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and time_type in list_middle:
            address_food = ""
            temp_objs = get_food_name_with_now_address(food_name, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in temp_objs]))
        elif food_name and start_time and time_type:
            address_food = ""
            temp_objs = get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào khung giờ " + time_type + " " + start_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào khung giờ " + time_type + " " + start_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']} , \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif address_food and start_time and end_time:
            temp_objs = get_time_address(start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in temp_objs]))
        elif address_food and time_type in list_middle:
            temp_objs = get_address_now(address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu tại " + address_food + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in temp_objs]))
        else:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm món ăn gì hay ở đâu?")

        return []