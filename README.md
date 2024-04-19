## ADD YOUR API KEYS
- Create a GoogleMaps API Key
- Create an OpenAI API key
- ADD your API keys to an env.txt file

```
OPENAI_API_KEY="YOUR_OPEN_AI_API_KEY"
GOOGLEMAPS_API_KEY="YOUR_GOOGLEMAPS_API_KEY"
```

## Create an environment
```
virtualenv -p python[version] [env-name]
```
## Activate the environment
- Windows
```
.\[env-name]\Scripts\activate
```
    
- Linux
```
source ./[env-name]/bin/activate
```

## Install requirements
```
pip isntall -r requirements.txt
```

## Run the project
```
streamlit run ./app.py
```