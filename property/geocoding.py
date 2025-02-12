# utils/geocoding.py
import requests
import re

def extract_lat_lon_from_gmaps_url(url):
    """
    Extracts latitude and longitude from a Google Maps URL.
    Returns a tuple (latitude, longitude) or (None, None) if extraction fails.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        full_url = requests.get(url, headers=headers, allow_redirects=True).url

        if "maps/search/" in full_url:
            extracted = re.search(r"maps/search/(.*?)(coh%|$)", full_url)
            location = extracted.group(1) if extracted else None

            if location and "," in location:
                lat_raw, lon_raw = location.split(",")[:2]
                extract_coord = lambda val: val[max(0, val.find(".")-2):val.find(".")+7] if "." in val else None
                latitude = extract_coord(lat_raw)
                longitude = extract_coord(lon_raw)
                return latitude, longitude

    except requests.RequestException:
        pass

    return None, None