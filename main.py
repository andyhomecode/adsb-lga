import requests
import time

# API endpoint for ADS-B data
base_url = "https://api.adsb.lol/v2/point"

# Coordinates for Laguardia area (adjust as needed)

lat = 40.6875
lon = -73.9845
radius = 3  # km

# ICAO 3-letter code to Airline Brand Name mapping for LGA
# Example usage:
# flight_icao = "JZA"
# print(f"This flight belongs to: {lga_airline_lookup.get(flight_icao, 'Unknown Airline')}")

lga_airline_lookup = {
    # Mainline Carriers
    "AAL": "American",
    "DAL": "Delta",
    "UAL": "United",
    "JBU": "JetBlue",
    "SWA": "SWest",
    "ACA": "AirCan",
    "NKS": "Spirit",
    "FFT": "Frontier",
    "WJA": "WestJet",
    "POE": "Porter",
    "BMA": "BermudA",

    # Regional Operators (The planes you see on trackers)
    "RPA": "Republic",
    "EDV": "Delta",
    "ENY": "American",
    "PDT": "American",
    "JIA": "American",
    "SKW": "Delta",
    "GJS": "UA/DL",
    "ASH": "United",
    "UCA": "United",
    "JZA": "AirCan",
    "AWI": "United"
}

def fetch_and_display_flights():
    try:
        response = requests.get(f"{base_url}/{lat}/{lon}/{radius}")
        response.raise_for_status()
        data = response.json()
        flights = data.get('ac', [])

        # Filter for commercial flights (A3), altitude ~20k ft, track ~37
        filtered_flights = [
            f for f in flights
            if f.get('category') == 'A3' and
                # True
               1000 <= f.get('alt_geom', 0) <= 5000 
               # 0 <= f.get('nav_heading', 0) <= 90
        ]

        # Sort by latitude descending (north to south)
        sorted_flights = sorted(filtered_flights, key=lambda x: x['lat'], reverse=True)

        print(f"Fetched {len(flights)} total flights, {len(sorted_flights)} filtered.")
        for flight in sorted_flights:
            flight_id = flight.get('flight', 'Unknown').strip()
            hex_id = flight.get('hex', 'N/A')
            alt_geom = flight.get('alt_geom', 'N/A')
            nav_heading = flight.get('nav_heading', 'N/A')
            lat_f = flight.get('lat', 'N/A')
            lon_f = flight.get('lon', 'N/A')
            icao_code = flight_id[:3] if len(flight_id) >= 3 else flight_id
            airline_name = lga_airline_lookup.get(icao_code, 'Unknown Airline')
            print(f"Flight: {flight_id} ({airline_name}) ({hex_id}), Alt: {alt_geom} ft, heading: {nav_heading}, Lat: {lat_f}, Lon: {lon_f}")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_display_flights()
        time.sleep(20)