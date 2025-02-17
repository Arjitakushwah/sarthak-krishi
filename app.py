from flask import Flask, render_template, jsonify, request
import json
import requests
import joblib
import numpy as np
import pandas as pd
from utils.fertilizer import fertilizer_dic
from markupsafe import Markup
# Load the trained model
crop_model = joblib.load('NOTEBOOKS\RandomForest.pkl')
fertilizer_model = joblib.load('NOTEBOOKS\RandomForest.pkl')

#weather api
WEATHER_API_KEY = "4867af3c5cff24159c594b45b0be9ca9"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title="Home - Sarthak Krishi")

@app.route('/crop_recommend')
def crop_recommend():
    return render_template('crop.html', title="Crop Recommendation")

@app.route('/fertilizer_recommendation')
def fertilizer_recommendation():
    return render_template('fertilizer.html', title="Fertilizer Recommendation")

@app.route('/disease_prediction')
def disease_prediction():
    return render_template('disease.html', title="Disease Prediction")

@app.route('/schemes')
def schemes():
    return render_template('schemes.html', title="Government Schemes")

@app.route('/faq')
def faq():
    with open('static/json/faq.json', 'r') as file:
        faq_data = json.load(file)
    return render_template('faq.html', faqs=faq_data, title="FAQ")

# API to fetch FAQs from JSON file
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    with open('static/faqs.json') as f:
        faqs = json.load(f)
    return jsonify(faqs)


# crop prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    nitrogen = float(request.form['nitrogen'])
    phosphorus = float(request.form['phosphorus'])
    potassium = float(request.form['potassium'])
    ph_value = float(request.form['ph_value'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    rainfall = float(request.form['rainfall'])
    soil = int(request.form['soil_type'])

    # Prepare the input features
    features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall, soil]])

    # Predict the crop
    prediction = crop_model.predict(features)

    # Render the result on the page with the recommendation
    return jsonify({'recommendation': prediction[0]})


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('DATA/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    recommendation = Markup(str(fertilizer_dic[key]))

    
    return jsonify({'recommendation': recommendation})





@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        city = request.form['city']
        response = requests.get(WEATHER_API_URL, params={
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Get temperature in Celsius
        })

        data = response.json()

        if response.status_code == 200:
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "wind_speed": data["wind"]["speed"]
            }
            return jsonify(weather_info)
        else:
            return jsonify({"error": data.get("message", "Unable to fetch weather data")})
    
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
