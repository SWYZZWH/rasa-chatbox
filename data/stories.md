## greet
* greet
    - utter_greet

## goodbye
* goodbye
    - utter_goodbye

## thankyou
* thankyou
    - utter_noworries

## bot challenge
* bot_challenge
    - utter_iamabot

## happy_path
* greet
    - utter_greet
    - utter_functions
* ask_current_weather{"city": "Shanghai"}    
    - action_get_weather
* thankyou
    - utter_noworries