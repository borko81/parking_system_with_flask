import requests
from decouple import config
from flask_restful import Resource
from werkzeug.exceptions import BadRequest


class WeatherInfo(Resource):
    @staticmethod
    def get():
        URL = f"http://api.openweathermap.org/data/2.5/weather?q=\
        {config('OPENWEATHER_TOWN')}&appid={config('OPENWEATHER_APIID')}&lang=bg&units=metric"
        check = requests.get(URL)
        if check.status_code == 200:
            json_data = check.json()
            data = {
                "Name": json_data["name"],
                "Temperature": round(json_data["main"]["temp"]),
                "FeelsLike": round(json_data["main"]["feels_like"]),
                "Weather": json_data["weather"][0]["description"],
            }
            return data
        else:
            raise BadRequest("Error with fetch data")
