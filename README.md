# ADS-B LGA Flights

This Python project fetches ADS-B data from api.adsb.lol and filters for commercial flights (category A3) on approach to Laguardia airport. It uses a smaller bounding box around Laguardia (lat: 40.6875, lon: -73.9845, radius: 5 km) to focus on approaching flights. It displays flights with altitude around 20,000 ft and track around 37 degrees, ranked by latitude (north to south).

## Requirements

- Python 3.x
- requests library

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script:
```
python main.py
```

The script will fetch data every 15 seconds and print the filtered flights.

## Configuration

Adjust the `lat`, `lon`, and `radius` in `main.py` to change the area of interest.
Modify the filters in `fetch_and_display_flights()` for different criteria.