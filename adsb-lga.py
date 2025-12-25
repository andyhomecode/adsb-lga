import requests
import time
import argparse
import re

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

def get_route_origin(callsign):
    """
    Fetches the route origin for a given callsign using the ADS-B API.
    
    Args:
        callsign (str): The flight callsign (e.g., "RPA4695")
    
    Returns:
        tuple: (origin_iata, dest_iata, origin_name) or (None, None, None) if not found or error
    """
    url = "https://api.adsb.lol/api/0/routeset"
    payload = {
        "planes": [
            {
                "callsign": callsign,
                "lat": 0,
                "lng": 0
            }
        ]
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            route = data[0]
            airports = route.get('_airports', [])
            if len(airports) >= 1:
                origin = airports[0]
                origin_iata = origin.get('iata')
                origin_name = origin.get('name')
                if origin_name:
                    origin_name = re.sub(r'\b(?:International|National|Ronald Reagan|Bergstrom|Douglas|Hilton Head|Hartsfield Jackson|Airport|Regional|Municipal|Field)\b', '', origin_name, flags=re.IGNORECASE).strip()
                    origin_name = ' '.join(origin_name.split())  # Normalize spaces
                dest_iata = None
                if len(airports) >= 2:
                    dest = airports[1]
                    dest_iata = dest.get('iata')
                return origin_iata, dest_iata, origin_name
        return None, None, None
    except requests.RequestException:
        return None, None, None

def get_flights():
    try:
        response = requests.get(f"{base_url}/{lat}/{lon}/{radius}")
        response.raise_for_status()
        data = response.json()
        flights = data.get('ac', [])

        # Filter for commercial flights (A3), low and heading north (not all send that)
        filtered_flights = [
            f for f in flights
            if f.get('category') == 'A3' and
                # True
               1000 <= f.get('alt_geom', 0) <= 5000 
               # 0 <= f.get('nav_heading', 0) <= 90
        ]

        # Sort by latitude descending (north to south)
        sorted_flights = sorted(filtered_flights, key=lambda x: x['lat'], reverse=True)

        # Add route origin info to each flight
        for flight in sorted_flights:
            flight_id = flight.get('flight', '').strip()
            if flight_id:
                origin_iata, dest_iata, origin_name = get_route_origin(flight_id)
                flight['origin_iata'] = origin_iata
                flight['dest_iata'] = dest_iata
                flight['origin_name'] = origin_name
            else:
                flight['origin_iata'] = None
                flight['dest_iata'] = None
                flight['origin_name'] = None

        return flights, sorted_flights
    except requests.RequestException:
        return [], []

def fetch_and_display_flights():
    flights, sorted_flights = get_flights()

    print(f"Fetched {len(flights)} total flights, {len(sorted_flights)} filtered.")
    for flight in sorted_flights:
        flight_id = flight.get('flight', 'Unknown').strip()
        hex_id = flight.get('hex', 'N/A')
        alt_geom = flight.get('alt_geom', 'N/A')
        nav_heading = flight.get('nav_heading', 'N/A')
        lat_f = flight.get('lat', 'N/A')
        lon_f = flight.get('lon', 'N/A')
        icao_code = flight_id[:3] if len(flight_id) >= 3 else flight_id
        airline_name = lga_airline_lookup.get(icao_code, 'Unknown')
        origin_iata = flight.get('origin_iata') or ''
        origin_name = flight.get('origin_name') or ''
        print(f"Flight: {flight_id} ({airline_name}) ({hex_id}), Alt: {alt_geom} ft, heading: {nav_heading}, Lat: {lat_f}, Lon: {lon_f}, Origin: {origin_iata} ({origin_name})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flight', action='store_true', help='Output the flight ID of the top sorted entry and exit')
    parser.add_argument('--airline', action='store_true', help='Output the airline name of the top sorted entry and exit')
    parser.add_argument('--route', action='store_true', help='Output the route info of the top sorted entry and exit')
    args = parser.parse_args()

    if args.flight or args.airline or args.route:
        flights, sorted_flights = get_flights()
        if sorted_flights:
            flight = sorted_flights[0]
            flight_id = flight.get('flight', '???000').strip()
            icao_code = flight_id[:3] if len(flight_id) >= 3 else flight_id
            airline_name = lga_airline_lookup.get(icao_code, 'Unknown')
            if args.flight:
                print(flight_id)
            elif args.airline:
                print(airline_name)
            elif args.route:
                origin_iata = flight.get('origin_iata')
                origin_name = flight.get('origin_name')
                if origin_iata and origin_name:
                    print(f"{origin_iata}, {origin_name}")
                else:
                    print("")
    else:
        while True:
            fetch_and_display_flights()
            time.sleep(20)