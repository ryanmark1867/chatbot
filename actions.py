# Custom actions for filebot project

# property of KarmaAI

# common imports

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import ast
import json
import logging
import itertools
import numbers
import decimal
import collections
from collections import Counter

# TODO figure out that even after setting logging level to debug, debug logging doesn't appear in the output
# for now, just keep warning messages for basic logging
logging.basicConfig(level=logging.DEBUG)
logging.warning("logging check")

class Condition:
   def __init__(self,value_list,d_table):
      self.value = value_list
      self.table = d_table
   
   

def json_check(string, placeholder): 
   ''' input string and placeholder JSON. If string parses as valid Python, return result of literal_eval.
   Otherwise, return placeholder string'''
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
image_path = 'https://image.tmdb.org/t/p/w500'

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
slot_map.update(dict.fromkeys(['release date','release_date'],'release_date'))
slot_map.update(dict.fromkeys(['year'],'year'))
slot_map.update(dict.fromkeys(['French'],'fr'))
slot_map.update(dict.fromkeys(['English'],'en'))
slot_map.update(dict.fromkeys(['German'],'de'))
slot_map.update(dict.fromkeys(['budget'],'budget'))
slot_map.update(dict.fromkeys(['revenue'],'revenue'))
slot_map.update(dict.fromkeys(['director','Director'],'Director'))
slot_map.update(dict.fromkeys(['original_language'],'original_language'))
slot_map.update(dict.fromkeys(['funny','comedy','Comedy'],'Comedy'))
# slot_map.update(dict.fromkeys(['popularity','rating'],'rating'))
slot_map.update(dict.fromkeys(['cast','castmember','cast_name'], 'cast_name'))
slot_map.update(dict.fromkeys(['crew','crewmember','crew_name'], 'crew_name'))
slot_map.update(dict.fromkeys(['characters','character','character_name'], 'character'))
slot_map.update(dict.fromkeys(['language','movies_language_name'], 'movies_language_name'))
slot_map.update(dict.fromkeys(['genre','genre_name'], 'genre_name'))
slot_map.update(dict.fromkeys(['keyword','keyword_name'], 'keyword_name'))
slot_map.update(dict.fromkeys(['ascending'], 'ascending'))


# define the subset of slots that can be condition columns:
# TODO confirm whether this list should contain exclusively slot names from rasa (e.g. no "original_title")
# TODO determine if possible to generate this list automatically instead of hand creating it
slot_condition_columns = ["original_language","original_title","movie","director","Director","genre","budget","overview","keyword","keyword_name","revenue","cast_name","crew_name","genre_name","year"]

def add_id_to_dict(dict_list,id_name,id):
   ''' for list of dictionaries dict_list, add the entry "id_name":id to each dictionary in the list'''
   str2 = "dict_list is"+str(dict_list)
   str3 = "id_name "+str(id_name)+" id "+str(id)
   logging.debug(str2)
   logging.debug(str3)
   for dict in dict_list:
      dict[id_name] = id
   return dict_list


