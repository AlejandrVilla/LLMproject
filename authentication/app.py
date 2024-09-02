from dotenv import load_dotenv
load_dotenv('./env.txt')
import requests
from flask import Flask, request, jsonify, session, json
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_session import Session
import os
from uuid import uuid4

sql_user = os.environ['MYSQL_USER']
sql_pw = os.environ['MYSQL_PASSWORD']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = sql_user
app.config['MYSQL_PASSWORD'] = sql_pw
app.config['MYSQL_DB'] = 'recomendation_app_db'
mysql = MySQL(app)

# Configuración para Cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # O 'None' si necesitas compartir cookies entre sitios cruzados
app.config['SESSION_COOKIE_SECURE'] = True  # Asegúrate de que esté en False para desarrollo local
CORS(
    app
)

server_session = Session(app)

# Personal user info
@app.route('/@me/', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def get_current_user():
    request_type = request.headers.get("Request-type")
    print(request_type)
    # Extract personal info
    user_id = session.get('user_id')
    if not user_id:
        res_dict = {"error": 'Not logged'}
        response = jsonify(res_dict)
        response.status_code = 401
        return response
    cur = mysql.connection.cursor()
    cur.execute('''SELECT username, email, name, last_name FROM user WHERE user_id = %s''', (user_id, ))
    data = cur.fetchall()
    cur.close()
    username = data[0][0]
    email = data[0][1]
    name = data[0][2]
    last_name = data[0][3]

    # Extract latest prompt searchs
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT prompt_id, prompt_text FROM user AS u JOIN prompt AS p WHERE u.user_id = p.user_id AND u.user_id = %s;
        ''',
        (user_id, )
    )
    prompts = cur.fetchall()
    cur.close
    # prompt_id, prompt_text
    prompts = [list(tupla) for tupla in prompts]

    # Extract latest places
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        SELECT up.place_id, p.placename FROM user_place as up JOIN place as p WHERE up.place_id = p.place_id AND up.user_id = %s;
        ''',
        (user_id, )
    )
    places = cur.fetchall()
    cur.close
    # place_id, placename
    places = [list(tupla) for tupla in places]

    # answer
    res_dict = {
        'uid': user_id,
        'username': username,
        'email': email,
        'name': name,
        'last_name': last_name,
        'prompts': prompts,
        'places': places
    }
    response = jsonify(res_dict)
    response.status_code = 200
    return response

# Sign up
@app.route('/signup/', methods=['POST'])
@cross_origin(supports_credentials=True) # allow all origins all methods.
def signup():
    request_type = request.headers.get("Request-type")
    print(request_type)
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    name = request.json.get('name')
    last_name = request.json.get('last_name')

    # check if user exists by username
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from user WHERE username = %s''', (username,))
    data = cur.fetchall()
    if len(data) != 0:
        res_dict = {"error": 'User already exists'}
        response = jsonify(res_dict)
        response.status_code = 409
        return response
    
    # hash password and send data to db
    hashed_pw = bcrypt.generate_password_hash(password)
    uid = uuid4().hex
    cur.execute(
        '''
        INSERT into user (user_id, username, password, email, name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (uid, username, hashed_pw, email, name, last_name)
    )
    mysql.connection.commit()
    cur.close()

    session["user_id"] = uid

    # answer
    res_dict = {
        "content": 'New user created',
        'uid': uid,
        'email': email
    }
    response = jsonify(res_dict)
    response.status_code = 200
    return response

