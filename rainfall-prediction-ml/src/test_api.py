import requests

payload = {
    "Date": "2008-12-01",
    "Location": "Albury",
    "MinTemp": 13.4,
    "MaxTemp": 22.9,
    "Rainfall": 0.6,
    "Evaporation": 4.0,
    "Sunshine": 9.0,
    "WindGustDir": "W",
    "WindGustSpeed": 44,
    "WindDir9am": "W",
    "WindDir3pm": "WNW",
    "WindSpeed9am": 20,
    "WindSpeed3pm": 24,
    "Humidity9am": 71,
    "Humidity3pm": 22,
    "Pressure9am": 1007.7,
    "Pressure3pm": 1007.1,
    "Cloud9am": 8,
    "Cloud3pm": 7,
    "Temp9am": 16.9,
    "Temp3pm": 21.8,
    "RainToday": "No"
}

response = requests.post("http://127.0.0.1:5000/predict", json=payload)

print("Status:", response.status_code)
print(response.json())
