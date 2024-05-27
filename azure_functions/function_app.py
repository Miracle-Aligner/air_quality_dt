import logging
import os

import random
import datetime
import azure.functions as func
import requests
from dotenv import load_dotenv
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()


@app.schedule(
    schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False
)
def updateAirData(myTimer: func.TimerRequest) -> None:
    # if myTimer.past_due:
    try:
        load_dotenv()

        adt_url = os.getenv("AZURE_DIGITAL_TWINS_URL")
        credential = DefaultAzureCredential()

        adt_client = DigitalTwinsClient(adt_url, credential)

        query_expression = "SELECT * FROM digitaltwins"
        query_result = adt_client.query_twins(query_expression)

        twins_data = [twin for twin in query_result if "name" in twin]
        for twin in twins_data:
            # api_response = get_air_quality(
            #     twin.get("latitude"), twin.get("longitude")
            # )["data"][-1]

            api_response = get_dummy_air_quality()["data"][-1]

            json_patch_document = [
                {
                    "op": "replace" if "aqi" in twin else "add",
                    "path": "/aqi",
                    "value": api_response["aqi"],
                },
                {
                    "op": "replace" if "co" in twin else "add",
                    "path": "/co",
                    "value": api_response["co"],
                },
                {
                    "op": "replace" if "datetime" in twin else "add",
                    "path": "/datetime",
                    "value": api_response["datetime"],
                },
                {
                    "op": "replace" if "no2" in twin else "add",
                    "path": "/no2",
                    "value": api_response["no2"],
                },
                {
                    "op": "replace" if "o3" in twin else "add",
                    "path": "/o3",
                    "value": api_response["o3"],
                },
                {
                    "op": "replace" if "pm10" in twin else "add",
                    "path": "/pm10",
                    "value": api_response["pm10"],
                },
                {
                    "op": "replace" if "pm25" in twin else "add",
                    "path": "/pm25",
                    "value": api_response["pm25"],
                },
                {
                    "op": "replace" if "so2" in twin else "add",
                    "path": "/so2",
                    "value": api_response["so2"],
                },
            ]
            adt_client.update_digital_twin(twin.get("$dtId"), json_patch_document)

            if is_air_polluted(api_response):
                server = adt_client.get_digital_twin("CityApplicationServer")
                updated_server = [
                    {
                        "op": "replace" if "alertLevel" in server else "add",
                        "path": "/alertLevel",
                        "value": 3,
                    },
                    {
                        "op": "replace" if "lastNotification" in server else "add",
                        "path": "/lastNotification",
                        "value": f"The air of {twin.get('name')} is polluted.",
                    },
                ]
                adt_client.update_digital_twin("CityApplicationServer", updated_server)

    except Exception as e:
        logging.error(f"Failed to fetch or update data: {str(e)}")


def is_air_polluted(factors):
    thresholds = {
        "aqi": 100,  # Air Quality Index normal threshold
        "co": 9,  # Carbon monoxide in mg/m³ for 8-hour exposure
        "no2": 106,  # Nitrogen dioxide in µg/m³ for 1-hour exposure
        "o3": 100,  # Ozone in µg/m³ for 8-hour exposure
        "pm10": 150,  # Particulate matter <= 10 µm in µg/m³ for 24-hour exposure
        "pm25": 35,  # Particulate matter <= 2.5 µm in µg/m³ for 24-hour exposure
        "so2": 75,  # Sulfur dioxide in µg/m³ for 1-hour exposure
    }

    # Iterate through the keys that need to be checked

    for key in ["aqi", "co", "no2", "o3", "pm10", "pm25", "so2"]:
        if key in factors:
            if factors[key] > thresholds[key]:
                # If any factor exceeds the threshold, return True indicating pollution
                return True

    # If no factors exceed their thresholds, return False indicating clean air
    return False


def get_air_quality(lat, lon):
    url = "https://air-quality.p.rapidapi.com/history/airquality"
    querystring = {"lon": lon, "lat": lat}
    headers = {
        "X-RapidAPI-Key": "c7b24345d6mshf47e7d19e8bce96p1a1e04jsn7988f4f59538",
        "X-RapidAPI-Host": "air-quality.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def get_dummy_air_quality():
    current_datetime = datetime.datetime.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d:%H")

    return {
        "data": [
            {
                "aqi": random.randint(
                    0, 100
                ),  # AQI could realistically be between 0 and 300
                "co": random.uniform(0, 10),  # CO level in µg/m³
                "datetime": formatted_datetime,  # Current date and hour
                "no2": random.uniform(5, 150),  # NO2 level in µg/m³
                "o3": random.uniform(10, 120),  # O3 level in µg/m³
                "pm10": random.uniform(0, 200),  # PM10 particulates level in µg/m³
                "pm25": random.uniform(0, 50),  # PM2.5 particulates level in µg/m³
                "so2": random.uniform(0, 75),  # SO2 level in µg/m³
            }
        ]
    }
