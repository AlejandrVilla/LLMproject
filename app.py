import streamlit as st
import requests
import json

st.set_page_config(page_title="place recommendation app", layout='centered')

with st.sidebar:
    st.title("Recomendations")
    with st.form("form"):
        # temperature = st.sidebar.slider("Select the creativity for your answer", 0.0, 2.0, 0.7, step=0.1)
        temperature = 0.7
        #reference_place = "Plaza de Armas de Arequipa"
        reference_place= st.text_input(label="Reference place", help="A place to search around")
        # origin="Escuela Profesional de Ciencia de la Computación"
        origin = st.text_input(label="Start point", help="Where you will start your trip")
        # activities="fast food and cinema"
        activities = st.text_area(label="Enter your activity", help="Activitie you want to do")
        # radius=25
        # radius = st.sidebar.slider("radius of search in meters", 50, 1000, 100, step=10)
        radius = 100
        # order_by = "arrival time"
        # order_by = st.sidebar.selectbox("order_by",("arrival time", "rating"))
        with st.expander(":red[More options]"):
            order_by = "rating"
            # mode="walking"
            mode = st.selectbox("mode",("walking", "driving"))
            # language="spanish"
            language = st.selectbox("language", ("spanish", "english"))

        submit_button = st.form_submit_button("search", use_container_width=True)

if submit_button:
    url = 'http://localhost:5001/get_recomendation'
    recomendation = {
        'reference_place': reference_place, 
        'order_by': order_by,
        'origin': origin,
        'activities': activities,
        'radius': radius,
        'mode': mode,
        'language': language,
        'temperature': temperature
        }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=json.dumps(recomendation))

    if response.status_code == 200:
        resultado = response.json()
        st.title(f"Plan for your activity")
        st.write(resultado['content'])
    else:
        resultado = {'error': 'An error occurred while sending information.'}
        st.write(f"error: {resultado['error']}") 