# load df_dict dictionary with dataframes corresponding to the datasets
# if saved_files, load from pickled dataframes created previously by this code block
# if save_files, save the 
# switch to serialize dataframes
save_files = False
# switch to load from serialized dataframes
saved_files = True
df_dict = {}
for file in path_dict:
   print("about to create df for ",file)
   if saved_files:
      # load pickled file corresponding to dataframes for the dataset files
      # pickled files for derived dataframes loaded below
      logging.warning("loading df from pickle file for : "+str(file))
      df_dict[file] = pd.read_pickle(str(file))
   else:
      df_dict[file] = pd.read_csv(path_dict[file])
      # manually cleaned up credits file - TODO make this real so input more resiliant
      for cols in json_dict[file]:
         logging.warning("about to ast.literal_eval "+cols)
         # apply tranformation to render JSON strings from the CSV file into Python structures
         # need to do this or operations cannot be performed on the structures (e.g. check_keyword_dict)
         df_dict[file][cols] = df_dict[file][cols].apply(lambda x: ast.literal_eval(x))
         # add the id all the dictionaries in the JSON format columns
         logging.warning("about to add ids to dictionaries in "+cols+" for file "+file)
         logging.warning(str(df_dict[file][cols].loc[[1]]))
         df_dict[file][cols] = df_dict[file].apply(lambda x: add_id_to_dict(x[cols],'movie_id',x['id']),axis=1)
         # create a new handle for the new dataframe
         new_handle = str(file)+"_"+str(cols)
         logging.warning("new handle is "+new_handle)
         nh_list = df_dict[file][cols].values
         # consolidate list of lists of dictionaries into a single list of dictionaries
         nh_list_single = list(itertools.chain.from_iterable(nh_list))
         # define new dataframe with distinct columns for each range in the original df's JSON column
         # and add new dataframe to df_dict
         df_dict[new_handle] = pd.DataFrame(nh_list_single)
         logging.warning("post new_handle col add: "+str(df_dict[new_handle].head()))
        
# load up the generated dataframes that came from JSON
if saved_files:
   for file in path_dict:
      for cols in json_dict[file]:
         # load pickled files corresponding to dataframes generated from JSON columns in original dataset
         new_handle = str(file)+"_"+str(cols)
         logging.warning("loading df from pickle file for : "+new_handle)
         df_dict[new_handle] = pd.read_pickle(str(new_handle))
if save_files:
   # have to go through df_dict again in a separate loop since new df_dict entries added in the above loop
   # save all the dataframes in the df_dict dictionary in separate pickle files
   for file in df_dict:
      df_dict[file].to_pickle(str(file))


# load the schema dictionary with "table":[colum1,column2...] 
#
def load_schema_dict(df_dict):
   schema_dict = {}
   for file in df_dict:
      schema_dict[file] = list(df_dict[file])
      #logging.warning("schema_dict for "+file+" is "+str(schema_dict[file]))
      #logging.warning("size of df for "+file+" is "+str(len(df_dict[file].index)))
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
df_dict['movies_genres'].rename({'name':'genre_name'},axis=1,inplace=True)
df_dict['movies_production_companies'].rename({'name':'movies_production_company_name'},axis=1,inplace=True)
df_dict['movies_production_countries'].rename({'name':'movies_production_country_name'},axis=1,inplace=True)
df_dict['movies_spoken_languages'].rename({'name':'movies_language_name'},axis=1,inplace=True)
df_dict['credits_cast'].rename({'name':'cast_name'},axis=1,inplace=True)
df_dict['credits_crew'].rename({'name':'crew_name'},axis=1,inplace=True)
df_dict['keywords_keywords'].rename({'name':'keyword_name'},axis=1,inplace=True)
# generate separate 'year' column from 'release_date'
df_dict['movies']['year'] = df_dict['movies']['release_date'].str[:4]

# define distinct dataframes for each profession in the credits_crew df
def create_crew_by_job_dfs(credits_df,df_dict):
   ''' create distinct tables for each job in credits_crew '''
   # df.name.unique()
   job_list = credits_df.job.unique()
   for job_name in job_list:
      # for each unique job, create
      job_name_uscore = job_name.replace(" ","_")
      new_handle = "credits_crew_"+job_name_uscore
      #logging.warning("job new handle "+str(new_handle))
      df_dict[new_handle] = credits_df[credits_df['job'] == job_name]
      df_dict[new_handle].rename({'crew_name':job_name_uscore},axis=1,inplace=True)
          
   return(df_dict)


# define the keys used to join parent table (movies) with children tables(keyword_keywords,credits_crew
# credits_cast, movies_spoken_languages, movies_production_companies, movies_production_countries, movies_genres
parent_key = 'id'
child_key = 'movie_id'
parent_table = 'movies'
child_tables = ['links','ratings','keywords','movies_genres','movies_production_companies','movies_production_countries','movies_spoken_languages','credits_cast','credits_crew','keywords_keywords']

