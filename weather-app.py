import requests

def get_temperature(city_name, api_key):
    """
    Retrieves the current temperature in Fahrenheit for a specified U.S. city using the OpenWeatherMap API.
    
    Args:
        city_name: Name of the U.S. city.
        api_key: OpenWeatherMap API key.
    
    Returns:
        The current temperature in Fahrenheit as a float if successful, or None if an error occurs or data is unavailable.
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
        print(f"HTTP error occurred: {http_err}")
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
    """
    Prompts the user for a U.S. city and displays its current temperature in Fahrenheit.
    
    Retrieves the OpenWeatherMap API key from the environment, requests the city name from the user, and prints the current temperature if available. Displays error messages for missing API key, empty city input, or failed data retrieval.
    """
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


import unittest
from unittest.mock import patch, Mock, MagicMock
import requests
from weather-app import get_temperature, main


class TestGetTemperature(unittest.TestCase):
    """Test cases for the get_temperature function."""

    @patch('weather-app.requests.get')
    def test_successful_temperature_fetch(self, mock_get):
        """Test successful temperature retrieval."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'main': {'temp': 72.5}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_temperature("New York", "valid_api_key")
        
        self.assertEqual(result, 72.5)
        mock_get.assert_called_once_with(
            "https://api.openweathermap.org/data/2.5/weather",
            params={'q': 'New York,US', 'appid': 'valid_api_key', 'units': 'imperial'},
            timeout=10
        )

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_invalid_api_key_none(self, mock_print, mock_get):
        """Test with None API key."""
        result = get_temperature("Chicago", None)
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Invalid or missing API key.")
        mock_get.assert_not_called()

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_invalid_api_key_empty_string(self, mock_print, mock_get):
        """Test with empty string API key."""
        result = get_temperature("Chicago", "")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Invalid or missing API key.")
        mock_get.assert_not_called()

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_invalid_api_key_non_string(self, mock_print, mock_get):
        """Test with non-string API key."""
        result = get_temperature("Chicago", 12345)
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Invalid or missing API key.")
        mock_get.assert_not_called()

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_http_error_401_unauthorized(self, mock_print, mock_get):
        """Test HTTP 401 Unauthorized error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response

        result = get_temperature("Boston", "invalid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once()
        self.assertIn("HTTP error occurred", str(mock_print.call_args))

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_http_error_404_not_found(self, mock_print, mock_get):
        """Test HTTP 404 Not Found error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = get_temperature("InvalidCity", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once()
        self.assertIn("HTTP error occurred", str(mock_print.call_args))

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_connection_error(self, mock_print, mock_get):
        """Test network connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network unreachable")

        result = get_temperature("Seattle", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Network connection error.")

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_timeout_error(self, mock_print, mock_get):
        """Test request timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        result = get_temperature("Miami", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: The request timed out.")

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_generic_request_exception(self, mock_print, mock_get):
        """Test generic request exception."""
        mock_get.side_effect = requests.exceptions.RequestException("Unknown error")

        result = get_temperature("Phoenix", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once()
        self.assertIn("An unexpected error occurred", str(mock_print.call_args))

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_json_parsing_error(self, mock_print, mock_get):
        """Test JSON parsing error."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_temperature("Denver", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Failed to parse JSON response.")

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_unexpected_response_structure_missing_main(self, mock_print, mock_get):
        """Test response with missing 'main' key."""
        mock_response = Mock()
        mock_response.json.return_value = {'weather': [{'description': 'clear sky'}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_temperature("Atlanta", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Unexpected response structure.")

    @patch('weather-app.requests.get')
    @patch('builtins.print')
    def test_unexpected_response_structure_missing_temp(self, mock_print, mock_get):
        """Test response with missing 'temp' key."""
        mock_response = Mock()
        mock_response.json.return_value = {'main': {'humidity': 65}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_temperature("Portland", "valid_key")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Error: Unexpected response structure.")


class TestMain(unittest.TestCase):
    """Test cases for the main function."""

    @patch('weather-app.get_temperature')
    @patch('builtins.input')
    @patch('weather-app.os.getenv')
    @patch('builtins.print')
    def test_successful_flow(self, mock_print, mock_getenv, mock_input, mock_get_temp):
        """Test successful execution with valid inputs."""
        mock_getenv.return_value = "test_api_key"
        mock_input.return_value = "  San Francisco  "
        mock_get_temp.return_value = 68.3

        main()

        mock_getenv.assert_called_once_with('OPENWEATHER_API_KEY')
        mock_input.assert_called_once_with("Enter a major U.S. city: ")
        mock_get_temp.assert_called_once_with("San Francisco", "test_api_key")
        mock_print.assert_called_once_with("The current temperature in San Francisco is 68.3°F.")

    @patch('weather-app.os.getenv')
    @patch('builtins.print')
    def test_missing_api_key_env_var(self, mock_print, mock_getenv):
        """Test when OPENWEATHER_API_KEY environment variable is not set."""
        mock_getenv.return_value = None

        main()

        mock_getenv.assert_called_once_with('OPENWEATHER_API_KEY')
        mock_print.assert_called_once_with("Error: Please set the OPENWEATHER_API_KEY environment variable")

    @patch('builtins.input')
    @patch('weather-app.os.getenv')
    @patch('builtins.print')
    def test_empty_city_name(self, mock_print, mock_getenv, mock_input):
        """Test when user enters empty city name."""
        mock_getenv.return_value = "test_api_key"
        mock_input.return_value = "   "

        main()

        mock_print.assert_called_once_with("Error: City name cannot be empty")

    @patch('weather-app.get_temperature')
    @patch('builtins.input')
    @patch('weather-app.os.getenv')
    @patch('builtins.print')
    def test_get_temperature_returns_none(self, mock_print, mock_getenv, mock_input, mock_get_temp):
        """Test when get_temperature fails and returns None."""
        mock_getenv.return_value = "test_api_key"
        mock_input.return_value = "InvalidCity"
        mock_get_temp.return_value = None

        main()

        mock_get_temp.assert_called_once_with("InvalidCity", "test_api_key")
        mock_print.assert_called_once_with("Sorry, couldn't find weather data for that city.")

    @patch('weather-app.get_temperature')
    @patch('builtins.input')
    @patch('weather-app.os.getenv')
    @patch('builtins.print')
    def test_temperature_formatting(self, mock_print, mock_getenv, mock_input, mock_get_temp):
        """Test temperature output formatting with various values."""
        mock_getenv.return_value = "test_api_key"
        mock_input.return_value = "los angeles"
        mock_get_temp.return_value = 75.678

        main()

        mock_print.assert_called_once_with("The current temperature in Los Angeles is 75.7°F.")


if __name__ == '__main__':
    unittest.main()
