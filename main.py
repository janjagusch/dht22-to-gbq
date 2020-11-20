"""
Reads temperature and humidty from a DHT22 sensor and stores the results in BigQuery.
"""

import os
from datetime import datetime

import Adafruit_DHT
from dotenv import load_dotenv
from google.cloud import bigquery


class DHT22Sensor:
    """
    DHT22 sensor class that can take measurements.
    """

    _sensor = Adafruit_DHT.DHT22

    def __init__(self, sensor_id, sensor_pin):
        self._sensor_id = sensor_id
        self._sensor_pin = sensor_pin

    @classmethod
    def from_env(cls):
        """
        Creates an instance of DHT22Sensor from environment variables.
        """
        return cls(os.environ["DHT22_SENSOR_ID"], os.environ["DHT22_SENSOR_PIN"])

    def _measurement(self):
        return Adafruit_DHT.read_retry(self._sensor, self._sensor_pin)

    def measurement(self):
        """
        Takes a measurement.
        """
        measurement_ = {}
        measurement_["sensor_id"] = self._sensor_id
        measurement_["requested_at"] = datetime.now()
        measurement_["humidity"], measurement_["temperature"] = self._measurement()
        return measurement_


def _gbq_setup():
    project_id = os.environ["GBQ_PROJECT_ID"]
    dataset_id = os.environ["GBQ_DATASET_ID"]
    table_id = os.environ["GBQ_TABLE_ID"]
    client = bigquery.Client()
    dataset = bigquery.dataset.DatasetReference.from_string(
        f"{project_id}.{dataset_id}"
    )
    table = client.get_table(dataset.table(table_id))
    return client, table


def _gbq_insert(measurement, client, table):
    errors = client.insert_rows(table, [measurement])
    if errors:
        raise RuntimeError(errors)


if __name__ == "__main__":
    load_dotenv()
    client, table = _gbq_setup()
    sensor = DHT22Sensor.from_env()
    measurement = sensor.measurement()
    print(measurement)
    _gbq_insert(measurement, client, table)
