
from flask import abort
import requests


def check_input(args: dict) -> dict:
    """
    Check if user entries latitude and longitude are well formated. If ok, retruns a dict with 
    lat and lng converted as flaots
        - args: dict. request.args
    """
    lat = args.get("lat")
    lng = args.get("lng")
    if lat is None:
        abort(400, "Latitude parameter (lat) is missing")
    if lng is None:
        abort(400, "Longitude parameter (lng) is missing")
    return {"lat": check_lat_lng(lat, "latitude"), "lng": check_lat_lng(lng, "longitude")}


def lat_lng_error_message(value: str, param: str) -> str:
    """
    Defines an error message when lat or long are not in good format
        - value: str. Latitude or longitude value as a string
        - param: str. Name of the param (either latitude or longitude)
    """    
    error_msg = "Incorrect " + param + " parameter: " + value + ". Latitudes should be floats"
    error_msg += " in the range (-90, 90) and longitudes should be floats in the range (-180, 180)"
    return error_msg


def check_lat_lng(value: str, param: str) -> float:
    """
    Check if user entries latitude and longitude are well formated. If ok, returns the value as 
    a float.
        - value: str. Latitude or longitude value as a string
        - param: str. Name of the param (either latitude or longitude)
    """

    try:
        value = float(value)
    except ValueError:
        abort(400, lat_lng_error_message(value, param))
    if param == "latitude":
        if value < -90 or value > 90:
            abort(400, lat_lng_error_message(value, param))
    elif param == "longitude":
        if value < -180 or value > 180:
            abort(400, lat_lng_error_message(value, param))
    else:
        raise ValueError("param parameter should be one of [lat, lng]")
    return value


def get_location_id(lat: float, lng: float, accu_weather_api_key: str, 
                    accu_weather_api_url: str) -> str:
    """ 
    Calls Accuweather API location endpoint to get closest city to lat and lng
        - lat: float. Latitude of the location the user if searching for
        - lng: float. Longitude of the location the user if searching for
        - accu_weather_api_key: str. Accuweather API key you get after registration. See 
        https://developer.accuweather.com/ for further details
        - accu_weather_api_url: str. Accuweather API base url.
    """
    req_url = accu_weather_api_url + "/locations/v1/cities/geoposition/search"
    params = {"apikey": accu_weather_api_key, "q": str(lat) + "," + str(lng)}
    response = requests.get(req_url, params=params)
    if response.status_code != 200:
        abort(404, "Location not found from Accuweather API!")
    key = response.json()["Key"]
    return key


def get_current_conditions(location_id: str, accu_weather_api_key: str,
                           accu_weather_api_url: str) -> dict:
    """ 
    Calls Accuweather API location endpoint to get conditions in the location defined by 
    location_id.
        - location_id: str. As returned by get_location_id
        - accu_weather_api_key: str. Accuweather API key you get after registration. See 
        https://developer.accuweather.com/ for further details
        - accu_weather_api_url: str. Accuweather API base url.
    """
    req_url = accu_weather_api_url + "/currentconditions/v1/" + location_id
    params = {"apikey": accu_weather_api_key, "details": "true"}
    response = requests.get(req_url, params=params)
    if response.status_code != 200:
        abort(404, "Current conditions not found from Accuweather API!")
    resp = response.json()
    prec_past_hour = resp[0]["PrecipitationSummary"]["PastHour"]
    uv_index = resp[0]["UVIndex"]
    visibility = resp[0]["Visibility"]
    conditions = {"precipitations_past_hour": prec_past_hour, "visibility": visibility,
                  "uv_index": uv_index}
    return conditions


def get_weather(lat: float, lng: float, accu_weather_api_key: str,
                accu_weather_api_url: str) -> dict:
    """ 
    Get weather conditions in the closest city to lat and lng through two Accuweather API calls 
    (location, and current_conditions)
        - lat: float. Latitude of the location the user if searching for
        - lng: float. Longitude of the location the user if searching for
        - accu_weather_api_key: str. Accuweather API key you get after registration. See 
        https://developer.accuweather.com/ for further details
        - accu_weather_api_url: str. Accuweather API base url.
    """
    location_id = get_location_id(lat, lng, accu_weather_api_key, accu_weather_api_url)
    res = get_current_conditions(location_id, accu_weather_api_key, accu_weather_api_url)
    return res
