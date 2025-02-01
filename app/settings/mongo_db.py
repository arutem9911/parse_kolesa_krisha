from contextlib import contextmanager
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from app.settings.config import settings


@contextmanager
def mongo_client():
    client = MongoClient(settings.MONGO_URI)
    try:
        yield client
    finally:
        client.close()


def insert_application_data(response_data, status_code, collection_name):
    with mongo_client() as client:
        mongo_db = client.db_scoring_logs
        collection = mongo_db[collection_name]
        response = jsonable_encoder(response_data)
        data_for_mongo = {
            "task_id": response.get("task_id"),
            "response": response,
            "create_date": datetime.now(),
            "status_code": status_code,
        }
        try:
            collection.insert_one(data_for_mongo)
        except Exception as e:
            raise Exception(f"An error occurred during data insertion: {e}")
