from flask import Flask, render_template, request
import os
from utils import get_weather, find_location
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def weather():
    if request.method == "POST":
        city = request.form["city"]
        funcs = find_location(loc=city)

        city_data = funcs['location'].split(",")[0]
        weather_data = get_weather(api_key, city_data)

        if "error" in weather_data:
            error = "Sorry, we couldn't find weather information for that city."
            return render_template("index.html", error=error)
        else:
            location = city_data
            temperature = weather_data["temperature"]
            description = weather_data["description"]
            humidity = weather_data["humidity"]

            return render_template("index.html",
                                   location=location,
                                   temperature=temperature,
                                   description=description,
                                   humidity=humidity)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1957, debug=True)
