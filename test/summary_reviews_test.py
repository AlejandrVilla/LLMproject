import requests
import json
from langchain_core.prompts.loading import load_prompt_from_config
from langchain_core.prompts import ChatPromptTemplate

with open('reviews_test.json', 'r') as file:
    all_places_reviews = json.load(file)

# print(type(all_places_reviews))

places_url = "http://127.0.0.1:5003/summary-reviews"
all_places_reviews = {"all_places_reviews": all_places_reviews}
headers = {"Content-type": "application/json"}
response = requests.post(places_url, headers=headers, data=json.dumps(all_places_reviews))
if response.status_code == 200:
    res = response.json()
    places_type = res["reviews_summary"]
else:
    places_type = None

print(type(places_type))
print(places_type)