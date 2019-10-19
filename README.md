# chatbot
repository for Rasa chatbot investigation 2H 2019

Main directory contains standard Rasa files:
- domain.yml - customized to problem space
- config.yml
- endpoints.yml - updated to point to local Python server as documented in https://rasa.com/docs/rasa/core/actions/
- actions.py - bootstrap Python code (to load data files and collect metadata) and classes for each custom action

data subdirectory contains standard Rasa files:
- stories.md
- nlu.md
