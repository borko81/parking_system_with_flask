from flask_restful import Resource
from decouple import config
import requests
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
                "Temperature": json_data["main"]["temp"],
                "FeelsLike": json_data["main"]["feels_like"],
            }
            return data
        else:
            raise BadRequest("Error with fetch data")
