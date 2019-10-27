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
import json
import logging
import itertools
# TODO figure out that even after setting logging level to debug, debug logging doesn't appear in the output
# for now, just keep warning messages for basic logging
logging.basicConfig(level=logging.DEBUG)
logging.warning("logging check")

def json_check(string, placeholder):
   try:
      testarray = ast.literal_eval(string)
   except ValueError as e:
      return placeholder
   return string

# define paths for movie dataset files

path_dict = {}
path_dict['links'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/links_small.csv'
path_dict['movies'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/movies_metadata_small.csv'
path_dict['ratings'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/ratings_small.csv'
path_dict['credits'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/credits_small.csv'
path_dict['keywords'] = 'https://raw.githubusercontent.com/ryanmark1867/chatbot/master/datasets/keywords_small.csv'

# placeholders used to clean up files with missing JSON values so that they can have literal_eval processing done on them
crew_placeholder = str([{'credit_id': '52fe4ab0c3a368484e161d3d', 'department': 'Directing', 'gender': 0, 'id': 1080311, 'job': 'Director', 'name': 'Sandip Ray', 'profile_path': None}])
cast_placeholder = str([{'cast_id': 0, 'character': '', 'credit_id': '53be47fb0e0a26158f003788', 'gender': 2, 'id': 1894, 'name': 'Scott Caan', 'order': 1, 'profile_path': '/kvUKf9HCaqUtgj7XuKZOvN66MOT.jpg'}, {'cast_id': 1, 'character': '', 'credit_id': '53be48030e0a2615760039f8', 'gender': 0, 'id': 1339926, 'name': 'Lee Nashold', 'order': 2, 'profile_path': None}, {'cast_id': 2, 'character': '', 'credit_id': '53be480a0e0a26158f00378a', 'gender': 2, 'id': 24362, 'name': 'Kevin Michael Richardson', 'order': 3, 'profile_path': '/9dMOW2CFRrlDkNzeXVGMJfASupM.jpg'}, {'cast_id': 3, 'character': '', 'credit_id': '53be48110e0a2615820038b6', 'gender': 2, 'id': 3085, 'name': 'James Caan', 'order': 4, 'profile_path': '/g4bxNXWft1jLZX8gKk4G6ypkTUf.jpg'}, {'cast_id': 4, 'character': '', 'credit_id': '53be48180e0a26157c003802', 'gender': 0, 'id': 53646, 'name': 'Missy Crider', 'order': 5, 'profile_path': '/xkFq4Ye3yz6R5EaBBLb6bY5IDjs.jpg'}, {'cast_id': 5, 'character': '', 'credit_id': '53be481f0e0a2615820038b9', 'gender': 2, 'id': 827, 'name': 'Elliott Gould', 'order': 6, 'profile_path': '/bo5jSwWyFRsKVAkELT9n7AKQqMk.jpg'}, {'cast_id': 6, 'character': '', 'credit_id': '53be48260e0a26157c003804', 'gender': 2, 'id': 62032, 'name': 'Duane Davis', 'order': 7, 'profile_path': '/t9tcFEEbffaD64VZdsc0qwnPnr9.jpg'}])

# define columns in each file that are JSON formatted and need to be ast.literal_eval processed
json_dict = {}
json_dict['links'] = []
json_dict['movies'] = ['genres','production_companies','production_countries','spoken_languages',]
json_dict['ratings'] = []
json_dict['credits'] = ['cast','crew']
json_dict['keywords'] = ['keywords']


# map various strings to correct column names
# define synonyms (TODO see how to move at least a subset of these to Rasa level so they don't have to be maintained at Python layer)
slot_map = dict.fromkeys(['movies','movie name','movie','title','original_title'],'original_title')
slot_map.update(dict.fromkeys(['plot','plot summary','plot statement','overview'],'overview'))
slot_map.update(dict.fromkeys(['year','release date','release_date'],'release_date'))
slot_map.update(dict.fromkeys(['French'],'fr'))
slot_map.update(dict.fromkeys(['English'],'en'))
slot_map.update(dict.fromkeys(['German'],'de'))
slot_map.update(dict.fromkeys(['budget'],'budget'))
slot_map.update(dict.fromkeys(['revenue'],'revenue'))
slot_map.update(dict.fromkeys(['original_language'],'original_language'))
slot_map.update(dict.fromkeys(['funny','comedy','Comedy'],'Comedy'))
slot_map.update(dict.fromkeys(['cast','castmember','cast_name'], 'cast_name'))
slot_map.update(dict.fromkeys(['crew','crewmember','crew_name'], 'crew_name'))
slot_map.update(dict.fromkeys(['language','movies_language_name'], 'movies_language_name'))
slot_map.update(dict.fromkeys(['genre','genre_name'], 'genre_name'))
slot_map.update(dict.fromkeys(['keyword','keyword_name'], 'keyword_name'))
slot_map.update(dict.fromkeys(['ascending'], 'ascending'))


# define the subset of slots that can be condition columns:
# TODO confirm whether this list should contain exclusively slot names from rasa (e.g. no "original_title"
# TODO determine if possible to generate this list automatically instead of hand creating it
slot_condition_columns = ["original_language","original_title","movie","budget","overview","keyword_name","revenue","cast_name","crew_name","genre_name","year"]

def add_id_to_dict(dict_list,id_name,id):
   str2 = "dict_list is"+str(dict_list)
   str3 = "id_name "+str(id_name)+" id "+str(id)
   logging.debug(str2)
   logging.debug(str3)
   for dict in dict_list:
      dict[id_name] = id
   return dict_list


# preload dataframes with datasets
# switch to serialize dataframes
save_files = False
# switch to load from serialized dataframes
saved_files = True
df_dict = {}
for file in path_dict:
   print("about to create df for ",file)
   if saved_files:
      logging.warning("loading df from pickle file for : "+str(file))
      df_dict[file] = pd.read_pickle(str(file))
      # repair bad values in credits file
      
   else:
      df_dict[file] = pd.read_csv(path_dict[file])
      # manually cleaned up credits file - TODO make this real so input more resiliant
      #if file == 'credits':
      #   # for rows with empty lists for their JSON columns, replace with placeholders
      #   df_dict[file]['crew'] = df_dict[file].apply(lambda x: json_check(x['crew'], crew_placeholder),axis=1)
      #   df_dict[file]['cast'] = df_dict[file].apply(lambda x: json_check(x['cast'], cast_placeholder),axis=1)
      for cols in json_dict[file]:
         logging.warning("about to ast.literal_eval "+cols)
         # apply tranformation to render JSON strings from the CSV file into Python structures
         # need to do this or operations cannot be performed on the structures (e.g. check_keyword_dict)
         df_dict[file][cols] = df_dict[file][cols].apply(lambda x: ast.literal_eval(x))
         # add the id all the dictionaries in the JSON format columns
         logging.warning("about to add ids to dictionaries in "+cols+" for file "+file)
         # df.loc[[159220]]
         logging.warning(str(df_dict[file][cols].loc[[1]]))
         df_dict[file][cols] = df_dict[file].apply(lambda x: add_id_to_dict(x[cols],'movie_id',x['id']),axis=1)
         # create a new handle for the new dataframe
         new_handle = str(file)+"_"+str(cols)
         logging.warning("new handle is "+new_handle)
         nh_list = df_dict[file][cols].values
         # consolidate list of lists of dictionaries into a single list of dictionaries
         nh_list_single = list(itertools.chain.from_iterable(nh_list))
         df_dict[new_handle] = pd.DataFrame(nh_list_single)
         logging.warning("post new_handle col add: "+str(df_dict[new_handle].head()))
         # logging.warning("post new_handle col add: "+str(df_dict[new_handle].loc[[1]]))
# load up the generated dataframes that came from JSON
if saved_files:
   for file in path_dict:
      for cols in json_dict[file]:
         new_handle = str(file)+"_"+str(cols)
         logging.warning("loading df from pickle file for : "+new_handle)
         df_dict[new_handle] = pd.read_pickle(str(new_handle))
if save_files:
   # have to go through df_dict again in a separate loop since new df_dict entries added in the above loop
   for file in df_dict:
      df_dict[file].to_pickle(str(file))


# load the schema dictionary
#
def load_schema_dict(df_dict):
   schema_dict = {}
   for file in df_dict:
      schema_dict[file] = list(df_dict[file])
      logging.warning("schema_dict for "+file+" is "+str(schema_dict[file]))
   return(schema_dict)

'''
RESULT:
links is ['movieId', 'imdbId', 'tmdbId']
movies is ['adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count']
ratings is ['userId', 'movieId', 'rating', 'timestamp']
credits is ['cast', 'crew', 'id']
keywords is ['id', 'keywords']
movies_genres is ['id', 'name', 'movie_id']
movies_production_companies is ['name', 'id', 'movie_id']
movies_production_countries is ['iso_3166_1', 'name', 'movie_id']
movies_spoken_languages is ['iso_639_1', 'name', 'movie_id']
credits_cast is ['cast_id', 'character', 'credit_id', 'gender', 'id', 'name', 'order', 'profile_path', 'movie_id']
credits_crew is ['credit_id', 'department', 'gender', 'id', 'job', 'name', 'profile_path', 'movie_id']
keywords_keywords is ['id', 'name', 'movie_id']
'''

# rename some columns to avoid duplicates
# df.rename({'a': 'X', 'b': 'Y'}, axis=1, inplace=True)
df_dict['movies_genres'].rename({'name':'genre_name'},axis=1,inplace=True)
df_dict['movies_production_companies'].rename({'name':'movies_production_company_name'},axis=1,inplace=True)
df_dict['movies_production_countries'].rename({'name':'movies_production_country_name'},axis=1,inplace=True)
df_dict['movies_spoken_languages'].rename({'name':'movies_language_name'},axis=1,inplace=True)
df_dict['credits_cast'].rename({'name':'cast_name'},axis=1,inplace=True)
df_dict['credits_crew'].rename({'name':'crew_name'},axis=1,inplace=True)
df_dict['keywords_keywords'].rename({'name':'keyword_name'},axis=1,inplace=True)

parent_key = 'id'
child_key = 'movie_id'

# main prep code block
movie_schema = load_schema_dict(df_dict)
      
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
      genre = tracker.get_slot("genre")
      if top_bottom == 'top':
         ascend_direction = False
      else:
         ascend_direction = True
      csv_row = int(tracker.get_slot('row_number'))
      sort_col = tracker.get_slot("sort_col")
      if genre == None:
         dispatcher.utter_message("genre is None")
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

class action_condition_by_movie_old(Action):
   """return the values scoped by movie"""
   def name(self) -> Text:
      return "action_condition_by_movie_old"
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

        
# version used for condition_by_cast
def check_keyword_dict(dispatcher,id,keyword_list, keywords,dict_key):
   # for id list id and keyword_list in JSON form, return the id value if
   # keyword is there
   id_there = False
   logging.debug("about to start check_keyword_dict")
   # make dictionary of keywords with values initialized to zero
   k_list = {e1:0 for e1 in keywords}
   str9 = "types id "+str(type(id))+" keyword_list "+str(type(keyword_list))+" keywords "+str(type(keywords))
   logging.debug(str9)
   for word in keywords:
      str0 = "input to check_keyword_dict keyword  "+word
      logging.debug(str0)
   # TODO: there should be a more pythonic way to do this (check if a value occurs anywhere in a list of dictionaries
   # that is more efficient that this loop
   allthere = 0
   str6 = "json.dump keyword_list is"+json.dumps(keyword_list)
   logging.debug(str6)
   for dict in keyword_list:
      str5 = "dict[dict_key] is "+str(dict[dict_key])
      logging.debug(str5)
      #logging.debug(str(dict))
      for word in keywords:
         if word in dict[dict_key]:
            str1 = "got a hit for word "+word
            logging.debug(str1)
            k_list[word] = 1
   # check if all elements of keyword appear in one of the dictionaries            
   logging.debug("about to leave check_keyword_dict")
   if all(value == 1 for value in k_list.values()):
      logging.warning("all values 1")
      return(id)
   else:
      logging.debug("not all values 1")
      return[]


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
      csv_row = int(tracker.get_slot('row_number'))
      genre = tracker.get_slot("genre")
      sort_col = tracker.get_slot("sort_col")
      str1 = "COMMENT: getting "+ str(ranked_col) + " for keyword "+str(keyword)
      dispatcher.utter_message(str1)
      df_movies=df_dict['movies']
      df_keywords = df_dict['keywords']
      ranked_col = slot_map[ranked_col]
      # interpret string of list from CSV as a Python list - moved to loading section to avoid copy being redone
      # df_keywords['keywords'] = df_keywords['keywords'].apply(lambda x: ast.literal_eval(x))
      ## TODO this is gross - need a better way to get the list of ids
      output = list(filter(None,df_keywords.apply(lambda x: check_keyword_dict(dispatcher, x['id'],x['keywords'],keyword,'name'),axis=1)))
      result_big = df_movies.loc[df_movies['id'].isin(output)]
      result = df_movies[ranked_col][df_movies['id'].isin(output)]
      limiter = int(csv_row)
      str4 = "result len " + str(len(result))
      i = 0
      for item in result:
         dispatcher.utter_message(str(item))
         i = i+1
         if i >= limiter:
            break
      dispatcher.utter_message("COMMENT: genre sublist")
      if genre != None:
         genre = slot_map[genre]
         str5 = "genre is "+genre
         dispatcher.utter_message(str(str5))
         genre_output = list(filter(None,result_big.apply(lambda x: check_keyword_dict(dispatcher, x[ranked_col],x['genres'],genre,'name'),axis=1)))
         for item in genre_output:
            dispatcher.utter_message(str(item))
            i = i+1
            if i >= limiter:
               break
      dispatcher.utter_message("COMMENT: end of transmission")
      return []

# old condition by cast where JSON columns processed natively

class action_condition_by_cast_old(Action):
   """return the values scoped by cast"""
   def name(self) -> Text:
      return "action_condition_by_cast_old"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #   dispatcher.utter_message(str(slot_entry))
      #   dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      language = tracker.get_slot("language")
      keyword = tracker.get_slot("keyword")
      castmembers = tracker.get_slot("castmember")
      top_bottom = tracker.get_slot("top_bottom")
      csv_row = int(tracker.get_slot('row_number'))
      genre = tracker.get_slot("genre")
      sort_col = tracker.get_slot("sort_col")
      cast_str = ", ".join(str(x) for x in castmembers)
      str1 = "COMMENT: getting "+ str(ranked_col) + " for cast "+cast_str
      dispatcher.utter_message(str1)
      
      
      df_movies=df_dict['movies']
      df_keywords = df_dict['keywords']
      df_credits = df_dict['credits']
      ranked_col = slot_map[ranked_col]
      # interpret string of list from CSV as a Python list - moved to loading section to avoid copy being redone
      # df_keywords['keywords'] = df_keywords['keywords'].apply(lambda x: ast.literal_eval(x))
      ## TODO this is gross - need a better way to get the list of ids
      output = list(filter(None,df_credits.apply(lambda x: check_keyword_dict(dispatcher, x['id'],x['cast'],castmembers,'name'),axis=1)))
      str3 = "here len output " + str(len(output))
      #str3 = "here 0 "+str(output[0]) +" here 1 "+ str(output[1])
      logging.warning(str(str3))
      
      result_big = df_movies.loc[df_movies['id'].isin(output)]
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
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission")
      return []

# TODO: instead of the complex multifaceted structure of various dictionaries and lists, encapsulate in a class
# to make the updates simpler and to avoid losing track of what's a list vs. dictionary


def execute_query (condition_col, condition_table, condition_value, condition_operator,top_bottom,ascending_descending,ranked_col, returned_values):
   """ perform query on specified table """
   return_values = condition_table[condition_table[condition_col] == condition_value][ranked_col]
   return(return_values)

def get_table(column_list,schema):
   """ return the table that contains the given column in the given schema dictionary"""
   table_list = []
   for table in schema:
      logging.warning("get_table table is: "+str(table))
      for column in column_list:
         logging.warning("get_table column is: "+str(column))
         if column in schema[table]:
            logging.warning("get_table got table "+str(table)+" for column: "+str(column))
            table_list.append(table)
   return(table_list)

def get_condition_columns(slot_dict):
   condition_dict = {}
   for slot in slot_dict:
      logging.warning("in gcc slot is "+str(slot))
      logging.warning("in gcc slot_dict[slot] "+str(slot_dict[slot]))
      # check  if slot is a candidate for condition column and that it's not empty
      if not(slot_dict[slot] is None) and (slot in slot_condition_columns):
         logging.warning("get_condition_columns found "+str(slot))
         condition_dict[slot]= slot_dict[slot]
         #condition_col.append(slot)
   return(condition_dict)

def same_table(condition_table, ranked_table):
   ''' return true if both lists have exactly one element which is the same. Otherwise return false '''
   if len(condition_table) == 1 and len(ranked_table) == 1:
      return(condition_table[0] == ranked_table[0])
   else:
      return(False)
    
# new condition by cast where JSON columns processed in separate dataframes rather than natively
# TO DO: SWITCH TO condition_by_movie to test an "all the same table" query

class action_condition_by_movie(Action):
   """return the values scoped by cast"""
   def name(self) -> Text:
      return "action_condition_by_movie"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # get dictionary of slot values
      slot_dict = tracker.current_slot_values()
      for table in movie_schema:
         logging.warning("table is: "+str(table))
      for slot_entry in slot_dict:
         logging.warning("in slot_entry loop slot_entry is: "+str(slot_entry))
         logging.warning("in slot_entry loop slot_dict[slot_entry] is: "+str(slot_dict[slot_entry]))
         if slot_entry in slot_condition_columns:
            logging.warning("in slot_condition_columns for slot_entry: "+str(slot_entry))
            # syntax to replace key value
            # dictionary[new_key] = dictionary.pop(old_key)
            slot_dict[slot_map[slot_entry]] = slot_dict.pop(slot_entry)
            logging.warning("in slot_condition_columns new key set for "+str(slot_map[slot_entry]))
         logging.warning("after "+str(slot_entry))
      # need to examine slot_dict for "None"s to determine condition_col
      slot_dict["ranked_col"] = slot_map[slot_dict["ranked_col"]]
      condition_dict = {}
      condition_dict = get_condition_columns(slot_dict)
      # get_table expects a list of columns as its first arg, so just take keys from condition_dict dictionary
      condition_table = get_table(list(condition_dict.keys()),movie_schema)
      ranked_table = get_table([slot_dict["ranked_col"]],movie_schema)
      
      logging.warning("condition_dict is "+str(condition_dict))
      logging.warning("condition_table is "+str(condition_table))
      logging.warning("ranked_cod is "+str(slot_dict["ranked_col"]))
      logging.warning("ranked_table is "+str(ranked_table))
      '''
      EXAMPLE OF CONDITION LIST
      - condition_dict is {'cast_name': ['Sean Connery']}
      - condition_table is ['credits_cast']
      - ranked_cod is original_title
      - ranked_table is ['movies']

      EXAMPLE OF CONDITION NOT A LIST
      condition_dict is {'original_title': 'Toy Story'}
      condition_table is ['movies']
      ranked_cod is budget
      ranked_table is ['movies']
      '''
      # TODO lowercase strings for comparison
      result = {}
      if same_table(condition_table, ranked_table):
         logging.warning("same table "+str(condition_table))
         base_df = df_dict[ranked_table[0]]
         # iterate through conditions keeping all columns
         for condition in condition_dict:
            logging.warning("in single table condition loop for condition "+str(condition))
            base_df = base_df[base_df[condition] == condition_dict[condition]]
         result = base_df[slot_dict["ranked_col"]]
      else:
         logging.warning("different condition_table"+str(condition_table)+" ranked_table "+str(ranked_table))
         '''
         # condition and rank in different tables
         first_condition = True
         for condition in condition_dict:
            # check if condition value is a list
            if isinstance(condition_dict[condition], list)
               # TODO complete logic for dealing with conditions that are lists
            else:
               # condition is not a list
               child_key_df = df_dict[condition_table[0]][df_dict[condition_table[0]][condition] == value][child_key]
               if first_condition:
                  first_condition = False
                  child_key_df = df_dict[condition_table[0]][df_dict[condition_table[0]][condition] == value][child_key]
               result_list = {}
               for value in condition_dict[condition]:
                  logging.warning("value in condition_dict value"+str(value)+" and condition_dict[value] "+str(condition_dict[value]))
                  result_list[value] = df_dict[condition_table[0]][df_dict[condition_table[0]][condition] == condition_dict[value]][child_key]
                  result_list[value] =
          '''        
      # ranked_col = slot_dict["ranked_col"]
      #if same_table(condition_table, ranked_table)
      #output = df_dict[condition_table[0]][df_dict[condition_table[0]][condition_col[0] == slot_dict["

      '''
      df_movies=df_dict['movies']
      ranked_df = df_dict[ranked_col]
      df_keywords = df_dict['keywords']
      df_cast = df_dict['credits_cast']
      df_credits = df_dict['credits']
      ranked_col = slot_map[ranked_col]
      # simple query to get movie ids 
      movie_ids = df_cast[df_cast['name'] == castmembers[0]]['movie_id']
      result2 = pd.merge(movie_ids,df_movies,left_on='movie_id',right_on='id')
      '''
      for result_item in result:
         logging.warning("in output loop ")
         logging.warning("result for re "+str(slot_dict["ranked_col"])+" is "+str(result_item))
         dispatcher.utter_message("result for condition "+str(slot_dict["ranked_col"])+" is "+str(result_item))
      '''                   
      for result_set in result:
         for item in result_set[slot_dict["ranked_col"]]:
            dispatcher.utter_message(item)
      '''
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission validated")
      return []

class action_condition_by_cast_nold(Action):
   """return the values scoped by cast"""
   def name(self) -> Text:
      return "action_condition_by_cast_nold"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      slot_dict = tracker.current_slot_values()
      #for slot_entry in slot_dict:
      #   dispatcher.utter_message(str(slot_entry))
      #   dispatcher.utter_message(str(slot_dict[slot_entry]))
      ranked_col = tracker.get_slot("ranked_col")
      language = tracker.get_slot("language")
      keyword = tracker.get_slot("keyword")
      castmembers = tracker.get_slot("castmember")
      top_bottom = tracker.get_slot("top_bottom")
      csv_row = int(tracker.get_slot('row_number'))
      genre = tracker.get_slot("genre")
      sort_col = tracker.get_slot("sort_col")
      cast_str = ", ".join(str(x) for x in castmembers)
      str1 = "COMMENT: getting "+ str(ranked_col) + " for cast "+cast_str
      dispatcher.utter_message(str1)
      
      
      df_movies=df_dict['movies']
      ranked_df = df_dict[ranked_col]
      df_keywords = df_dict['keywords']
      df_cast = df_dict['credits_cast']
      df_credits = df_dict['credits']
      ranked_col = slot_map[ranked_col]
      # simple query to get movie ids 
      movie_ids = df_cast[df_cast['name'] == castmembers[0]]['movie_id']
      result2 = pd.merge(movie_ids,df_movies,left_on='movie_id',right_on='id')
      for item in result2['original_title']:
         dispatcher.utter_message(item)
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission validated")
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

 
                




   