# Login
@app.route('/login/', methods=['POST'])
@cross_origin(supports_credentials=True) # allow all origins all methods.
def login():
    request_type = request.headers.get("Request-type")
    print(request_type)
    username = request.json.get('username')
    password = request.json.get('password')

    # check if user exists by username
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user_id, password, email from user WHERE username = %s''', (username,))
    data = cur.fetchall()
    cur.close()

    if len(data) == 0:
        res_dict = {"error": 'User doesn\'t exists'}
        response = jsonify(res_dict)
        response.status_code = 409
        return response
    
    db_hashed_pw = data[0][1]
    if not bcrypt.check_password_hash(db_hashed_pw, password):
        res_dict = {"error": 'Incorrect password'}
        response = jsonify(res_dict)
        response.status_code = 409
        return response

    user_id = data[0][0]
    email = data[0][2]

    session["user_id"] = user_id

    res_dict = {
        "content": 'Login succesfully',
        'uid': user_id,
        'email': email
    }
    response = jsonify(res_dict)
    response.status_code = 200
    # response.set_cookie('session', session['user_id'], httponly=False, samesite='None')
    return response

# Logout
@app.route('/logout/', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True) # allow all origins all methods.
def logout_user():
    request_type = request.headers.get("Request-type")
    print(request_type)
    session.pop('user_id')
    res_dict = {
        "content": 'Succesfully logout',
    }
    response = jsonify(res_dict)
    response.status_code = 200
    return response

# Pass to get recomendation microservice
@app.route('/get-recomendation/', methods=['POST'])
@cross_origin(supports_credentials=True) # allow all origins all methods.
def get_recomendation():
    content_type = request.headers.get('Content-type')
    if (content_type != "application/json"):
        message = {
            "status": 404,
            "message": "Content type is unsuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
        return response
    
    data = request.json
    activities = data.get('activities')
    origin = data.get('origin')
    radius = data.get('radius')
    language = data.get('language')
    temperature = data.get('temperature')

    print("user data:")
    print(f"activities: {activities}")
    print(f"origin: {origin}")
    print(f"radius: {radius}")
    print(f"language: {language}")
    print(f"temperature: {temperature}")

    user_id = session.get("user_id")
    print(f"user: {user_id}")

    get_recomendation_url = "http://127.0.0.1:5001/get-recomendation"
    headers = {"Content-type": "application/json"}
    user_info = {
        "activities": activities,
        "origin": origin,
        "radius": radius,
        "language": language,
        "temperature": temperature,
        "user_id": user_id
    }

    response = requests.post(
        get_recomendation_url, 
        headers=headers, 
        data=json.dumps(user_info)
    )

    if response.status_code != 200:
        res = "Error trying to send user info to get-recomendation microservice"
        return 0, res
    
    print(f"user info sent to get_recomendation microservice")
    res = response.json()
    group_places = res["content"]
    res_dict = {"content": group_places}
    response = jsonify(res_dict)
    response.status_code = 200
    return response

# Pass to get plan microservice
@app.route('/get-plan/', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_plan():
    content_type = request.headers.get('Content-type')
    if (content_type != "application/json"):
        message = {
            "status": 404,
            "message": "Content type is unsuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
        return response
    
    data = request.json
    ind = int(data.get('ind'))
    plan_type = data.get('plan_type')
    origin = data.get('origin')
    mode = data.get('mode')
    temperature = data.get('temperature')

    print("user data:")
    print(f"origin: {origin}")
    print(f"mode: {mode}")
    print(f"plan_type: {plan_type}")
    print(f"temperature: {temperature}")
    print(f"index plan: {ind}")

    user_id = session.get('user_id')
    print(f"user: {user_id}")

    post_plan_url = "http://127.0.0.1:5005/get-plan"
    headers = {"Content-type": "application/json"}
    plan_info = {
        "ind": ind,
        "origin": origin,
        "mode": mode,
        "plan_type": plan_type,
        "temperature": temperature,
        "user_id": user_id
    }

    response = requests.post(
        post_plan_url,
        headers=headers,
        data=json.dumps(plan_info)
    )

    if response.status_code != 200:
        res = "Error trying to send place index to get-plan microservice"
        return 0, res
    
    print(f"place index sent to get-plan microservice")
    res = response.json()
    res_dict = {
        "content": res['content'],
        "places_info": res['places_info']
    }
    response = jsonify(res_dict)
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)