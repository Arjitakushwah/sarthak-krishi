from flask import Flask, render_template, jsonify, request
import json
import joblib
import numpy as np

# Load the trained model
model = joblib.load('NOTEBOOKS\RandomForest.pkl')


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

    # Prepare the input features
    features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall, 1]])

    # Predict the crop
    prediction = model.predict(features)

    # Render the result on the page with the recommendation
    return render_template('crop.html', recommendation=prediction[0])




if __name__ == '__main__':
    app.run(debug=True)
