from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, jsonify, request
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
)

# activities templates
activities_system_template = """\
You will receive a plan to do some activities and you have to categorize each type of places as a python array in {language} language, example:
["restaurant of pollo a la brasa",
"shopping mall",
"fast food"]
"""
activities_human_template = "{activities}"

activities_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(activities_system_template),
        HumanMessagePromptTemplate.from_template(activities_human_template)
    ]
)

app = Flask(__name__)

# Extract activities
@app.route('/extract_places', methods=["POST"])
def extract_places():
    content_type = request.headers.get('Content-type')
    if (content_type == "application/json"):
        data = request.json
        activities = data.get('activities')
        language = data.get('language')
        # Extract places
        chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0.7)
        activities_messages = activities_chat_prompt.format(
            language=language,
            activities=activities
        )
        places_type = chat_openai.invoke(activities_messages)
        # print(places_type.content)
        places_type = eval(places_type.content)
        print("places", places_type)
        # Format data
        # places type -> list
        res_dict = {"places_type": places_type}
        response = jsonify(res_dict)
        response.status_code = 200
    else:
        message = {
            "status": 404,
            "message": "Content type is insuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)