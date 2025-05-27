import requests

def get_temperature(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f"{city_name},US",
        'appid': api_key,
        'units': 'imperial'  # Fahrenheit
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        return temp
    else:
        return None

def main():
    api_key = "YOUR_API_KEY_HERE"  # Replace this with your OpenWeatherMap API key
    city = input("Enter a major U.S. city: ").strip()
    
    temp = get_temperature(city, api_key)
    if temp is not None:
        print(f"The current temperature in {city.title()} is {temp:.1f}°F.")
    else:
        print("Sorry, couldn't find weather data for that city.")

if __name__ == "__main__":
    main()
