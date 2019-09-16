## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## file path
* greet
  - utter_greet
  - utter_get_file_columns
* get_file_columns
  - action_file_columns
  - utter_get_file_row
* get_file_row
  - action_file_row
* affirm
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

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