# main prep code block
df_dict = create_crew_by_job_dfs(df_dict['credits_crew'],df_dict)
movie_schema = load_schema_dict(df_dict)

def get_image_path(image_file):
   # TODO replace with code that gets the actual base path
   return(image_path+image_file)



# classes for individual custom actions triggered by Rasa
      
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

# TODO: instead of the complex multifaceted structure of various dictionaries and lists, encapsulate in a class
# to make the updates simpler and to avoid losing track of what's a list vs. dictionary

# helper function for refactored main class action_condition_by_movie

def execute_query (condition_col, condition_table, condition_value, condition_operator,top_bottom,ascending_descending,ranked_col, returned_values):
   """ perform query on specified table """
   return_values = condition_table[condition_table[condition_col] == condition_value][ranked_col]
   return(return_values)

def get_table(column_list,schema):
   """ return the table that contains the given column in the given schema dictionary"""
   table_dict = {}
   for table in schema:
      #logging.warning("get_table table is: "+str(table))
      for column in column_list:
         #logging.warning("get_table column is: "+str(column))
         if column in schema[table]:
            #logging.warning("get_table got table "+str(table)+" for column: "+str(column))
            table_dict[column] = table
   return(table_dict)

def get_condition_columns(slot_dict):
   ''' given a slot dictionary, return dictionary of condition columns whose slots are filled in '''
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
   ''' return true if both lists have exactly one element, and this element which is the same. Otherwise return false '''
   # check a single unique value in each list
   if ((len((Counter(condition_table).keys())) == 1) and (len((Counter(ranked_table).keys())) == 1)):
      # check to see if unique values identical
      return(collections.Counter(set(condition_table))== collections.Counter(set(ranked_table)))
   else:
      return(False)
   

def prep_slot_dict(slot_dict):
   ''' iterate through slot dictionary mapping slot keys and values from Rasa settings to what's required for schema '''
   for table in movie_schema: 
         logging.warning("table is: "+str(table))
   for slot_entry in slot_dict:
      logging.warning("in slot_entry loop slot_entry is: "+str(slot_entry))
      logging.warning("in slot_entry loop slot_dict[slot_entry] is: "+str(slot_dict[slot_entry]))
      if slot_entry in slot_condition_columns:
         logging.warning("in slot_condition_columns for slot_entry: "+str(slot_entry))
         # syntax to replace key value
         slot_dict[slot_map[slot_entry]] = slot_dict.pop(slot_entry)
         logging.warning("in slot_condition_columns new key set for "+str(slot_map[slot_entry]))
      logging.warning("after "+str(slot_entry))
   length = len(slot_dict["ranked_col"])
   i = 0
   while i < length:
      # iterate through entries in ranked_col list
      logging.warning("in slot_entry loop ranked_col slot_entry is: "+str(i))
      slot_dict["ranked_col"][i] = slot_map[slot_dict["ranked_col"][i]]
      logging.warning("in slot_entry loop ranked_col slot_entry is: "+str(slot_dict["ranked_col"][i]))
      i = i+1
   return(slot_dict)

def get_results_same_table(result,condition_dict,condition_table,slot_dict):
   logging.warning("same_table condition_table "+str(condition_table))
   first_same = True
   # iterate through conditions keeping all columns
   for condition in condition_dict:
      logging.warning("in single table condition loop for condition "+str(condition))
      if first_same:
         # first time through loop set base_df
         base_df = df_dict[condition_table[condition]]
         first_same = False
      base_df = base_df[base_df[condition] == condition_dict[condition]]
   result = base_df[slot_dict["ranked_col"]]
   return(result)

