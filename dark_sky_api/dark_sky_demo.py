# example of getting header data from dark-sky API


import requests

url = "https://dark-sky.p.rapidapi.com/43.653225,-79.383186,2007-03-01T01%253A32%253A33"

headers = {
    'x-rapidapi-host': "dark-sky.p.rapidapi.com",
    'x-rapidapi-key': "<>"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)


