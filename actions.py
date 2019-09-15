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
#         dispatcher.utter_message("Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

class ActionFileColumns(Action):
   def name(self) -> Text:
      return "action_file_columns"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      dispatcher.utter_message("Here is the list of column names 1")
      csv_url = tracker.get_slot('file_name')
      df=pd.read_csv(csv_url)
      result = list(df)
      dispatcher.utter_message("Here is the list of column names 2")
      for i in range(len(result)):
          dispatcher.utter_message(result[i]+" ")
      return []
      


class ActionFileRow(Action):
   def name(self) -> Text:
      return "action_file_row"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      csv_url = tracker.get_slot('file_name')
      csv_row = tracker.get_slot('row_number')
      df=pd.read_csv(csv_url)
      result = list(df)
      dispatcher.utter_message("Here is column ",csv_row)
      dispathcer.utter_message(df.iloc[[csv_row]])
      return []
   
