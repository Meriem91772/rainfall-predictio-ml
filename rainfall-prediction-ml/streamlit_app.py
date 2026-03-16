import streamlit as st
import requests

st.set_page_config(page_title="Rainfall Prediction", page_icon="🌧️")

st.title("🌧️ Rainfall Prediction Classifier")
st.write("Entrez les données météo pour prédire s'il pleuvra demain.")

date = st.text_input("Date", "2008-12-01")
location = st.text_input("Location", "Albury")
min_temp = st.number_input("MinTemp", value=13.4)
max_temp = st.number_input("MaxTemp", value=22.9)
rainfall = st.number_input("Rainfall", value=0.6)
evaporation = st.number_input("Evaporation", value=4.0)
sunshine = st.number_input("Sunshine", value=9.0)
wind_gust_dir = st.text_input("WindGustDir", "W")
wind_gust_speed = st.number_input("WindGustSpeed", value=44.0)
wind_dir_9am = st.text_input("WindDir9am", "W")
wind_dir_3pm = st.text_input("WindDir3pm", "WNW")
wind_speed_9am = st.number_input("WindSpeed9am", value=20.0)
wind_speed_3pm = st.number_input("WindSpeed3pm", value=24.0)
humidity_9am = st.number_input("Humidity9am", value=71.0)
humidity_3pm = st.number_input("Humidity3pm", value=22.0)
pressure_9am = st.number_input("Pressure9am", value=1007.7)
pressure_3pm = st.number_input("Pressure3pm", value=1007.1)
cloud_9am = st.number_input("Cloud9am", value=8.0)
cloud_3pm = st.number_input("Cloud3pm", value=7.0)
temp_9am = st.number_input("Temp9am", value=16.9)
temp_3pm = st.number_input("Temp3pm", value=21.8)
rain_today = st.selectbox("RainToday", ["No", "Yes"])

if st.button("Predict"):
    payload = {
        "Date": date,
        "Location": location,
        "MinTemp": min_temp,
        "MaxTemp": max_temp,
        "Rainfall": rainfall,
        "Evaporation": evaporation,
        "Sunshine": sunshine,
        "WindGustDir": wind_gust_dir,
        "WindGustSpeed": wind_gust_speed,
        "WindDir9am": wind_dir_9am,
        "WindDir3pm": wind_dir_3pm,
        "WindSpeed9am": wind_speed_9am,
        "WindSpeed3pm": wind_speed_3pm,
        "Humidity9am": humidity_9am,
        "Humidity3pm": humidity_3pm,
        "Pressure9am": pressure_9am,
        "Pressure3pm": pressure_3pm,
        "Cloud9am": cloud_9am,
        "Cloud3pm": cloud_3pm,
        "Temp9am": temp_9am,
        "Temp3pm": temp_3pm,
        "RainToday": rain_today
    }

    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=payload)
        data = response.json()

        if response.status_code == 200:
            st.success(f"Prediction: {data['prediction']}")
            st.info(f"Probability of rain: {data['probability_rain']:.4f}")
        else:
            st.error(data)
    except Exception as e:
        st.error(f"Error: {e}")
