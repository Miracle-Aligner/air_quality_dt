import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

from pymongo.server_api import ServerApi


class AirQualityManager:
    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = self.client["air_quality_db"]
        self.collection = self.db["air_quality_data"]

    def create_or_update_record(self, name, data):
        """Create a new air quality record or update if it exists."""

        new_data = {
            "aqi": data.get("aqi", 0),
            "co": data.get("co", 0),
            "datetime": data.get("datetime", None),
            "no2": data.get("no2", 0),
            "o3": data.get("o3", 0),
            "pm10": data.get("pm10", 0),
            "pm25": data.get("pm25", 0),
            "so2": data.get("so2", 0),
        }

        result = self.collection.update_one(
            {"name": name}, {"$push": {"data": new_data}}, upsert=True
        )

        if result.upserted_id or result.modified_count:
            print(f"Record created or updated for {name}.")

            return True

        else:
            print(f"Failed to create or update record for {name}.")

            return False

    def read_data(self, name, field):
        """Retrieve historical data for a specific field by entity name, sorted by datetime."""
        record = self.collection.aggregate(
            [
                {"$match": {"name": name}},
                {
                    "$project": {
                        "data": {
                            "$filter": {
                                "input": "$data",
                                "as": "item",
                                "cond": {"$ifNull": ["$$item." + field, False]},
                            }
                        },
                        "_id": 0,
                    }
                },
                {"$unwind": "$data"},
                {"$sort": {"data.datetime": 1}},
                {"$group": {"_id": None, "data": {"$push": "$data"}}},
            ]
        )

        # Convert the cursor to a list and extract data

        sorted_data = list(record)

        if sorted_data and "data" in sorted_data[0]:
            return [
                {field: entry[field], "datetime": entry["datetime"]}
                for entry in sorted_data[0]["data"]
            ]

        else:
            print(f"No record found with name {name}.")

            return []

    def get_all_indices_for_name(self, name):
        """Retrieve all data entries for a specific record by name, sorted by datetime."""

        record = self.collection.aggregate(
            [
                {"$match": {"name": name}},
                {"$project": {"data": 1, "_id": 0}},
                {"$unwind": "$data"},
                {"$sort": {"data.datetime": 1}},
                {"$group": {"_id": None, "data": {"$push": "$data"}}},
            ]
        )

        # Convert the cursor to a list and extract data

        sorted_data = list(record)

        if sorted_data and "data" in sorted_data[0]:
            return sorted_data[0]["data"]

        else:
            print(f"No data found for name {name}.")

            return []

    def delete_record(self, name):
        """Delete a record by name."""

        result = self.collection.delete_one({"name": name})

        if result.deleted_count:
            print(f"Record with name {name} deleted.")

            return True

        else:
            print(f"No record found with name {name}.")

            return False

    def get_all_records(self):
        """Retrieve all records with their data."""
        records = self.collection.find({}, {"_id": 0, "name": 1, "data": 1})

        return list(records)


# Example usage
if __name__ == "__main__":
    load_dotenv()

    uri = os.getenv("MONGO_URI")
    manager = AirQualityManager(uri)

    # Create or update a record
    data = {
        "aqi": 85,
        "co": 0.3,
        "no2": 45,
        "o3": 60,
        "pm10": 150,
        "pm25": 25,
        "so2": 10,
    }

    manager.create_or_update_record("CityA", data)

    # Read specific data
    aqi_data = manager.read_data("CityA", "aqi")
    print(aqi_data)

    # Get all records
    all_records = manager.get_all_records()

    print(all_records)

    # Delete a record
    manager.delete_record("CityA")
