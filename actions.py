# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

base_url = "http://api.weatherapi.com/v1/{}.json?key=ea68642fb5ae4a3ea82101516201502&q={}"
search_modes = {
    "current":"",
    "forecast":"&days={}",
    "history":"&dt={}",
    "astronomy":"&dt={}"
}
response_templates = {
    "current":"Temperature:{}\nCondition:{}",
    "someday":"Max Temperature:{}\nMin Temperature:{}\nCondition:{}\n"
}

def create_url(search_mode,paras):
    #cat all querys
    url = base_url
    if search_mode in search_modes.keys():
        url += search_modes[search_mode]
    #fill in parameters
    
    paras.insert(0,search_mode)
    url = url.format(*paras)
    return url

class ActionGetWeather(Action):
    
    def name(self) -> Text:
        return "action_get_weather"
        
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #search_mode = tracker.get_slot("search_mode")
        search_mode = "current"
        city = tracker.get_slot("city")
        paras = [city]
        
        if search_mode == "forecast":
            days = tracker.get_slot("days")
            paras.append(days)
        elif search_mode == "history" or search_mode == "astronomy":
            date = tracker.get_slot("date")
            paras.append(date)
        
        
        full_url = create_url(search_mode,paras)
        result = requests.get(full_url).json()
        print(full_url)
        print(result)
        if result.get("error"):
            error_message = result["error"]
            dispatcher.utter_message(text="Error")
            return [SlotSet("weather_info","null")]
        else:
            #extract infos according to search mode
            response_text = "Weather Infomation:\n"
            if search_mode == "current":
                current = result["current"]
                temp_c = current["temp_c"]
                condition = current["condition"]
                response_text += response_templates[search_mode].format(temp_c,condition["text"])
            elif search_mode == "forecast":
                forecast_days = result["forecast"]["forecastday"]
                for day in forecast_days:
                    response_text += response_templates["day"].format(day["day"]["maxtemp_c"],day["day"]["mintemp_c"],day["day"]["condition"]["text"])
            elif search_mode == "history":
                response_text += response_templates["day"].format(all_day["maxtemp_c"],all_day["mintemp_c"],all_day["condition"]["text"])
            #elif search_mode == "astronomy"
       
        dispatcher.utter_message(text=response_text)
        return [SlotSet("weather_info",response_text)]
    
    