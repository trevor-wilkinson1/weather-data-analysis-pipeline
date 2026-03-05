# Weather Data Analysis Pipeline

This project retrieves real-time weather forecast data using the OpenWeather API and performs data analysis to generate operational recommendations.

The program collects weather forecasts for multiple ZIP codes, stores raw data in JSON format, appends historical records to a CSV file, and analyzes temperature, humidity, and weather conditions.

Based on the forecasted weather conditions, the script generates simple business recommendations such as increasing or reducing staffing depending on expected demand.

## Features

- Retrieves weather forecast data using the OpenWeather API
- Stores raw API responses in JSON format
- Appends structured weather data to a CSV file
- Extracts key weather metrics such as temperature, humidity, and conditions
- Performs statistical analysis on collected weather data
- Generates business recommendations based on weather conditions

## Technologies Used

- Python
- REST APIs
- JSON
- CSV
- Basic data analysis

## Files

- `weather_data_pipeline.py` – main script that retrieves and processes weather data
- `results.json` – raw weather data retrieved from the API
- `analysis_results.json` – processed analysis results
- `weather_data.csv` – historical weather records

## How to Run

1. Install required package:

pip install requests

2. Add your OpenWeather API key to the script.

3. Run the program:

python weather_data_pipeline.py
