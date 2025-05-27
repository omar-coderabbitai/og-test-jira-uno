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
    import os
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Error: Please set the OPENWEATHER_API_KEY environment variable")
        return

    city = input("Enter a major U.S. city: ").strip()
    if not city:
        print("Error: City name cannot be empty")
        return

    temp = get_temperature(city, api_key)
    if temp is not None:
        print(f"The current temperature in {city.title()} is {temp:.1f}°F.")
    else:
        print("Sorry, couldn't find weather data for that city.")

if __name__ == "__main__":
    main()
