#!/usr/bin/env python3
"""
Air Quality Data Scraper using Open-Meteo API
Free, no API key required, global coverage for 2023
"""



# 
# PM2.5 (Particulate Matter 2.5) refers to very small airborne particles with a diameter of 2.5 micrometers or less.
# These particles come from sources like:
# Vehicle missions
# Industrial processes
# Burning fuels and waste
# Dust and pollution
# Because of their tiny size, PM2.5 particles can penetrate deep into the lungs and even enter the bloodstream, making them harmful to human health.
# They are measured in:
# micrograms per cubic meter (µg/m³)
# PM2.5 is one of the most important indicators of air quality:
# Higher values → worse air pollution
# Lower values → cleaner air
# It is also a key component used in calculating the Air Quality Index (AQI).




import requests
import csv
import io
from datetime import datetime, timedelta
import time

CITY_COORDS = {
    "Cairo": (30.0444, 31.2357),
    "Dubai": (25.2048, 55.2708),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Tokyo": (35.6762, 139.6503),
    "Paris": (48.8566, 2.3522),
    "Nairobi": (-1.2921, 36.8219)
}

AQ_PARAMS = [
    "pm10",
    "pm2_5", 
    "ozone",
    "nitrogen_dioxide",
    "carbon_monoxide",
    "sulphur_dioxide"
]

def get_air_quality(lat, lon, start_date, end_date):
    """Fetch air quality data from Open-Meteo API"""
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(AQ_PARAMS),
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
    
    return None

def parse_hourly_to_daily(data):
    """Convert hourly data to daily averages"""
    if not data or "hourly" not in data:
        return []
    
    hourly = data["hourly"]
    times = hourly.get("time", [])
    daily_data = {}
    
    for param in AQ_PARAMS:
        values = hourly.get(param, [])
        if not values:
            continue
            
        for i, t in enumerate(times):
            day = t[:10]  # YYYY-MM-DD
            val = values[i]
            
            if day not in daily_data:
                daily_data[day] = {}
            
            if val is not None:
                if param not in daily_data[day]:
                    daily_data[day][param] = []
                daily_data[day][param].append(val)
    
    results = []
    for day in sorted(daily_data.keys()):
        row = {"date": day}
        for param in AQ_PARAMS:
            if param in daily_data[day] and daily_data[day][param]:
                vals = [v for v in daily_data[day][param] if v is not None]
                if vals:
                    row[param] = sum(vals) / len(vals)
                else:
                    row[param] = None
            else:
                row[param] = None
        results.append(row)
    
    return results

def main():
    print("=" * 60)
    print("Air Quality Data Scraper - Open-Meteo API")
    print("=" * 60)
    
    all_data = []
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    for city, (lat, lon) in CITY_COORDS.items():
        print(f"\nFetching {city} ({lat}, {lon})...")
        
        data = get_air_quality(lat, lon, start_date, end_date)
        
        if data:
            daily = parse_hourly_to_daily(data)
            print(f"  Got {len(daily)} daily records")
            
            for row in daily:
                all_data.append({
                    "City": city,
                    "Date": row["date"],
                    "PM2.5": row.get("pm2_5"),
                    "PM10": row.get("pm10"),
                    "O3": row.get("ozone"),
                    "NO2": row.get("nitrogen_dioxide"),
                    "CO": row.get("carbon_monoxide"),
                    "SO2": row.get("sulphur_dioxide")
                })
        else:
            print(f"  Failed to get data for {city}")
        
        time.sleep(1)  # Rate limiting
    
    print(f"\nTotal records: {len(all_data)}")
    
    if all_data:
        output_file = "...data/raw/air_quality_2023.csv"
        
        fieldnames = ["City", "Date", "PM2.5", "PM10", "O3", "NO2", "CO", "SO2"]
        
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"\nSaved to: {output_file}")
        
        print("\nSample data:")
        for row in all_data[:5]:
            print(row)

if __name__ == "__main__":
    main()