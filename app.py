from flask import Flask, render_template, jsonify, request
import json
import requests
import joblib
import numpy as np
import pandas as pd
from utils.fertilizer import fertilizer_dic
from markupsafe import Markup
from fuzzywuzzy import process
from google import genai

# Load the trained model
crop_model = joblib.load('NOTEBOOKS\RandomForest.pkl')
fertilizer_model = joblib.load('NOTEBOOKS\RandomForest.pkl')

#weather api
WEATHER_API_KEY = "34bd3fee32a8027642574e732728a7d7"
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

@app.route('/weather')
def weather():
    return render_template('weather.html', title="Weather Prediction")

@app.route('/disease_prediction')
def disease_prediction():
    return render_template('disease.html', title="Disease Prediction")

@app.route('/schemes')
def schemes():
    return render_template('schemes.html', title="Government Schemes")

@app.route('/news')
def news():
    return render_template('news.html', title="News & Events")

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
    

# Load the chat question data from the JSON file


# Dummy chatbot response function (to be improved later with ML models or rule-based responses)
def get_chatbot_response(user_message):
    with open('static/json/chat.json', 'r') as file:
        faq_data = json.load(file)
    # Normalize and find best match using fuzzy matching
    best_match = process.extractOne(user_message, faq_data.keys())
    
    if best_match and best_match[1] > 80:  # You can set your threshold
        return faq_data[best_match[0]]
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get user message from the request
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get the chatbot's response
    bot_response = get_chatbot_response(user_message)

    # Return the chatbot's response as JSON
    return jsonify({"response": bot_response})


# Initialize the Gemini client with your API key
client = genai.Client(api_key="AIzaSyA3488jY1IFUZowigfFtQ9m9zRlX-3wTmc")

import re

def clean_response(text):
    # Remove *, -, and unwanted bullet characters
    text = re.sub(r'^\s*[\*\-\•]\s*', '', text, flags=re.MULTILINE)
    # Optionally remove extra newlines if needed
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

def get_gemini_response(user_input):
    try:
        instruction = (
            "Answer in simple paragraph format without using any bullets (*, -, •) or markdown syntax. "
            "Just use plain text. Start directly with the answer. No headings, no lists, only clean sentences."
        )
        final_prompt = instruction + "\n\n" + user_input

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=final_prompt
        )

        # Now clean the response text
        clean_text = clean_response(response.text)
        return clean_text
    except Exception as e:
        return f"Error: {str(e)}"

 
@app.route('/chat')
def chat2():
    return render_template('chat.html')

# Route for handling chatbot requests (API endpoint)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()  # Get the request data (JSON)
    user_message = data.get("message")  # Extract message
    
    if not user_message:
        return jsonify({"response": "Please provide a question."})
    
    # Get response from Gemini API
    response_text = get_gemini_response(user_message)
    
    return jsonify({"response": response_text})




if __name__ == '__main__':
    app.run(debug=True)
