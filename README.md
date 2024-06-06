# LLM app with microservices
## ADD YOUR API KEYS
- Create a GoogleMaps API Key
- Create an OpenAI API key
- ADD your API keys to an env.txt file and copy it to the directories
    - extract_places
    - get_recomendation
    - summary_reviews

```
OPENAI_API_KEY="YOUR_OPEN_AI_API_KEY"
GOOGLEMAPS_API_KEY="YOUR_GOOGLEMAPS_API_KEY"
```

## Frontend
### Create an environment for the UI
```
virtualenv -p python[version] [env-name]
```
### Activate the environment
- Windows
```
.\[env-name]\Scripts\activate
```
    
- Linux
```
source ./[env-name]/bin/activate
```

### Install requirements
```
pip isntall -r requirements.txt
```

### Run the app
```
streamlit run ./app.py
```

## Backend
- Use the following command to run the microservices with docker compose
```
docker-compose up --build
```
- The above command will create the containers, a private network and connect them

## Tests
- You can use the test directory to test the microservices
    - Extract places
    - Summary reviews 