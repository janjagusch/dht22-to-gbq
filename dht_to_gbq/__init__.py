"""
Requests humidty and temperature data from a DHT22 sensor and inserts it into BigQuery.
"""

import os
import time
from datetime import datetime

import Adafruit_DHT
from google.cloud import bigquery

_SENSOR = Adafruit_DHT.DHT22
_CLIENT = bigquery.Client()


def _dht_data(sensor_id, sensor_pin):
    """
    Returns a tuple (humidity, temperature) from sensor.
    """
    dht_data = {}
    dht_data["sensor_id"] = sensor_id
    dht_data["requested_at"] = datetime.now()
    dht_data["humidity"], dht_data["temperature"] = Adafruit_DHT.read_retry(
        _SENSOR, sensor_pin
    )
    return dht_data


def _gbq_insert(dht_data, project_id, dataset_id, table_id):
    """
    Inserts dht data into BigQuery.
    """

    def _table(project_id, dataset_id, table_id):
        dataset = bigquery.dataset.DatasetReference.from_string(
            f"{project_id}.{dataset_id}"
        )
        return _CLIENT.get_table(dataset.table(table_id))

    dht_data["inserted_at"] = datetime.now()
    errors = _CLIENT.insert_rows(_table(project_id, dataset_id, table_id), [dht_data])
    if errors:
        raise RuntimeError(errors)


def main():
    """
    Requests humidty and temperature data from a DHT22 sensor and inserts it into BigQuery.
    """
    sensor_id = int(os.environ.get("DHT_SENSOR_ID", 1))
    sensor_pin = int(os.environ["DHT_SENSOR_PIN"])
    gbq_insert = bool(os.environ.get("DHT_GBQ_INSERT", False))

    dht_data = _dht_data(sensor_id, sensor_pin)
    print(dht_data)

    if gbq_insert:
        project_id = os.environ["DHT_GBQ_PROJECT_ID"]
        dataset_id = os.environ["DHT_GBQ_DATASET_ID"]
        table_id = os.environ["DHT_GBQ_TABLE_ID"]
        _gbq_insert(dht_data, project_id, dataset_id, table_id)
