from flask import Flask, jsonify, render_template
from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from dotenv import load_dotenv
import os
import logging
from database import AirQualityManager

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

adt_url = os.getenv("AZURE_DIGITAL_TWINS_URL")
credential = DefaultAzureCredential()

adt_client = DigitalTwinsClient(adt_url, credential)

mongo_uri = os.getenv("MONGO_URI")
db_manager = AirQualityManager(mongo_uri)

@app.route("/")
def home():
    return render_template("map.html")


@app.route("/api/twins")
def get_twins():
    try:
        query_expression = "SELECT * FROM digitaltwins"
        query_result = adt_client.query_twins(query_expression)
        twins_data = [twin for twin in query_result]

        return jsonify(twins_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sensors")
def get_sensors():
    try:
        query_expression = "SELECT * FROM digitaltwins"
        query_result = adt_client.query_twins(query_expression)
        twins_data = [twin for twin in query_result if "name" in twin]

        return jsonify(twins_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/indices/<string:district_name>")
def get_indices(district_name):
    return db_manager.get_all_indices_for_name(district_name)

@app.route("/api/indices/<string:district_name>/<string:index_name>")
def get_indice_for_district(district_name, index_name):
    return db_manager.read_data(district_name, index_name)

if __name__ == "__main__":
    app.run(debug=True)