def get_result_diff_table(result,condition_dict,condition_table,slot_dict):
   logging.warning("different condition_table"+str(condition_table)+" ranked_table "+str(ranked_table))
   # TODO: eventually want to consider a class to replace all the various dictionaries
   # but for now, just make the condition and ranked table containers dictionaries indexed by slot/column
   # rather than lists
   # condition and rank in different tables
   first_different = True
   child_key_df_dict = {}
   for condition in condition_table:
      # check if condition value is a list
      if isinstance(condition_dict[condition], list):
         #child_key_df_dict[condition] = build_condition_list_df(condition_dict[condition],condition
         # TODO complete logic for dealing with conditions that are lists
         logging.warning("condition_dict is a list "+str(condition))
         sub_condition_df_dict = {}
         # iterate through each element in the condition value list getting a df of matching child keys
         for sub_condition in condition_dict[condition]:
            logging.warning("sub_condition is "+str(sub_condition))
            sub_condition_df_dict[sub_condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition].str.contains(sub_condition)][child_key]
            logging.warning("sub_condition_df_dict[sub_condition] len is "+str(len(sub_condition_df_dict[sub_condition])))
            logging.warning("sub_condition_df_dict[sub_condition] is "+str(sub_condition_df_dict[sub_condition]))
         logging.warning("sub_condition_df_dict len is "+str(len(sub_condition_df_dict)))
         # merge the child key dfs to get a single df containing the intersection of child keys
         first_sub_condition = True
         for sub_condition in sub_condition_df_dict:
            logging.warning("sub_condition in merge loop is "+str(sub_condition))
            if first_sub_condition:
               first_sub_condition = False
               child_key_df_dict[condition] = sub_condition_df_dict[sub_condition]
            else:
               child_key_df_dict[condition] = pd.merge(child_key_df_dict[condition],sub_condition_df_dict[sub_condition],on=child_key,how='inner')
            logging.warning("sub_condition child_key_df_dict[condition] len is "+str(len(child_key_df_dict[condition])))
         logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
      else:
         # condition is not a list
         logging.warning("in multi table condition loop for not list condition "+str(condition))
         # build df that just contains child_keys for this
         child_key_df_dict[condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition] == condition_dict[condition]][child_key]
         logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
   for condition in condition_table:
      # iteratively merge child key tables
      if first_different:
         logging.warning("got first different "+str(condition))
         logging.warning("number of rows in child_key_df second loop "+str(len(child_key_df_dict[condition].index)))               
         result_child_merge = child_key_df_dict[condition]
         first_different = False
      else:
         result_child_merge = pd.merge(result_child_merge,child_key_df_dict[condition],on=child_key,how='inner')
   # now merge with parent table
   logging.warning("number of rows in child_key_df "+str(len(result_child_merge.index)))
   logging.warning("type of result_child_merge is "+str(type(type(result_child_merge))))
   for item_c in result_child_merge:
      logging.warning("item is "+str(item_c))
   first_final = True
   for condition in ranked_table:
         # TODO need to find a way to get the ranked table if there are multiple ranked columns
         logging.warning("in final ranked table loop for condition "+str(condition))
         result[condition] = pd.merge(df_dict[ranked_table[condition]],result_child_merge,left_on=parent_key,right_on=child_key,how='inner')[condition]
   
   return(result)
    
# refactored condition_by_cast using calls to power functions
class action_condition_by_cast(Action):
   """return the values scoped by cast"""
   def name(self) -> Text:
      return "action_condition_by_cast"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # get dictionary of slot values
      slot_dict = tracker.current_slot_values()
      # make required mappings of slot names and slot values
      slot_dict = prep_slot_dict(slot_dict)
      condition_dict = {}
      condition_dict = get_condition_columns(slot_dict)
      # get_table expects a list of columns as its first arg, so just take keys from condition_dict dictionary
      condition_table = get_table(list(condition_dict.keys()),movie_schema)
      # TODO change ranked_col slot to a list in rasa, to match condition
      ranked_table = get_table(slot_dict["ranked_col"],movie_schema)      
      logging.warning("condition_dict is "+str(condition_dict))
      logging.warning("condition_table is "+str(condition_table))
      logging.warning("ranked_cod is "+str(slot_dict["ranked_col"]))
      logging.warning("ranked_table is "+str(ranked_table))
      result = {}
      if same_table(list(condition_table.values()),list(ranked_table.values())):
         result = get_results_same_table(result,condition_dict,condition_table,slot_dict)
      else:
         result = get_result_diff_table(result,condition_dict,condition_table,slot_dict)
      # output results
      logging.warning("number of rows in result "+str(len(result))) 
      for result_item in result:
         logging.warning("number of rows in result][result_item "+str(len(result[result_item].index)))       
         logging.warning("in output loop ")
         for nested_item in result[result_item]:
            logging.warning(str(nested_item))
            dispatcher.utter_message(str(nested_item))
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission validated")
      return []

