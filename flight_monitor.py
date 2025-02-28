import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from the environment file
load_dotenv('environment.env')

# Fetch parameters from environment variables
BASE_URL = os.environ.get("BASE_URL")
FROM_ENTITY_ID = os.environ.get("FROM_ENTITY_ID")
TO_ENTITY_ID = os.environ.get("TO_ENTITY_ID")
DEPART_DATE = os.environ.get("DEPART_DATE")
RETURN_DATE = os.environ.get("RETURN_DATE")
MARKET = os.environ.get("MARKET")
LOCALE = os.environ.get("LOCALE")
CURRENCY = os.environ.get("CURRENCY")
ADULTS = os.environ.get("ADULTS")
INCLUDE_ORIGIN_NEARBY_AIRPORTS = os.environ.get("INCLUDE_ORIGIN_NEARBY_AIRPORTS")
SORT = os.environ.get("SORT")
STOPS = os.environ.get("STOPS")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")

# Construct the API URL with query parameters
url = (
    f"{BASE_URL}?"
    f"fromEntityId={FROM_ENTITY_ID}&toEntityId={TO_ENTITY_ID}"
    f"&departDate={DEPART_DATE}&returnDate={RETURN_DATE}"
    f"&market={MARKET}&locale={LOCALE}&currency={CURRENCY}"
    f"&adults={ADULTS}&includeOriginNearbyAirports={INCLUDE_ORIGIN_NEARBY_AIRPORTS}"
    f"&sort={SORT}&stops={STOPS}"
)

# Set up the request headers with your API credentials
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
}


def format_datetime(dt_str):
    """Convert an ISO datetime string to a formatted string."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception as e:
        return dt_str


def fetch_flight_data():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching data:", response.status_code, response.text)
        return None
    return response.json()


def get_top_cheapest_flights(data, top_n=3):
    itineraries = data.get("data", {}).get("itineraries", [])
    if not itineraries:
        print("No itineraries found in the response.")
        return []
    sorted_itineraries = sorted(itineraries, key=lambda x: x.get("price", {}).get("raw", float('inf')))
    return sorted_itineraries[:top_n]


def print_flights(flights):
    for idx, itinerary in enumerate(flights, 1):
        price = itinerary.get("price", {}).get("formatted", "N/A")
        legs = itinerary.get("legs", [])
        airline = "Unknown"
        outbound_departure = "N/A"
        outbound_arrival = "N/A"
        inbound_departure = "N/A"
        inbound_arrival = "N/A"
        # Optional: Terminal information if available
        outbound_dep_terminal = None
        outbound_arr_terminal = None
        inbound_dep_terminal = None
        inbound_arr_terminal = None

        if legs:
            # First leg is assumed as the outbound flight
            first_leg = legs[0]
            marketing = first_leg.get("carriers", {}).get("marketing", [])
            if marketing:
                airline = marketing[0].get("name", "Unknown")
            outbound_departure = first_leg.get("departure", "N/A")
            outbound_arrival = first_leg.get("arrival", "N/A")
            outbound_dep_terminal = first_leg.get("departureTerminal")
            outbound_arr_terminal = first_leg.get("arrivalTerminal")

            # If a second leg exists, assume it's the inbound flight
            if len(legs) > 1:
                second_leg = legs[1]
                inbound_departure = second_leg.get("departure", "N/A")
                inbound_arrival = second_leg.get("arrival", "N/A")
                inbound_dep_terminal = second_leg.get("departureTerminal")
                inbound_arr_terminal = second_leg.get("arrivalTerminal")

        formatted_outbound_departure = format_datetime(
            outbound_departure) if outbound_departure != "N/A" else outbound_departure
        formatted_outbound_arrival = format_datetime(
            outbound_arrival) if outbound_arrival != "N/A" else outbound_arrival
        formatted_inbound_departure = format_datetime(
            inbound_departure) if inbound_departure != "N/A" else inbound_departure
        formatted_inbound_arrival = format_datetime(inbound_arrival) if inbound_arrival != "N/A" else inbound_arrival

        print(f"{idx}. Airline: {airline}, Price: {price}")
        outbound_line = f"   Outbound: {formatted_outbound_departure} -> {formatted_outbound_arrival}"
        if outbound_dep_terminal or outbound_arr_terminal:
            outbound_line += f" (Terminal: {outbound_dep_terminal or 'N/A'} -> {outbound_arr_terminal or 'N/A'})"
        print(outbound_line)
        if len(legs) > 1:
            inbound_line = f"   Inbound: {formatted_inbound_departure} -> {formatted_inbound_arrival}"
            if inbound_dep_terminal or inbound_arr_terminal:
                inbound_line += f" (Terminal: {inbound_dep_terminal or 'N/A'} -> {inbound_arr_terminal or 'N/A'})"
            print(inbound_line)


if __name__ == "__main__":
    data = fetch_flight_data()
    if data:
        top_flights = get_top_cheapest_flights(data, top_n=3)
        print("Top 3 Cheapest Direct Flights:")
        print_flights(top_flights)
