# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import csv, json
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Đọc file JSON
with open('D:\Project2\chatbot2\data\datafoody.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionTopResRate(Action):

    def name(self) -> Text:
        return "action_top_res_rate"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        number_top_res = tracker.get_slot("number_top_res")
        if number_top_res:
             dispatcher.utter_message(text="Test message with number top rate " + str(number_top_res))
        else:
            dispatcher.utter_message(text="Test message with no number top rate")

        return []
    
class ActionAddressRes(Action):

    def name(self) -> Text:
        return "action_address_res"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        address_res = tracker.get_slot("address_res")
        if address_res:
            dispatcher.utter_message(text="Test message with local " + str(address_res))
        else:
            dispatcher.utter_message(text="Test message with no local")
        return []
    
class ActionFoodName(Action):

    def name(self) -> Text:
        return "action_food_name"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:            
            food_name = None
            address_res = None
            start_price = None
            end_price = None
            price_type = None

            entities = tracker.latest_message.get('entities', {})
            for entitie in entities:
                if entitie['entity'] == 'food_name' or entitie['entity'] == 'food_name_time':
                    food_name = entitie['value']
                elif entitie['entity'] == 'address_res':
                    address_res = entitie['value']
                elif entitie['entity'] == 'start_price':
                    start_price = entitie['value']
                elif entitie['entity'] == 'end_price':
                    end_price = entitie['value']
                elif entitie['entity'] == 'start_time':
                    start_time = entitie['value']
                elif entitie['entity'] == 'end_time':
                    end_time = entitie['value']
                elif entitie['entity'] == 'price_type':
                    price_type = entitie['value']
                elif entitie['entity'] == 'time_type':
                    time_type = entitie['value']
                            
        except:
                        print("test4-------------end")

        dispatcher.utter_message(text="Món ăn: " + str(food_name) + " Địa chỉ" + str(address_res) + " giá từ " + str(start_price) + " đến " + str(end_price)  +  str(price_type))
        # return []
    
class ActionFoodTime(Action):

    def name(self) -> Text:
        return "action_food_time"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        food_name = None
        address_res = None
        start_price = None
        end_price = None
        price_type = None
        start_time = None
        end_time = None
        time_type = None

        entities = tracker.latest_message.get('entities', {})

        for entitie in entities:
                            if entitie['entity'] == 'food_name' or entitie['entity'] == 'food_name_time':
                                food_name = entitie['value']
                            elif entitie['entity'] == 'address_res':
                                address_res = entitie['value']
                            elif entitie['entity'] == 'start_price':
                                start_price = entitie['value']
                            elif entitie['entity'] == 'end_price':
                                end_price = entitie['value']
                            elif entitie['entity'] == 'start_time':
                                start_time = entitie['value']
                            elif entitie['entity'] == 'end_time':
                                end_time = entitie['value']
                            elif entitie['entity'] == 'price_type':
                                price_type = entitie['value']
                            elif entitie['entity'] == 'time_type':
                                time_type = entitie['value']

        # print("test5-------------")
        # print(food_name)
        # print(address_res)
        # print(start_price)
        # print(end_price)
        # print(start_time)
        # print(end_time)
        # print(price_type)
        # print(time_type)
        # print("test5-------------end")

        dispatcher.utter_message(text=" thời gian từ " + str(start_time) + " đến " + str(end_time) + str(time_type))
        return []