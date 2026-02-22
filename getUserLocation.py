"""
User location handling for the web app.

The actual latitude/longitude come from the browser when the user grants
location permission (Geolocation API). The frontend sends lat/lon to your
backend; these helpers validate and use them (e.g. to find closest SNAP stores).
"""


def get_user_location_from_coords(lat: float, lon: float) -> dict:
    """
    Validate and return user location from coordinates sent by the frontend.
    Call this with the lat/lon you receive after the user grants location access.
    """
    lat, lon = float(lat), float(lon)
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates: lat must be -90..90, lon -180..180")
    return {"lat": lat, "lon": lon}


def get_location_and_closest_snap_stores(lat: float, lon: float, k: int = 10) -> dict:
    """
    Get the user's location (lat/lon) and the closest SNAP stores to them.
    Use this when the frontend has already sent you lat/lon (after user said yes).
    """
    from findSnapStores import get_closest_snap_stores

    location = get_user_location_from_coords(lat, lon)
    stores = get_closest_snap_stores(lat, lon, k=k)
    return {"location": location, "snap_stores": stores}


# --- Frontend: get lat/lon in the web app when user says yes ---
# Use the browser Geolocation API, then send coords to your backend:
#
#   if (navigator.geolocation) {
#     navigator.geolocation.getCurrentPosition(
#       (pos) => {
#         const lat = pos.coords.latitude;
#         const lon = pos.coords.longitude;
#         // POST or GET to your backend with lat, lon, then call
#         // get_location_and_closest_snap_stores(lat, lon) on the server
#         // or get_closest_snap_stores(lat, lon) from findSnapStores
#       },
#       (err) => { /* user denied or error */ }
#     );
#   }