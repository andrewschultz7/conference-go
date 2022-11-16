from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"per_page": 1, "query": city + " " + state}
    url = "https://api.pexels.com/v1/search/"
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    r = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},USA&limit=1&appid={OPEN_WEATHER_API_KEY}"
    )

    weather = json.loads(r.content)
    # lat_lon = {
    #     "lat": weather[0]["lat"],
    #     "lon": weather[0]["lon"],
    # }

    lat = weather[0]["lat"]
    lon = weather[0]["lon"]
    response2 = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    )
    weather = json.loads(response2.content)
    temperature = {
        "temp": weather["main"]["temp"],
        "desciption": weather["weather"][0]["description"],
    }

    return temperature
