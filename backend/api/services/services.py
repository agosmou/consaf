from api.models.models import YOLOv5Model
import requests
from configs.configs import Config

LOS_ANGELES_LAT = 34.006181
LOS_ANGELES_LON = -118.497065


class YoloService:
    def __init__(self):
        self.cv = YOLOv5Model()

    def process_image_url(self, image_url):
        # Performs inference on the image URL
        # image will be resized to 640 x 640. Other options are: 320, 416, 512
        # augmentation set to true will create more accurate model because it will create variations of the image with changes in lighting, angles, size. It is more compute-intensive.
        results = self.cv.model(image_url, augment=True)

        # Get the detection bounding boxes, scores, and categories
        # parse results
        predictions = results.pred[0]
        boxes = predictions[:, :4]  # x1, y1, x2, y2
        scores = predictions[:, 4]
        categories = predictions[:, 5]

        # Gets the possible class labels as a dictionary for detected objects
        class_labels = self.cv.model.names

        # creates a list of dictionaries of predictions. It will contain the bounding boxes, the categories, and confidence score
        processed_predictions = []

        # iterates through the boxes, scores, and categories
        for box, score, category in zip(boxes, scores, categories):
            # get value by converting the category to int, so we can use it as a key for the dictionary and get the value as the variable class_label
            class_label = class_labels[int(category)]

            # create the dictionary
            prediction = {
                # convert tensor array to list to create bounding box
                "box": box.tolist(),
                # convert score, which is a tensor array element, to float
                "score": score.item(),
                # set category to the class_label variable
                "category": class_label,
            }
            # append the dictionary to the list of processed_predictions
            processed_predictions.append(prediction)

        return processed_predictions


class RandomImage:
    def get_random_image(self):
        unsplash_key = Config.UNSPLASH_ACCESS_KEY
        search_query = "construction worker"
        unsplash_api_endpoint = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {unsplash_key}"}
        params = {"query": search_query, "count": 1}

        try:
            response = requests.get(
                unsplash_api_endpoint, headers=headers, params=params, timeout=5
            )

            response.raise_for_status()

            data = response.json()

            image_data = data[0]
            regular_image_url = image_data.get("urls", {}).get("regular")
            latitude = (
                image_data.get("location", {}).get("position", {}).get("latitude", {})
            )
            longitude = (
                image_data.get("location", {}).get("position", {}).get("longitude", {})
            )

            if longitude == None:
                longitude = LOS_ANGELES_LON

            if latitude == None:
                latitude = LOS_ANGELES_LAT

            result = {
                "latitude": latitude,
                "longitude": longitude,
                "regular_image_url": regular_image_url,
            }

            return result

        except requests.exceptions.RequestException:
            return {"error": "Error fetching image"}


class Location:
    def get_location(self, image_data):
        latitude = image_data.get("latitude")
        longitude = image_data.get("longitude")

        if longitude == LOS_ANGELES_LON and latitude == LOS_ANGELES_LAT:
            return {"location": "Los Angeles, California, United States"}

        api_endpoint = f"https://geocode.maps.co/reverse?lat={latitude}&lon={longitude}"

        try:
            response = requests.get(api_endpoint, timeout=5)

            response.raise_for_status()

            data = response.json()

            location_name = data.get("display_name", {})

            return {"location": location_name}

        except requests.exceptions.RequestException:
            return {"error": "Error fetching location"}


class Weather:
    def get_weather(self, new_image_data):
        latitude = new_image_data.get("latitude")
        longitude = new_image_data.get("longitude")

        api_endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&forecast_days=1"

        try:
            response = requests.get(api_endpoint, timeout=5)

            response.raise_for_status()

            data = response.json()

            data["location"] = new_image_data.get("location")
            data["regular_image_url"] = new_image_data.get("regular_image_url")

            return data

        except requests.exceptions.RequestException:
            return {"error": "Error fetching weather"}


class CleanUpObjectDetection:
    def get_analysis_and_clean(self, image_analysis_data):
        """the object detection models detects many labels so we only want to return the relevant safety labels"""

        predictions = image_analysis_data.get("predictions")

        if len(predictions) == 0:
            return {"message": "Nothing to detect"}

        proper_ppe = ["Hardhat", "Safety Vest", "Safety Shoes", "Safety Net"]

        improper_ppe = [
            "NO-Hardhat",
            "NO-Safety Vest",
        ]

        proper_ppe_list = []
        improper_ppe_list = []

        for i in range(len(predictions)):
            category_detected = predictions[i].get("category")
            if category_detected in proper_ppe:
                proper_ppe_list.append(category_detected)
            elif category_detected in improper_ppe:
                improper_ppe_list.append(category_detected)

        result = {"proper_ppe": proper_ppe_list, "improper_ppe": improper_ppe_list}

        return result
