from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple rule-based chatbot responses
responses = {
    "hello": "Hi there! How can I assist you today?",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "recommend a crop": "Sure! Please enter soil details, temperature, and other parameters.",
    "recommend a fertilizer": "I can help! Enter soil nutrients (N, P, K) to get the best fertilizer recommendation.",
    "weather forecast": "You can check the weather on the weather prediction page.",
    "bye": "Goodbye! Have a great day!"
}

# Chatbot API route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()
    
    # Get response or a default reply
    response = responses.get(user_message, "I'm not sure about that. Can you rephrase?")
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