def get_selection_column_list(condition_table_list,ranked_table_list):
   ''' get list of columns to pull in final result'''
   return()

def get_condition_columns_to_pull(child_key, ranked_table, condition_table):
   ''' return the ranked columns that are in the condition_table
   child_key: column that is always pulled from condition_table for use to join with main table
   ranked_table: dictionary of form  {'original_title': 'movies', 'character': 'credits_cast'}
   condition_table: name of the table that corresponds with the condition that is being applied: e.g. 'movies', 'credits_cast' '''
   # list(mydict.keys())[list(mydict.values()).index(16)]
   column_list = [child_key]
   if condition_table in ranked_table.values():
      # reverse lookup the key in ranked_table that corresponds with the value condition_table and append to column_list
      column_list.append(list(ranked_table.keys())[list(ranked_table.values()).index(condition_table)])
   return(column_list)
   
def generate_result(slot_dict,condition_dict,condition_table,ranked_table):
   result = {}
   if same_table(list(condition_table.values()),list(ranked_table.values())):
      logging.warning("same_table condition_table "+str(condition_table))
      first_same = True
      # iterate through conditions keeping all columns
      for condition in condition_dict:
         logging.warning("in single table condition loop for condition "+str(condition))
         logging.warning("in single table condition loop for condition_table[condition] "+str(condition_table[condition]))
         if first_same:
            # first time through loop set base_df
            base_df = df_dict[condition_table[condition]]
            first_same = False
         logging.warning("in single table condition loop for condition_dict[condition] "+str(condition_dict[condition]))
         # TODO: need to handle list of conditions properly - currently OR for a list
         if isinstance(condition_dict[condition], list):
            base_df = base_df[base_df[condition].isin(condition_dict[condition])]
         else:
            base_df = base_df[base_df[condition] == str(condition_dict[condition])]
      logging.warning("RESULT IS "+str(base_df[slot_dict["ranked_col"]]))
      result = base_df[slot_dict["ranked_col"]]
   else:
      logging.warning("different condition_table"+str(condition_table)+" ranked_table "+str(ranked_table))
      # TODO: eventually want to consider a class to replace all the various dictionaries
      # but for now, just make the condition and ranked table containers dictionaries indexed by slot/column
      # rather than lists
      # condition and rank in different tables
      first_different = True
      child_key_df_dict = {}
      for condition in condition_table:
         # check if condition value is a list
         # for this condition, build the list of columns to pull from the child table
         condition_columns_to_pull = get_condition_columns_to_pull(child_key, ranked_table, condition_table[condition])
         if isinstance(condition_dict[condition], list):
            # TODO complete logic for dealing with conditions that are lists
            logging.warning("condition_dict is a list "+str(condition))
            sub_condition_df_dict = {}
            # iterate through each element in the condition value list getting a df of matching child keys
            for sub_condition in condition_dict[condition]:
               logging.warning("sub_condition is "+str(sub_condition))
               sub_condition_df_dict[sub_condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition].str.contains(sub_condition)][condition_columns_to_pull]
               logging.warning("sub_condition_df_dict[sub_condition] len is "+str(len(sub_condition_df_dict[sub_condition])))
               logging.warning("sub_condition_df_dict[sub_condition] is "+str(sub_condition_df_dict[sub_condition]))
            logging.warning("sub_condition_df_dict len is "+str(len(sub_condition_df_dict)))
            # merge the child key dfs to get a single df containing the intersection of child keys
            first_sub_condition = True
            for sub_condition in sub_condition_df_dict:
               logging.warning("sub_condition in merge loop is "+str(sub_condition))
               if first_sub_condition:
                  first_sub_condition = False
                  child_key_df_dict[condition] = sub_condition_df_dict[sub_condition]
               else:
                  child_key_df_dict[condition] = pd.merge(child_key_df_dict[condition],sub_condition_df_dict[sub_condition],on=child_key,how='inner')
            logging.warning("sub_condition child_key_df_dict[condition] len is "+str(len(child_key_df_dict[condition])))
            logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
         else:
            # condition is not a list
            logging.warning("in multi table condition loop for not list condition "+str(condition))
            # build df that just contains child_keys for this
            child_key_df_dict[condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition] == condition_dict[condition]][condition_columns_to_pull]
            logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
      for condition in condition_table:
         # iteratively merge child key tables
         if first_different:
            logging.warning("got first different "+str(condition))
            logging.warning("number of rows in child_key_df second loop "+str(len(child_key_df_dict[condition].index)))               
            result_child_merge = child_key_df_dict[condition]
            first_different = False
         else:
            result_child_merge = pd.merge(result_child_merge,child_key_df_dict[condition],on=child_key,how='inner')
      # now merge with parent table
      logging.warning("number of rows in child_key_df "+str(len(result_child_merge.index)))
      logging.warning("type of result_child_merge is "+str(type(type(result_child_merge))))
      for item_c in result_child_merge:
         logging.warning("item is "+str(item_c))
      first_final = True
      #
      logging.warning("slot_dict[ranked_col] is "+str(slot_dict["ranked_col"]))
      logging.warning("parent_key is "+str(parent_key))
      result_col_list = slot_dict["ranked_col"]
      result_col_list.append(parent_key)
      result_col_list.append(slot_dict["rank_axis"])
      logging.warning("result_col_list is "+str(result_col_list))
      result = pd.merge(df_dict[parent_table],result_child_merge,left_on=parent_key,right_on=child_key,how='inner')[result_col_list]
      logging.warning("about to leave generate_result")
   return(result)

