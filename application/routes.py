from application.utils import check_input, get_weather
from flask import request, jsonify, current_app


@current_app.route("/precipitations", methods=["GET"])
def get_precipitations():
    """
    Returns a json containing the visibility and Amount of precipitation in the last hour
    of closest location based on lat/lng parameters
    """
    input = check_input(request.args)
    weather = get_weather(input["lat"], input["lng"], current_app.config["ACCUWEATHER_API_KEY"],
                          current_app.config["ACCUWEATHER_API_BASE_URL"])
    response = {k: v for k, v in weather.items() if k in ["precipitations_past_hour",
                                                          "visibility"]}
    response = jsonify(response)
    return response


@current_app.route("/uv", methods=["GET"])
def get_uv_index():
    """
    Returns current UV index of closest location based on lat/lng parameters
    """
    input = check_input(request.args)
    weather = get_weather(input["lat"], input["lng"], current_app.config["ACCUWEATHER_API_KEY"],
                          current_app.config["ACCUWEATHER_API_BASE_URL"])
    response = {k: v for k, v in weather.items() if k in ["uv_index"]}
    response = jsonify(response)
    return response
