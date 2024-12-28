from flask import Flask, render_template, jsonify
import json

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
    return render_template('faq.html', faqs=faq_data)

# API to fetch FAQs from JSON file
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    with open('static/faqs.json') as f:
        faqs = json.load(f)
    return jsonify(faqs)



if __name__ == '__main__':
    app.run(debug=True)