class action_condition_by_movie_ordered(Action):
   """return the values from movie table"""
   def name(self) -> Text:
      return "action_condition_by_movie_ordered"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # get dictionary of slot values
      slot_dict = tracker.current_slot_values()
      # apply mappings in slot_dict from Rasa to table schema
      slot_dict = prep_slot_dict(slot_dict)
      condition_dict = {}
      condition_dict = get_condition_columns(slot_dict)
      # get_table expects a list of columns as its first arg, so just take keys from condition_dict dictionary
      logging.warning("ABOUT TO GET CONDITION TABLE ")
      condition_table = get_table(list(condition_dict.keys()),movie_schema)
      logging.warning("ABOUT TO GET RANKED TABLE ")
      ranked_table = get_table(slot_dict["ranked_col"],movie_schema)
      logging.warning("ABOUT TO GET SORT TABLE ")
      sort_table = get_table([slot_dict["rank_axis"]],movie_schema)
      logging.warning("condition_dict is "+str(condition_dict))
      logging.warning("condition_table is "+str(condition_table))
      logging.warning("ranked_col is "+str(slot_dict["ranked_col"]))
      logging.warning("ranked_table is "+str(ranked_table))
      logging.warning("sort_col is "+str(slot_dict["rank_axis"]))
      logging.warning("sort_table is "+str(sort_table))
      # work through condition columns to get preliminary result
      result_pre_sort = generate_result(slot_dict,condition_dict,condition_table,ranked_table)
      logging.warning("past result_pre_sort")
      logging.warning(" result_pre_sort type"+str(type(result_pre_sort)))
      logging.warning(" df_dict[sort_table] type"+str(type(df_dict[sort_table[slot_dict["rank_axis"]]])))
      '''
      # join result table with sort table - TODO CHECK IF THIS HAS TO BE PUT BACK AGAIN OR SAFE TO INCLUDE RANK_AXIS ALL THE TIME
      if sort_table[slot_dict["rank_axis"]] == parent_table:
         right_key = parent_key
      else:
         right_key = child_key
      logging.warning(" result_pre_sort "+str(result_pre_sort))
      result_pre_sort = pd.merge(result_pre_sort,df_dict[sort_table[slot_dict["rank_axis"]]],left_on=parent_key,right_on=right_key,how='inner')
      logging.warning(" result_pre_sort "+str(result_pre_sort))
      '''
      # check the direction of sort
      if slot_dict["ascending_descending"] == "ascending":
         sort_direction_ascending = True
      else:
         sort_direction_ascending = False
      result = result_pre_sort.sort_values(by = [slot_dict["rank_axis"]],ascending=sort_direction_ascending)[slot_dict["ranked_col"]]
      for index, row in result.iterrows():
         logging.warning(str(result.loc[[index]]))
         dispatcher.utter_message(str(result.loc[[index]]))
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission validated")
      return []


