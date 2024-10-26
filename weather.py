import requests

def get_weather(city_name, api_key):
    # Define the endpoint URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    # Make a GET request to the OpenWeather API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        city = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        try:
            rain = data["rain"]["1h"]
        except KeyError:
            rain = 0.0

        # Return as JSON object
        return {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "rain": rain
        }
    else:
        # Return an error message
        return {"error": response.status_code, "message": response.json().get("message", "Unknown error")}

# Example usage
if __name__ == "__main__":
    city_name = input("Enter the city name: ")
    api_key = "1742867b48c91cbfd96b692e8905626a"  # Replace with your actual API key
    weather_data = get_weather(city_name, api_key)
    print(weather_data)
