# LLM app with microservices
## ADD YOUR API KEYS
- Create a GoogleMaps API Key
- Create an OpenAI API key
- ADD your API keys to an env.txt file and copy it to the directories
    - extract_places
    - get_recomendation
    - summary_reviews
    - get_plan

```
OPENAI_API_KEY="YOUR_OPEN_AI_API_KEY"
GOOGLEMAPS_API_KEY="YOUR_GOOGLEMAPS_API_KEY"
```

## Frontend
### Install dependencies
```
cd frontend
npm install
```
### Run react app
```
npm start
```

## Backend
### Create an environment for each microservice
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

### Run the app on each microservice
```
python app.py
```
## Run in k8s
### Create an k8s cluster for example in aws
### Deploy services and deployments
```
cd k8s
cd deployment_services
kubectl apply -f .
```
### Create your own host and change in ingress-nginx.yaml file
```
spec:
  ingressClassName: "nginx"
  rules:
    - host: [your host]
```
### Apply nginx ingress controller
```
cd ingress
kubectl apply -f ingress-nginx.yaml
```
### Delete the secret.yaml file an set your secret