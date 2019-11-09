
## file path1
* greet
  - utter_greet
  - utter_get_file_columns
* get_file_columns
  - action_file_columns
  - utter_get_file_row
* get_file_row
  - action_file_row
  - utter_what_next
* get_first_n_rows
  - action_first_n_rows
  - utter_what_next

## New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","cast_name":"Jack Lemmon"}
    - slot{"ranked_col":"movies"}
    - slot{"cast_name":"Jack Lemmon"}
    - action_condition_by_movie


## New Story
* greet
    - utter_what_next
* condition_by_media{"media":"poster","movie":"Harry Meet Sally"}
    - slot{"media":"poster"}
    - slot{"movie":"Harry Meet Sally"}
    - action_condition_by_media



## New Story
* greet
    - utter_what_next
* condition_by_movie_ordered{"ranked_col":"movies","director":"Woody Allen","rank_axis":"popularity"}
    - slot{"ranked_col":"movies"}
    - slot{"director":"Woody Allen"}
	- slot{"rank_axis":"popularity"}
    - action_condition_by_movie_ordered


## New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","director":"Woody Allen"}
    - slot{"ranked_col":"movies"}
    - slot{"director":"Woody Allen"}
    - action_condition_by_movie

# New Story
* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"characters","cast_name":"Tom Hanks"}
    - slot{"ranked_col":"characters"}
    - slot{"cast_name":"Tom Hanks"}
    - action_condition_by_movie


## say goodbye
* goodbye
  - utter_goodbye

## New Story

* greet
    - utter_greet
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row

## New Story

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"3"}
    - slot{"row_number":"3"}
    - action_file_row

## New Story

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"6"}

## New Story

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"6"}

## Chat with me

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"8"}
    - slot{"row_number":"8"}
    - action_file_row

## Chat with me

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"8"}
    - slot{"row_number":"8"}
    - action_file_row

## New Story

* greet
    - utter_greet
    - utter_get_file_columns
* get_file_columns{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - slot{"file_name":"https://raw.githubusercontent.com/ryanmark1867/manning/master/CSV_XLS/Streetcar%20Jan%202014.csv"}
    - action_file_columns
    - utter_get_file_row
* get_file_row{"row_number":"3"}
    - slot{"row_number":"3"}
    - action_file_row
    - utter_what_next
* get_last_n_rows{"row_range":"4"}
    - slot{"row_range":"4"}
    - action_last_n_rows
    - utter_what_next
* get_first_n_rows{"row_range":"3"}
    - slot{"row_range":"3"}
    - action_first_n_rows

## New Story

* greet
    - utter_what_next
* condition_by_year{"top_bottom":"top","ranked_col":"movies","row_number":"2004"}
    - slot{"ranked_col":"movies"}
    - slot{"row_number":"2004"}
    - slot{"top_bottom":"top"}
    - action_condition_by_year

## New Story

* greet
    - utter_greet
    - utter_what_next
* condition_by_year{"top_bottom":"top","ranked_col":"movies","year":"2004"}
    - slot{"ranked_col":"movies"}
    - slot{"top_bottom":"top"}
    - slot{"year":"2004"}
    - action_condition_by_year

## New Story

* greet
    - utter_what_next
* condition_by_year{"top_bottom":"top","ranked_col":"movies","year":"1948"}
    - slot{"ranked_col":"movies"}
    - slot{"top_bottom":"top"}
    - slot{"year":"1948"}
    - action_condition_by_year

## New Story

* greet
    - utter_what_next
* condition_by_year{"top_bottom":"top","ranked_col":"movies","year":"1948"}
    - slot{"ranked_col":"movies"}
    - slot{"top_bottom":"top"}
    - slot{"year":"1948"}
    - action_condition_by_year

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"Taxi Driver"}
    - slot{"movie":"Taxi Driver"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"Toy Story"}
    - slot{"movie":"Toy Story"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"plot","movie":"The Exorcist"}
    - slot{"movie":"The Exorcist"}
    - slot{"ranked_col":"plot"}
    - action_condition_by_movie

## New Story

* greet
    - utter_what_next
* condition_by_movie{"ranked_col":"movies","keyword":"midlife crisis"}
    - slot{"ranked_col":"movies"}
    - slot{"keyword":"midlife crisis"}
    - action_condition_by_movie
	
	
