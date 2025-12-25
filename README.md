# ADS-B LGA Flights

This Python project fetches ADS-B data from api.adsb.lol and filters for commercial flights (category A3) on approach to Laguardia airport. It uses a smaller bounding box around Laguardia (lat: 40.6875, lon: -73.9845, radius: 3 km) to focus on approaching flights. It displays flights with altitude around 20,000 ft and track around 37 degrees, ranked by latitude (north to south).

## Requirements

- Python 3.x
- requests library
- figlet (for the display script)

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Continuous Monitoring
Run the script for continuous monitoring:
```
python adsb-lga.py
```
or use the VS Code task "Run ADS-B Monitor".

The script will fetch data every 20 seconds and print the filtered flights.

### Single Output for Piping
For piping into other programs, use command-line options:
- `--flight`: Output only the flight ID of the top sorted entry and exit.
- `--airline`: Output only the airline name of the top sorted entry and exit.

Examples:
```
python adsb-lga.py --flight
python adsb-lga.py --airline
```

### Display Script with Figlet
Run the shell script `adsb-lga.sh` for a looping display with ASCII art:
```
./adsb-lga.sh
```
This script alternates between displaying the flight ID and airline name using `figlet`, with a 5-second pause between each. If no data is available, it shows a progress bar of asterisks (*) until data appears.

## Configuration

Adjust the `lat`, `lon`, and `radius` in `adsb-lga.py` to change the area of interest.
Modify the filters in `get_flights()` for different criteria.