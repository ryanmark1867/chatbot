## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## get columnname
* greet
  - utter_greet
* inform{"url":"https://medium.com/datadriveninvestor/build-a-flight-search-chatbot-from-scratch-using-rasa-part-2-4e99abee4e88"}
  - action_csv_info
#  - slot{"column_names": "['sepal_length','sepal_width','petal_length','petal_width','species']"} 
# get_columns
#  - utter_give_columns

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


