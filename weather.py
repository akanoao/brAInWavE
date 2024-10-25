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
        weather_description = data['weather'][0]['description']
        print(data)
        print(f"City: {city}")
        print(f"Temperature: {temperature} °C")
        print(f"Weather: {weather_description.capitalize()}")
    else:
        print("Error:", response.status_code, response.json().get("message", "Unknown error"))

# Example usage
if __name__ == "__main__":
    city_name = input("Enter the city name: ")
    api_key = "1742867b48c91cbfd96b692e8905626a"  # Replace with your actual API key
    get_weather(city_name, api_key)
