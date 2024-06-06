import requests
import json
from langchain_core.prompts.loading import load_prompt_from_config
from langchain_core.prompts import ChatPromptTemplate

places_url = "http://localhost:5002/extract-places"
places_url = "https://www.guideplanner.pro/extract-places"
activities = "ir a comer ceviche y luego al parque a pasear"
# activities = "Go to the cinema and then play with my kids in the a park and go to the coffee"
language = "English"
activities_dict = {
    "activities": activities,
    "language": language,
}
headers = {"Content-type": "application/json"}
response = requests.post(places_url, headers=headers, data=json.dumps(activities_dict))
print(json.dumps(activities_dict))
if response.status_code == 200:
    res = response.json()
    places_type = res["places_type"]
    print("good")
else:
    places_type = None
    print("bad")

print(type(places_type))
print(places_type)