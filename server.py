from flask import Flask, jsonify, render_template
from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

adt_url = os.getenv("AZURE_DIGITAL_TWINS_URL")
credential = DefaultAzureCredential()

adt_client = DigitalTwinsClient(adt_url, credential)
# Mock data - In a real scenario, you would fetch this data from Azure Digital Twins

twins_data = [
    {"name": "Location A", "latitude": 50.4501, "longitude": 30.5234},
    {"name": "Location B", "latitude": 50.4547, "longitude": 30.5238},
]


@app.route("/")
def home():
    return render_template("map.html")


@app.route("/api/twins")
def get_twins():
    try:
        query_expression = "SELECT * FROM digitaltwins"
        query_result = adt_client.query_twins(query_expression)
        twins_data = [twin for twin in query_result]
        print(twins_data)

        return jsonify(twins_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sensors")
def get_sensors():
    try:
        query_expression = "SELECT * FROM digitaltwins"
        query_result = adt_client.query_twins(query_expression)
        twins_data = [twin for twin in query_result if "name" in twin]

        print(twins_data)
        return jsonify(twins_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
