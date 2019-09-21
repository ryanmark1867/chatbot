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

# movie db schema
movie_schema = {"ratings_small":["userId", "movieId","rating","timestamp"],
                "credit_small":["cast","crew","id"],
                "movies_metadata_small":["adult","belongs_to_collection","budget","genres","homepage","id","imdb_id","original_language","original_title",
                "overview","popularity","poster_path","production_companies","production_countries","release_date","revenue","runtime","spoken_languages",
                "status	tagline	title","video","vote_average","vote_count"],
                "keywords_small":["id","keywords"],
                "links_small":["movieId","imdbId","tmdbId"]}
                




class ActionFileColumns(Action):
   """ return the column names for a file """
   def name(self) -> Text:
      return "action_file_columns"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      csv_url = tracker.get_slot('file_name')
      df=pd.read_csv(csv_url)
      result = list(df)
      dispatcher.utter_message("Here is the list of column names for file:")
      dispatcher.utter_message(csv_url)
      for i in range(len(result)):
          dispatcher.utter_message(result[i]+" ")
      return []
      


class ActionFileRow(Action):
   """ return the values in a specific row """
   def name(self) -> Text:
      return "action_file_row"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      csv_url = tracker.get_slot('file_name')
      csv_row = int(tracker.get_slot('row_number'))
      df=pd.read_csv(csv_url)
      # get raw values from dataframe
      result = df.values
      header_output = "contents for row "+str(csv_row)+" are:"
      dispatcher.utter_message(header_output)
      #
      # convert all elements of the row to strings (dispather.utter_message will only output strings)
      str_array = [str(i) for i in result[csv_row]]
      # concatenate all the elements of the string cast arrage
      one_line_output = ", ".join(str_array)
      dispatcher.utter_message(one_line_output)
      #for i in range(len(result[csv_row])):
      #   dispatcher.utter_message(str(result[csv_row][i]))
      return []

class ActionFirstNRows(Action):
   """ return the values of the first n rows """
   def name(self) -> Text:
      return "action_first_n_rows"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      csv_url = tracker.get_slot('file_name')
      csv_row_range = int(tracker.get_slot('row_range'))
      df=pd.read_csv(csv_url)
      # get raw values from dataframe
      result = df.values
      header_output = "last "+str(csv_row_range)+" rows are:"
      dispatcher.utter_message(header_output)
      for j in range (csv_row_range):
         str_array = [str(i) for i in result[j]]
         one_line_output = ", ".join(str_array)
         dispatcher.utter_message(one_line_output)
      return []

   
class ActionLastNRows(Action):
   """return the values of the last n rows"""
   def name(self) -> Text:
      return "action_last_n_rows"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      csv_url = tracker.get_slot('file_name')
      csv_row_range = int(tracker.get_slot('row_range'))
      df=pd.read_csv(csv_url)
      number_rows = len(df.index)
      # get raw values from dataframe
      result = df.values
      header_output = "last "+str(csv_row_range)+" rows are:"
      dispatcher.utter_message(header_output)
      # iterate through the last n rows
      for j in range (number_rows-csv_row_range,number_rows):
         str_array = [str(i) for i in result[j]]
         one_line_output = ", ".join(str_array)
         dispatcher.utter_message(one_line_output)
      return []

class ActionRankColByOtherCol(Action):
   """return the list of values from one column ranked according to another column"""
   def name(self) -> Text:
      return "action_rank_col_by_other_col"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # give me the top 5 movies by budget
      # give me the [top_bottom] [row_range] [ranked_col} by [ranking_col]
      # give me the top 5 French movies by budget
      # give me the [top_bottom] [row_range] [ranked_col] by [ranking_col] where [condition_col] [condition_operator] [condition_value]
      # top movies from 2004
      # [top_bottom] [ranked_col] [by [ranking_col] assumed to be [popularity]] [condition_col][condition_value]
      # slots:
      # ranked_col
      # ranking_col
      # ascending_descending
      # top_bottom
      # condition_col
      # condition_value
      # condition_operator
      ranked_col = tracker.get_slot('ranked_col')
      ranking_col = tracker.get_slot('ranking_col')
      ascending_descending = tracker.get_slot('ascending_descending')
      top_bottom = tracker.get_slot('top_bottom')
      row_range = int(tracker.get_slot('row_range'))
      condition_col = tracker.get_slot('condition_col')
      condition_value = tracker.get_slot('condition_value')
      condition_operator = tracker.get_slot('condition_operator')

      # def map_cols_to_tables(col_dict):
      #     '''return the tables / files associated with each of the columns'''
      #     for col in col_dict:
      #        col_dict[col] = find_table(col)
      #     return(col_dict)
      #
      #
      

      
      # are ranked_col and ranking_col in the same file?
      return []
   
