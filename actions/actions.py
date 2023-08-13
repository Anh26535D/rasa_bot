# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .ActionService import ActionService

class ActionTopRateAddress(Action):
    def name(self) -> Text:
        return "action_top_rate_address"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        action_service = ActionService()

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
            
        try:
            number_top_res_count = int(number_top_res)
        except:
            number_top_res_count = 5
    
        if (address_food is None) and (food_name is None):
            dispatcher.utter_message(text="Xin lỗi nhưng em không hiểu bạn muốn tìm thông tin về đồ ăn hay quán ăn nào?")
        elif (address_food is None) and (food_name is not None):
            top_names = action_service.get_top_food(number_top_res_count, food_name)
            if len(top_names) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa có dữ liệu về món ăn " + food_name)
            elif number_top_res is not None:
                dispatcher.utter_message(text="Em xin gợi ý top "+ number_top_res +" quán ăn có món " + food_name + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
            else:
                dispatcher.utter_message(text="Em xin gợi ý vài quán ăn có món " + food_name + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
        elif (address_food is not None) and (food_name is None):
            top_names = action_service.get_top_names(number_top_res_count, address_food)
            if len(top_names) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa có dữ liệu về quán ăn tại " + address_food)
            elif number_top_res:
                dispatcher.utter_message(text="Em xin gợi ý top "+ number_top_res +" quán ăn tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
            else:
                dispatcher.utter_message(text="Em xin gợi ý top vài quán ăn tại " + address_food + " là: \n" +  "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in top_names]))
        else:
            top_names = action_service.get_top_names_with_food(number_top_res_count, food_name, address_food)
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
        
        action_service = ActionService()

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
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
        elif food_name and start_price and price_type and address_food:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and address_food:
            list = action_service.get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and end_price:
            address_food = ""
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and price_type:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif address_food and start_price and end_price:
            list = action_service.get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif address_food and start_price and price_type:
            list = action_service.get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and end_price:
            list = action_service.get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and price_type:
            list = action_service.get_type_price(price_type, start_price)
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
        
        action_service = ActionService()

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
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
            return []
        
        if food_name and start_price and price_type and address_food:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
            return []
        
        if food_name and address_food:
            list = action_service.get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
            return []
        
        if food_name and start_price and end_price:
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
            return []
        
        if food_name and start_price and price_type:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
            return []
        
        if address_food and start_price and end_price:
            list = action_service.get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
            return []
        
        if address_food and start_price and price_type:
            list = action_service.get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
            return []
        
        if start_price and end_price:
            list = action_service.get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
            return []
        
        if start_price and price_type:
            list = action_service.get_type_price(price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
            return []
        
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
        
        action_service = ActionService()

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
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))       
        elif food_name and start_price and price_type and address_food:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price +".")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and address_food:
            list = action_service.get_food_name_with_address(food_name, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and end_price:
            address_food = ""
            list = action_service.get_food_name_with_price_address(food_name, start_price, end_price, address_food)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif food_name and start_price and price_type:
            list = action_service.get_food_name_with_type_price(food_name, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu về món ăn " + food_name + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in list]))
        elif address_food and start_price and end_price:
            list = action_service.get_address_price(address_food, start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif address_food and start_price and price_type:
            list = action_service.get_address_type_price(address_food, price_type, start_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu tại " + address_food + " với giá " + price_type + " " + start_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " với giá " + price_type + " " + start_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and end_price:
            list = action_service.get_price(start_price, end_price)
            if list is None or len(list) == 0:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại chưa tìm thấy dữ liệu với giá từ " + start_price + " đến " + end_price)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món với giá từ " + start_price + " đến " + end_price + " là: \n" + "\n".join([f"* Tên món: {food['Tên đồ ăn']}, Giá: {food['Giá']}, Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in list]))
        elif start_price and price_type:
            list = action_service.get_type_price(price_type, start_price)
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
        
        action_service = ActionService()

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
            temp_objs = action_service.get_food_name_with_time_address(food_name, start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}, \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and address_food and time_type in action_service.list_middle:
            temp_objs = action_service.get_food_name_with_now_address(food_name, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in temp_objs]))
        elif food_name and address_food and time_type and start_time:
            temp_objs = action_service.get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " tại " + address_food + " vào khung giờ " + time_type + " " + start_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " tại " + address_food + " vào khung giờ " + time_type + " " + start_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}, \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and start_time and end_time:
            address_food = ""
            temp_objs = action_service.get_food_name_with_time_address(food_name, start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']} , \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif food_name and time_type in action_service.list_middle:
            address_food = ""
            temp_objs = action_service.get_food_name_with_now_address(food_name, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']}" for obj in temp_objs]))
        elif food_name and start_time and time_type:
            address_food = ""
            temp_objs = action_service.get_food_name_with_type_time_address1(food_name, start_time, time_type, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu về món ăn " + food_name + " vào khung giờ " + time_type + " " + start_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán có món ăn " + food_name + " vào khung giờ " + time_type + " " + start_time + " là: \n" + "\n".join([f"* Tên quán: {obj['name']}, Địa chỉ: {obj['address']}, Link mua hàng: {obj['link']} , \nThời gian bán vào các thứ: {obj['time']}" for obj in temp_objs]))
        elif address_food and start_time and end_time:
            temp_objs = action_service.get_time_address(start_time, end_time, address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time)
            else:
                dispatcher.utter_message(text="Em xin gợi ý các quán tại " + address_food + " vào khung giờ từ " + start_time + " đến " + end_time + " là: \n" + "\n".join([f"* Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in temp_objs]))
        elif address_food and time_type in action_service.list_middle:
            temp_objs = action_service.get_address_now(address_food)
            if not temp_objs:
                dispatcher.utter_message(text="Em xin lỗi, hiện tại không tìm thấy dữ liệu tại " + address_food + " vào thời điểm hiện tại")
            else:
                dispatcher.utter_message(text="Em xin gợi ý các món tại " + address_food + " vào thời điểm hiện tại là: \n" + "\n".join([f"* Tên quán: {food['Tên quán']}, Địa chỉ: {food['Địa chỉ']}, Link mua hàng: {food['Url']}" for food in temp_objs]))
        else:
            dispatcher.utter_message(text="Xin lỗi bạn, em không hiểu bạn muốn tìm món ăn gì hay ở đâu?")

        return []