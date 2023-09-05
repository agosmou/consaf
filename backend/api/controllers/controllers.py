"""
controllers
"""
from flask import Flask, jsonify, request
from configs.configs import DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from api.services.services import (
    YoloService,
    RandomImage,
    Location,
    Weather,
    CleanUpObjectDetection,
)

ENV = "env"

app = Flask(__name__)

if ENV == "prod":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

SERVER_URL = app.config.get("SERVER_URL", "http://localhost:5000")

CORS(
    app,
    origins=[
        r"https?://([\w-]+\.)?netlify\.app/?.*",
        "https://OFFICIALWEBSITENAME.com",
        "http://localhost:3000/",
        "http://127.0.0.1:3000",
    ],
)

## singleton pattern - YoloService instantiated outside of the endpoint to be reused globally for the server's lifetime
# service = YoloService()


@app.route("/process_image", methods=["POST"])
def process_image():
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "Image URL not provided"}), 400

    service = YoloService()

    predictions = service.process_image_url(image_url)

    response_data = {"predictions": predictions}

    return jsonify(response_data)


@app.route("/image_analysis", methods=["GET"])
def image_analysis():
    generate_image_url = RandomImage()
    image_data = generate_image_url.get_random_image()
    image_url = image_data.get("regular_image_url")
    latitude = image_data.get("latitude")
    longitude = image_data.get("longitude")

    reverse_geocode = Location()
    location_data = reverse_geocode.get_location(image_data)
    location = location_data.get("location")
    new_image_data = {
        "regular_image_url": image_url,
        "latitude": latitude,
        "longitude": longitude,
        "location": location,
    }

    weather = Weather()
    weather_data = weather.get_weather(new_image_data)
    image_data = weather_data
    location = image_data.get("location")
    weather = (image_data.get("daily"), image_data.get("daily_units"))
    latitude = image_data.get("latitude")
    longitude = image_data.get("longitude")
    image_url = image_data.get("regular_image_url")

    service = YoloService()
    predictions = service.process_image_url(image_url)
    image_analysis_data = {"predictions": predictions}

    data_cleanse = CleanUpObjectDetection()
    cleaned_data = data_cleanse.get_analysis_and_clean(image_analysis_data)
    proper_ppe = cleaned_data.get("proper_ppe")
    improper_ppe = cleaned_data.get("improper_ppe")

    final_image_data = {
        "proper_ppe": proper_ppe,
        "improper_ppe": improper_ppe,
        "image_url": image_url,
        "image_location": location,
        "latitude": latitude,
        "longitude": longitude,
        "weather": weather,
    }

    return jsonify(final_image_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
