import json
import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def get_weather(api_key, city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        data = response.json()

        # Extract relevant weather information
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        # Return the weather data
        return {
            "temperature": temperature,
            "description": weather_description,
            "humidity": humidity
        }
    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)
        return None


def find_location(loc: str):
    """find location"""
    completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": f"{loc}?"}],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        function_call="auto",
    )

    reply_content = completion.choices[0].message

    funcs = reply_content.to_dict()['function_call']['arguments']

    funcs = json.loads(funcs)  # {'location': 'Dallas'}

    return funcs
