# dht22-to-gbq

Retrieving data from a DHT22 temperature and humidity sensor and sending it to Google BigQuery. 🌞

## Getting Started

### Requirements

Install the dependencies in `requirements.txt` and activate the virtual environment.

### Google Cloud Authentification

Your application needs to be authentificated against Google Cloud. We recommend [passing credentials via environment variable](https://cloud.google.com/docs/authentication/production#passing_variable).

### BigQuery Table

You will need a BigQuery table with the following schema

```yaml
- name: sensor_id
  type: STRING
  mode: REQUIRED
- name: requested_at
  type: TIMESTAMP
  mode: REQUIRED
- name: temperature
  type: FLOAT
  mode: NULLABLE
- name: humidity
  type: FLOAT
  mode: NULLABLE
```

### Environment Variables

Create an `.env` file (`cp .env.example .env`) and fill in the following information:

* `DHT22_SENSOR_ID`: The ID of the sensor (appears in BigQuery)
* `DHT22_SENSOR_PIN`: The GPIO pin the sensor is connected to.
* `GBQ_PROJECT_ID`: The ID of your Google Cloud project, where your BigQuery dataset resides.
* `GBQ_DATASET_ID`: The ID of your BigQuery dataset, where your table resides.
* `GBQ_TABLE_ID`: The ID of the table, where your measurements should be stored.

## Running the Application

From your virtual environment, execute:

```sh
python3 main.py
```

### Running as Crontab

A simple crontab that runs every 5 minutes could look somewhat like this:

```sh
*/5 * * * * /usr/bin/env bash -c 'cd $HOME/path-to-your-application && source .venv/bin/activate && python3 main.py > .log 2>&1' > /dev/null 2>&1
```
