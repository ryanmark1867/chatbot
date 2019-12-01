cd C:\personal\chatbot_july_2019\filebot_6
rasa train
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials_test.yml