from datetime import datetime, timedelta
import pandas as pd
from meteostat import Stations, Daily

# List of major US cities with their coordinates
cities = [
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Houston", "latitude": 29.7604, "longitude": -95.3698},
    {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740}
    # Add more cities as needed
]

end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

# DataFrame to hold the aggregated data
all_data = pd.DataFrame()

for city in cities:
    latitude = city["latitude"]
    longitude = city["longitude"]
    city_name = city["name"]
    
    # Find the nearest weather station
    stations = Stations()
    station = stations.nearby(latitude, longitude).fetch(1)
    
    # Check if any stations were found
    if station.empty:
        print(f"No weather stations found near {city_name}.")
        continue
    
    station_id = station.index[0]
    print(f"Using weather station: {station_id} for {city_name}")

    # Fetch daily weather data for the last three years
    data = Daily(station_id, start_date, end_date)
    data = data.fetch()
    
    # Check if any data was returned
    if data.empty:
        print(f"No weather data found for {city_name} for the specified date range.")
        continue
    
    # Add city name to the data
    data["city"] = city_name
    
    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, data])

# Save the aggregated data to a CSV file
all_data.to_csv('us_weather_data_last_3_years.csv')
print("Aggregated weather data saved to 'us_weather_data_last_3_years.csv'.")

# Display the aggregated data
print(all_data)
