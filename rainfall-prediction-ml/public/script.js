const form = document.getElementById("predict-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    MinTemp: parseFloat(document.getElementById("MinTemp").value),
    MaxTemp: parseFloat(document.getElementById("MaxTemp").value),
    Humidity9am: parseFloat(document.getElementById("Humidity9am").value),
    Humidity3pm: parseFloat(document.getElementById("Humidity3pm").value),
    Rainfall: 0.0,
    WindGustSpeed: 30,
    WindSpeed9am: 15,
    WindSpeed3pm: 18,
    Pressure9am: 1012,
    Pressure3pm: 1010,
    Temp9am: 18,
    Temp3pm: 22,
    Location: "Albury",
    WindDir9am: "N",
    WindDir3pm: "NW",
    WindGustDir: "W",
    RainToday: "No"
  };

  const res = await fetch("/api/predict", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  result.innerHTML = `Prediction: ${data.prediction}<br>Probability of rain: ${data.probability_rain}`;
});