# new condition_by_movie class:
#     - JSON columns processed in separate dataframes rather than native
#     - code generalized to handle a wide variety of queries
# TO DO: SWITCH TO condition_by_movie to test an "all the same table" query





class action_condition_by_movie(Action):
   """return the values from movie table"""
   def name(self) -> Text:
      return "action_condition_by_movie"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # get dictionary of slot values
      slot_dict = tracker.current_slot_values()
      for table in movie_schema:
         logging.warning("table is: "+str(table))
      # apply mappings in slot_dict from Rasa to table schema
      slot_dict = prep_slot_dict(slot_dict)
      condition_dict = {}
      condition_dict = get_condition_columns(slot_dict)
      # get_table expects a list of columns as its first arg, so just take keys from condition_dict dictionary
      logging.warning("ABOUT TO GET CONDITION TABLE ")
      condition_table = get_table(list(condition_dict.keys()),movie_schema)
      logging.warning("ABOUT TO GET RANKED TABLE ")
      ranked_table = get_table(slot_dict["ranked_col"],movie_schema)
      logging.warning("condition_dict is "+str(condition_dict))
      logging.warning("condition_table is "+str(condition_table))
      logging.warning("ranked_cod is "+str(slot_dict["ranked_col"]))
      logging.warning("ranked_table is "+str(ranked_table))
      # result = generate_result(slot_dict,condition_dict,condition_table,ranked_table)
      # TODO lowercase strings for comparison
      result = {}
      if same_table(list(condition_table.values()),list(ranked_table.values())):
         logging.warning("same_table condition_table "+str(condition_table))
         first_same = True
         # iterate through conditions keeping all columns
         for condition in condition_dict:
            logging.warning("in single table condition loop for condition "+str(condition))
            logging.warning("in single table condition loop for condition_table[condition] "+str(condition_table[condition]))
            if first_same:
               # first time through loop set base_df
               base_df = df_dict[condition_table[condition]]
               first_same = False
            logging.warning("in single table condition loop for condition_dict[condition] "+str(condition_dict[condition]))
            # TODO: need to handle list of conditions properly - currently OR for a list
            if isinstance(condition_dict[condition], list):
               base_df = base_df[base_df[condition].isin(condition_dict[condition])]
            else:
               base_df = base_df[base_df[condition] == str(condition_dict[condition])]
         logging.warning("RESULT IS "+str(base_df[slot_dict["ranked_col"]]))
         result = base_df[slot_dict["ranked_col"]]
      else:
         logging.warning("different condition_table"+str(condition_table)+" ranked_table "+str(ranked_table))
         # TODO: eventually want to consider a class to replace all the various dictionaries
         # but for now, just make the condition and ranked table containers dictionaries indexed by slot/column
         # rather than lists
         
         # condition and rank in different tables
         first_different = True
         child_key_df_dict = {}
         for condition in condition_table:
            # check if condition value is a list
            # for this condition, build the list of columns to pull from the child table
            condition_columns_to_pull = get_condition_columns_to_pull(child_key, ranked_table, condition_table[condition])
            if isinstance(condition_dict[condition], list):
               # TODO complete logic for dealing with conditions that are lists
               logging.warning("condition_dict is a list "+str(condition))
               sub_condition_df_dict = {}
               # iterate through each element in the condition value list getting a df of matching child keys
               for sub_condition in condition_dict[condition]:
                  logging.warning("sub_condition is "+str(sub_condition))
                  sub_condition_df_dict[sub_condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition].str.contains(sub_condition)][condition_columns_to_pull]
                  logging.warning("sub_condition_df_dict[sub_condition] len is "+str(len(sub_condition_df_dict[sub_condition])))
                  logging.warning("sub_condition_df_dict[sub_condition] is "+str(sub_condition_df_dict[sub_condition]))
               logging.warning("sub_condition_df_dict len is "+str(len(sub_condition_df_dict)))
               # merge the child key dfs to get a single df containing the intersection of child keys
               first_sub_condition = True
               for sub_condition in sub_condition_df_dict:
                  logging.warning("sub_condition in merge loop is "+str(sub_condition))
                  if first_sub_condition:
                     first_sub_condition = False
                     child_key_df_dict[condition] = sub_condition_df_dict[sub_condition]
                  else:
                     child_key_df_dict[condition] = pd.merge(child_key_df_dict[condition],sub_condition_df_dict[sub_condition],on=child_key,how='inner')
                  logging.warning("sub_condition child_key_df_dict[condition] len is "+str(len(child_key_df_dict[condition])))
               logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
            else:
               # condition is not a list
               logging.warning("in multi table condition loop for not list condition "+str(condition))
               # build df that just contains child_keys for this
               child_key_df_dict[condition] = df_dict[condition_table[condition]][df_dict[condition_table[condition]][condition] == condition_dict[condition]][condition_columns_to_pull]
               logging.warning("number of rows in child_key_df "+str(len(child_key_df_dict[condition].index)))
         for condition in condition_table:
            # iteratively merge child key tables
            if first_different:
               logging.warning("got first different "+str(condition))
               logging.warning("number of rows in child_key_df second loop "+str(len(child_key_df_dict[condition].index)))               
               result_child_merge = child_key_df_dict[condition]
               first_different = False
            else:
               result_child_merge = pd.merge(result_child_merge,child_key_df_dict[condition],on=child_key,how='inner')
         # now merge with parent table
         logging.warning("number of rows in child_key_df "+str(len(result_child_merge.index)))
         logging.warning("type of result_child_merge is "+str(type(type(result_child_merge))))
         for item_c in result_child_merge:
            logging.warning("item is "+str(item_c))
         first_final = True
         # TODO need to get table from among ranked_tables that has to be merged
         result = pd.merge(df_dict[parent_table],result_child_merge,left_on=parent_key,right_on=child_key,how='inner')[slot_dict["ranked_col"]]
      logging.warning("number of rows in result "+str(len(result)))
      # TODO NEED TO FIX DISPLAY OF MULTI ENTRY OUTPUT - CURRENTLY GLITCHY
      # output result
      # for index, row in df.iterrows():
      logging.warning("result is "+str(result))
      for index, row in result.iterrows():
         logging.warning(str(result.loc[[index]]))
         dispatcher.utter_message(str(result.loc[[index]]))

      
      logging.warning("COMMENT: end of transmission")
      dispatcher.utter_message("COMMENT: end of transmission validated")
      return []

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
      
class action_condition_by_media(Action):
   """return the values from movie table"""
   def name(self) -> Text:
      return "action_condition_by_media"
   def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      image = "https://image.tmdb.org/t/p/w500/rhIRbceoE9lR4veEXuwCC2wARtG.jpg"
      dispatcher.utter_message("COMMENT: before end of transmission validated")
      dispatcher.utter_attachment(image)
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

# Property of KarmaAI 
                




   
