import requests

# Intents and responses
intents = {
    "greet": ["hello", "hi", "hey"],
    "get_weather": ["weather", "forecast", "temperature"],
    "goodbye": ["bye", "goodbye", "see you"]
}

# API Setup
API_KEY = "721212d17509a9911fc510bea7d4750e"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to get weather by latitude and longitude
def get_weather(lat, lon):
    try:
        response = requests.get(f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
        data = response.json()
        if data["cod"] != 200:
            return "Location not found. Please try again."
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The current weather in {city_name} is {temp}°C with {weather_desc}."
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

# Chatbot conversation
def chatbot():
    print("🤖 WeatherBot: Hello! I can give you weather updates.")
    while True:
        user_input = input("You: ")
        intent = get_intent(user_input)

        if intent == "greet":
            print("🤖 WeatherBot: Hello! How can I help you?")
        elif intent == "get_weather":
            try:
                lat = float(input("🤖 WeatherBot: Please enter the latitude: "))
                lon = float(input("🤖 WeatherBot: Please enter the longitude: "))
                print("🤖 WeatherBot:", get_weather(lat, lon))
            except ValueError:
                print("🤖 WeatherBot: Invalid input. Please enter numbers for latitude and longitude.")
        elif intent == "goodbye":
            print("🤖 WeatherBot: Goodbye! Have a great day.")
            break
        else:
            print("🤖 WeatherBot: I'm sorry, I didn't understand that.")

# Run the chatbot
chatbot()
