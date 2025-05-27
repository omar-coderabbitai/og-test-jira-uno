import requests

def get_temperature(city_name, api_key):
    """
    Fetches the current temperature in Fahrenheit for a given U.S. city
    using the OpenWeatherMap API.

    Parameters:
        city_name (str): The name of the U.S. city.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        float: Current temperature in Fahrenheit if successful.
        None: If an error occurs or the data cannot be retrieved.
    """
    if not api_key or not isinstance(api_key, str):
        print("Error: Invalid or missing API key.")
        return None

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f"{city_name},US",
        'appid': api_key,
        'units': 'imperial'
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'main' in data and 'temp' in data['main']:
            return data['main']['temp']
        else:
            print("Error: Unexpected response structure.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Network connection error.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"Error: An unexpected error occurred: {err}")
    except ValueError:
        print("Error: Failed to parse JSON response.")

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
