from dotenv import load_dotenv, find_dotenv
load_dotenv('./env.txt')

import streamlit as st
from langchain_utils import get_recomendation

st.sidebar.title("Recomendations")

temperature = st.sidebar.slider("Select the creativity for your answer", 0.0, 2.0, 0.7, step=0.1)
#reference_place = "Plaza de Armas de Arequipa"
reference_place= st.sidebar.text_input(label="Reference place")
# origin="Escuela Profesional de Ciencia de la Computación"
origin = st.sidebar.text_input(label="Start point")
# activities="fast food and cinema"
activities = st.sidebar.text_area(label="Enter your activity")
# radius=25
radius = st.sidebar.slider("radius of search in meters", 25, 100, 25, step=1)
# order_by = "arrival time"
order_by = st.sidebar.selectbox("order_by",("arrival time", "rating"))
# mode="walking"
mode = st.sidebar.selectbox("mode",("walking", "driving"))
# language="spanish"
language = st.sidebar.selectbox("language", ("spanish", "english"))

submit_button = st.sidebar.button("search")

if submit_button:
    response = get_recomendation(
        reference_place=reference_place,
        order_by=order_by,
        origin=origin,
        activities=activities,
        radius=radius,
        mode=mode,
        language=language,
        temperature=temperature
    )
    st.title(f"Nearest recomendations for {activities}")
    st.write(response.content)