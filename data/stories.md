## superlative ranking
* greet
  - utter_greet
  - utter_what_next
* rank_col_by_other_col  
  - action_rank_col_by_other_col
  - utter_what_next

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
