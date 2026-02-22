# Make a request to the following URL
# URL: https://snap-finder-api.onrender.com/
# Docs: {"message":"SNAP Retailer Locator API","docs":"/docs","health":"/health","closest_retailers":"/retailers/closest?lat=<lat>&lon=<lon>&k=10 or ?zip_code=<zip>&k=10"}

import requests
# Write a function to get the closest SNAP stores to a given latitude and longitude
def get_closest_snap_stores(lat, lon, k=10):
    url = f"https://snap-finder-api.onrender.com/retailers/closest?lat={lat}&lon={lon}&k={k}"
    response = requests.get(url)
    return response.json()

# Write a function to get the closest SNAP stores to a given zip code
def get_closest_snap_stores_by_zip(zip_code, k=10):
    url = f"https://snap-finder-api.onrender.com/retailers/closest?zip_code={zip_code}&k={k}"
    response = requests.get(url)
    return response.json()

# TESTING
# print(get_closest_snap_stores(37.774929, -122.419418))
print(get_closest_snap_stores_by_zip(30058))