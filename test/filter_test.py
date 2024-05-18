import requests
import json

# text_url = "http://127.0.0.1:5004/filter"
text_url = "https://staging.d2z3gii7z44mha.amplifyapp.com:5004/filter"
text = "They are playing with his friends"
text = "bitches much twitter"
text = "Play in a park with my children"

text_dict = {
    "text": text
}
header = {
    "Content-type": "application/json"
}
response = requests.post(text_url, headers=header, data=json.dumps(text_dict))
if response.status_code == 200:
    res = response.json()
    prediction = res["prediction"]
    if(prediction != 2):
        print("bad prompt")
    else:
        print("good prompt")
else:
    print("status code incorrect")