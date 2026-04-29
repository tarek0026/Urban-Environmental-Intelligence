import requests
import pandas as pd
import time



api_key = "e1f10a1e78da46f5b10a1e78da96f525"

# New York
base_url = "https://api.weather.com/v1/location/KJRB:9:US/observations/historical.json"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.wunderground.com/",
    "Origin": "https://www.wunderground.com"
}

all_data = []

days_in_month = {
    1:31, 2:28, 3:31, 4:30, 5:31, 6:30,
    7:31, 8:31, 9:30, 10:31, 11:30, 12:31
}

for month in range(1, 13):
    start_date = f"2023{month:02d}01"
    end_date   = f"2023{month:02d}{days_in_month[month]}"

    params = {
        "apiKey": api_key,
        "units": "m",
        "startDate": start_date,
        "endDate": end_date
    }

    res = requests.get(base_url, params=params, headers=headers)

    if res.status_code != 200:
        print(f"Error in month {month}")
        continue

    data = res.json()

    for obs in data.get("observations", []):
        all_data.append({
            "Date": obs.get("valid_time_gmt"),
            "Temperature": obs.get("temp"),
            "Humidity": obs.get("rh"),
            "Wind_speed": obs.get("wspd"),
            "Pressure": obs.get("pressure")
        })

    time.sleep(1)

df = pd.DataFrame(all_data)

df["Date"] = pd.to_datetime(df["Date"], unit="s")
df["Date"] = df["Date"].dt.floor("D")

df = df.groupby("Date").agg({
    "Temperature": ["mean", "max"],
    "Humidity": "mean",
    "Wind_speed": "mean",
    "Pressure": "mean"
}).reset_index()

# flatten columns
df.columns = [
    "Date",
    "Temperature_mean",
    "Temperature_max",
    "Humidity",
    "Wind_speed",
    "Pressure"
]

df["City"] = "New York"

df.to_csv("weather_newyork_2023.csv", index=False)

print("Done New York ✅")