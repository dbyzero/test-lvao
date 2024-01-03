from retry import retry
import requests
import re
from math import radians, sin, cos, sqrt, atan2

def transform_string(input_string):
    # Remove special characters
    input_string = re.sub(r'[^a-zA-Z0-9\s]', '+', input_string)
    
    # Replace spaces with '+'
    input_string = input_string.replace(' ', '+')
    
    # Convert the string to lowercase
    return input_string.lower()
    

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    if lat1 is None:
        return None
    if lat2 is None:
        return None
    if lon1 is None:
        return None
    if lon2 is None:
        return None
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Radius of the Earth in kilometers
    R = 6371.0

    # Calculate differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

@retry(exceptions=requests.HTTPError, tries=3, delay=2)
def call_api_address_gouv(a1,a2,zip,city):
    url = f"https://api-adresse.data.gouv.fr/search/?q={transform_string(a1)}+{transform_string(a2)}+{transform_string(zip)}+{transform_string(city)}"
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()