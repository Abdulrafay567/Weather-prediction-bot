from flask import Flask, request, jsonify, render_template  
from dotenv import load_dotenv  # For loading environment variables
import requests  # For making API requests to OpenWeatherMap
import os  # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# API key from .env 
api_key = os.getenv("API_KEY")
aapi_key = os.getenv("BASE_URL")
# Flask app initialization
app = Flask(__name__)

# Intents and responses
intents = {
    "greet": ["hello", "hi", "hey"],
    "get_weather": ["weather", "forecast", "temperature"],
    "goodbye": ["bye", "goodbye", "see you"]
}


# Function to get weather by city name
def get_weather(city_name):
    try:
        response = requests.get(f"{aapi_key}?q={city_name}&appid={api_key}&units=metric")
        data = response.json()
        if data["cod"] != 200:
            return "City not found. Please try again."
        city = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The current weather in {city} is {temp}°C with {weather_desc}."
    except Exception as e:
        return "Error: Unable to fetch weather data."

# Function to identify user intent
def get_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent
    return None

# Route to render chatbot HTML page
@app.route('/')
def home():
    return render_template('chat.html')  # Renders the chat page

# API endpoint to handle user messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    intent = get_intent(user_message)

    if intent == "greet":
        response = "Hello! How can I help you?"
    elif intent == "get_weather":
        response = "Please provide a city name."
    elif intent == "goodbye":
        response = "Goodbye! Have a great day."
    else:
        response = "I'm sorry, I didn't understand that."

    return jsonify({"response": response})

# API endpoint to handle weather requests
@app.route('/weather', methods=['POST'])
def weather():
    city_name = request.json.get('city')
    response = get_weather(city_name)
    return jsonify({"response": response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5008)
