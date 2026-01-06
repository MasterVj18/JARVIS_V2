import requests

def get_weather(city_name):
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']



        wind_speed = data['wind']['speed']

        print(f"Weather in {city_name}:")
        print(f"Description: {weather_description}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print("Error: City not found")

