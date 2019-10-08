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
import ast

# define paths for movie dataset files

path_dict = {}
path_dict['links'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/links_small.csv'
path_dict['movies'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/movies_metadata_small.csv'
path_dict['ratings'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/ratings_small.csv'
path_dict['credits'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/credits_small.csv'
path_dict['keywords'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/keywords_small.csv'

# define columns in each file that are JSON formatted and need to be ast.literal_eval processed
json_dict = {}
json_dict['links'] = []
json_dict['movies'] = ['genres','production_companies','production_countries','spoken_languages',]
json_dict['ratings'] = []
# credits file currently corrputed - comment out literal_eval columns for it until corruption gets fixed
# json_dict['credits'] = ['cast','crew']
json_dict['credits'] = []
json_dict['keywords'] = ['keywords']

# define schema for dataset
movie_schema = {"ratings_small":["userId", "movieId","rating","timestamp"],
                "credit_small":["cast","crew","id"],
                "movies_metadata_small":["adult","belongs_to_collection","budget","genres","homepage","id","imdb_id","original_language","original_title",
                "overview","popularity","poster_path","production_companies","production_countries","release_date","revenue","runtime","spoken_languages",
                "status	tagline	title","video","vote_average","vote_count"],
                "keywords_small":["id","keywords"],
                "links_small":["movieId","imdbId","tmdbId"]}

# define synonyms (TODO see how to move at least a subset of these to Rasa level so they don't have to be maintained at Python layer)
slot_map = dict.fromkeys(['movies','movie name','title'],'original_title')
slot_map.update(dict.fromkeys(['plot','plot summary','plot statement'],'overview'))
slot_map.update(dict.fromkeys(['year','release date'],'release_date'))
slot_map.update(dict.fromkeys(['French'],'fr'))
slot_map.update(dict.fromkeys(['English'],'en'))
slot_map.update(dict.fromkeys(['German'],'de'))
slot_map.update(dict.fromkeys(['budget'],'budget'))
slot_map.update(dict.fromkeys(['revenue'],'revenue'))

# preload dataframes with datasets
# switch to serialize dataframes
save_files = False
# switch to load from serialized dataframes
saved_files = True
df_dict = {}
for file in path_dict:
   print("about to create df for ",file)
   if saved_files:
      df_dict[file] = pd.read_pickle(str(file))
   else:
      df_dict[file] = pd.read_csv(path_dict[file])
   for cols in json_dict[file]:
      print("about to ast.literal_eval ",cols)
      # df_keywords['keywords'] = df_keywords['keywords'].apply(lambda x: ast.literal_eval(x))
      df_dict[file][cols] = df_dict[file][cols].apply(lambda x: ast.literal_eval(x))
   if save_files:
      df_dict[file].to_pickle(str(file))




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
   """return the values of the last n rows"""
   def name(self) -> Text:
      return "action_rank_col_by_other_col"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      for slot_entry in slot_dict:
         dispatcher.utter_message(str(slot_entry))
         dispatcher.utter_message(str(slot_dict[slot_entry]))
      return []
   
class action_condition_by_year(Action):
   """return the values scoped by year"""
   def name(self) -> Text:
      return "action_condition_by_year"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #   dispatcher.utter_message(str(slot_entry))
      #   dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      year = tracker.get_slot("year")
      top_bottom = tracker.get_slot("top_bottom")
      if top_bottom == 'top':
         ascend_direction = False
      else:
         ascend_direction = True
      csv_row = int(tracker.get_slot('row_number'))
      sort_col = tracker.get_slot("sort_col")
      str1 = "COMMENT: getting "+ str(ranked_col) + " for year "+str(year)
      dispatcher.utter_message(str1)
      df=df_dict['movies']
      ranked_col = slot_map[ranked_col]
      result = (df[df['release_date'].str[:4] == year].sort_values(by = [sort_col],ascending=ascend_direction))[ranked_col]
      limiter = int(csv_row)
      i = 0
      str2 = "COMMENT: number of elements to show is "+str(limiter)
      dispatcher.utter_message(str2)
      for item in result:
         dispatcher.utter_message(str(item))
         i = i+1
         if i >= limiter:
            break
      dispatcher.utter_message("COMMENT: end of transmission")
      return []

class action_condition_by_movie(Action):
   """return the values scoped by movie"""
   def name(self) -> Text:
      return "action_condition_by_movie"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #  dispatcher.utter_message(str(slot_entry))
      #  dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      movie = tracker.get_slot("movie")
      top_bottom = tracker.get_slot("top_bottom")
      if top_bottom == 'top':
         ascend_direction = False
      else:
         ascend_direction = True
      csv_row = int(tracker.get_slot('row_number'))
      sort_col = tracker.get_slot("sort_col")
      str1 = "COMMENT: getting "+ str(ranked_col) + " for "+str(movie)
      dispatcher.utter_message(str1)
      df=df_dict['movies']
      ranked_col = slot_map[ranked_col]
      result = df[df['original_title'] == movie][ranked_col]
      dispatcher.utter_message(str(result))
      dispatcher.utter_message("COMMENT: end of transmission")
      return []

# syntax to determine if a value exists in a an array of dictionaries:
# keyword_list = [{'id': 1009, 'name': 'baby'}, {'id': 1599, 'name': 'midlife crisis'}, {'id': 2246, 'name': 'confidence'}, {'id': 4995, 'name': 'aging'}, {'id': 5600, 'name': 'daughter'}, {'id': 10707, 'name': 'mother daughter relationship'}, {'id': 13149, 'name': 'pregnancy'}, {'id': 33358, 'name': 'contraception'}, {'id': 170521, 'name': 'gynecologist'}]
#  y = any(d.get('name',None)=='midlife crisis' for d in keyword_list)
   

def check_keyword_dict(dispatcher,id,keyword_list, keyword):
   id_there = False
   # TODO: there should be a more pythonic way to do this (check if a value occurs anywhere in a list of dictionaries
   # that is more efficient that this loop 
   for dict in keyword_list:
      if keyword in dict.values():
         id_there = True
   if id_there:
      return(id)
   else:
      return[]
         
      
   
   '''if any(d.get('name',None)==keyword for d in keyword_list):
      return(id)
   else:
      return('None')'''
      


class action_condition_by_keyword(Action):
   """return the values scoped by keyword"""
   def name(self) -> Text:
      return "action_condition_by_keyword"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #   dispatcher.utter_message(str(slot_entry))
      #   dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      language = tracker.get_slot("language")
      keyword = tracker.get_slot("keyword")
      top_bottom = tracker.get_slot("top_bottom")
      if top_bottom == 'top':
         ascend_direction = False
      else:
         ascend_direction = True
      csv_row = int(tracker.get_slot('row_number'))
      sort_col = tracker.get_slot("sort_col")
      str1 = "COMMENT: getting "+ str(ranked_col) + " for keyword "+str(keyword)
      dispatcher.utter_message(str1)
      df_movies=df_dict['movies']
      df_keywords = df_dict['keywords']
      ranked_col = slot_map[ranked_col]
      # interpret string of list from CSV as a Python list - moved to loading section to avoid copy being redone
      # df_keywords['keywords'] = df_keywords['keywords'].apply(lambda x: ast.literal_eval(x))
      ## TODO this is gross - need a better way to get the list of ids
      output = list(filter(None,df_keywords.apply(lambda x: check_keyword_dict(dispatcher, x['id'],x['keywords'],keyword),axis=1)))
      #str3 = "here output " + str(len(output))
      #str3 = "here 0 "+str(output[0]) +" here 1 "+ str(output[1])
      #str5 = "len output "+ str(len(output))
      # result = (df[df['release_date'].str[:4] == year].sort_values(by = [sort_col],ascending=ascend_direction))[ranked_col]
      result = df_movies[ranked_col][df_movies['id'].isin(output)]
      limiter = int(csv_row)
      str4 = "result len " + str(len(result))
      #dispatcher.utter_message(str(str4))
      i = 0
      for item in result:
         dispatcher.utter_message(str(item))
         i = i+1
         if i >= limiter:
            break
      #dispatcher.utter_message(str(str3))
      dispatcher.utter_message("COMMENT: end of transmission")
      return []




class action_condition_by_language(Action):
   """return the values scoped by year"""
   def name(self) -> Text:
      return "action_condition_by_language"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #   dispatcher.utter_message(str(slot_entry))
      #   dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      language = tracker.get_slot("language")
      top_bottom = tracker.get_slot("top_bottom")
      if top_bottom == 'top':
         ascend_direction = False
      else:
         ascend_direction = True
      csv_row = int(tracker.get_slot('row_number'))
      sort_col = tracker.get_slot("sort_col")
      str1 = "COMMENT: "+ str(path_dict['movies'])
      dispatcher.utter_message(str1)
      df=df_dict['movies']
      ranked_col = slot_map[ranked_col]
      language = slot_map[language]
      result = df[df['original_language'] == language][ranked_col]
      dispatcher.utter_message(str(result))
      dispatcher.utter_message("COMMENT: end of transmission")
      return []

'''
class ActionRankColByOtherCol(Action):
   """return the list of values from one column ranked according to another column"""
   def name(self) -> Text:
      return "action_rank_col_by_other_col"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      for entry in slot_dict:
         # print "key: %s , value: %s" % (key, mydictionary[key])
         dispatcher.utter_message(str(entry))
         dispatcher.utter_message(str(slot_dict[entry])
      return []


   
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
      # condition_col - list
      # condition_value - list
      # condition_operator
      #
      # in SQL parlance
      # select ranked_col from table where condition_col[0] condition_operator condition_value[0] and condition_col[1] condition_operator condition_value[1]

      # ranked_col = tracker.get_slot('ranked_col')
      # ranking_col = tracker.get_slot('ranking_col') - this is redundant; condition_col covers this
      #ascending_descending = tracker.get_slot('ascending_descending')
      #top_bottom = tracker.get_slot('top_bottom')
      #row_range = int(tracker.get_slot('row_range'))
      #condition_col = tracker.get_slot('condition_col')
      #condition_value = tracker.get_slot('condition_value')
      #condition_operator = tracker.get_slot('condition_operator')
      # get and print all currently set values of the slots
      #
      # in Python parlance, assuming all cols are in dataframe df
      #
      # result = df[df.condition_col[0] condition_operator condition_value[0]].ranked_col
      # example: streetcarjan2014[streetcarjan2014.Location == "King and Shaw"].Route

      # movie db schema
      ''''''
''' 
                




   
