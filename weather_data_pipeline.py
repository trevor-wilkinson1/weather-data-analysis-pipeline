import requests
import json
import datetime
import csv
import os

API_Key = API_Key = "your_real_key_here"

Zip_Codes = ["84321", "84790", "84302", "84101", "84060"]

def get_weather(zip_code):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    parameters = {"zip": f"{zip_code},US", "units": "imperial", "appid": API_Key}

    response = requests.get(url, params=parameters)
    response.raise_for_status()
    return response.json()

def save_results(data, filename ="raw_weather.json"):
    folder_path = os.path.join(os.path.dirname(__file__), "results.json")

    with open(folder_path, "w") as f:
        json.dump(data, f, indent=4)

        print(f"Saved results to {folder_path}")

def append_to_csv(data, filename="weather_data.csv"):
    file_path = os.path.join(os.path.dirname(__file__), filename)

    file_exists = os.path.isfile(file_path) #checking if the CSV exists

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        #write CSV headers only once
        if not file_exists:
            writer.writerow([
                "zip_code", "forecast_timestamp", "temp", "temp_min", "temp_max", 
                "humidity", "conditions"
            ])

        for zip_block in data: #writing the forecast entry
            zip_code = zip_block["zip_code"]

            for entry in zip_block["list"]:
                writer.writerow([
                    zip_code,
                    entry["dt_txt"], entry["main"]["temp"],
                    entry["main"]["temp_min"],
                    entry["main"]["temp_max"],
                    entry["main"]["humidity"],
                    entry["weather"][0]["description"]])

import json
import os
import statistics

def load_weather_data(): #loading results from my joson created in the fetch_weather
    file_path = os.path.join(os.path.dirname(__file__), "results.json")

    with open(file_path, "r") as f:
        return json.load(f)
    
def extract_metrics(data):
    extracted = []
    
    # ChatGPT was used to help generate the function below. 
    for zip_object in data: #changing the sturcture of our JSON into cleaner data
        zip_code = zip_object["zip_code"]

        for entry in zip_object["list"]:
            metrics = {"zip": zip_code,
                "temp": entry["main"]["temp"],
                "temp_min": entry["main"]["temp_min"],
                "temp_max": entry["main"]["temp_max"],
                "humidity": entry["main"]["humidity"],
                "conditions": entry["weather"][0]["description"],
                "timestamp": entry["dt_txt"]}
            extracted.append(metrics)


    return extracted

def business_recommendation(temp, conditions): #business rule recommendations 
    temp = float(temp)
    conditions = conditions.lower()

    if temp >= 75 and "rain" not in conditions: 
        return "Increase staffing - warm weather expected."
    elif "rain" in conditions or "snow" in conditions:
        return "Reduce staffing - bad weather will reduce demand"
    elif temp < 40:
        return "Reduce staffing - cold outside"
    else:
        return "Normal staffing - moderate conditions outside"
    
def analyze(weather_metrics): # performance metrics/analysis and printted summary
    print("\nWEATHER ANALYSIS SUMMARY \n")

    temps = []

    results_summary = []

    for entry in weather_metrics:
        zip_code = entry["zip"]
        temp = entry["temp"]
        temp_min = entry["temp_min"]
        temp_max = entry["temp_max"]
        humidity = entry["humidity"]
        cond = entry["conditions"]

        temps.append(temp)

        recommendation = business_recommendation(temp, cond)

        print(f"ZIP Code: {zip_code}")
        print(f"Current Temp: {temp}F")
        print(f"High: {temp_max}F  Low: {temp_min}F")
        print(f" Humidity: {humidity}%")
        print(f"Conditions: {cond}")
        print(f"Recommendation: {recommendation}\n")

        results_summary.append({"zip_code": zip_code, 
        "temp": temp,
        "high": temp_max,
        "low": temp_min,
        "humidity": humidity,
        "conditions": cond,
        "recommendation": recommendation})

    overall_results = { #extra summary
        "average_temp": round(statistics.mean(temps), 2),
        "highest_temp": round(max(temps), 2),
        "lowest_temp": round(min(temps), 2),
    }

    print("OVERALL SUMMARY")
    print("--------------------")
    print(f"Average Temperature: {overall_results['average_temp']}F")
    print(f"Highest Temperature: {overall_results['highest_temp']}F")
    print(f"Lowest Temperature: {overall_results['lowest_temp']}F")

    return {
        "individual_results": results_summary,
        "overall_summary": overall_results
}



def save_analysis_results(data): #results to json (overwriting)
    file_path = os.path.join(os.path.dirname(__file__), "analysis_results.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated results.json with analysis output")

def main(): #fetching weather data
    all_weather = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for z in Zip_Codes:
        print(f"Fetching weather for Zip {z}")
        weather = get_weather(z)
        weather["zip_code"] = z
        weather["timestamp"] = timestamp
        all_weather.append(weather)

    save_results(all_weather)     
    append_to_csv(all_weather) #appending to csv

    #data analysis
    raw_data = load_weather_data()
    cleaned = extract_metrics(raw_data)
    analysis_results = analyze(cleaned)
    save_analysis_results(analysis_results)

if __name__ == "__main__":
    main()






