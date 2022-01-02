from flask_restful import Resource

from helpers.loger_config import custom_logger
from resources.parking_capacity_resource import ParkingCapacityRes
from services.weather_info import WeatherInfo


class ForUsersParkingInfo(Resource):
    @staticmethod
    def get():
        """
        Return weather info and parking free slots
        ---
        tags:
        - weather info free space in park
        responses:
          200:
            description: OK
        """
        parking_slot = ParkingCapacityRes.get()
        # Paused to check flask wun in testing mod if not true, load weather info
        if not "FLASK_ENV" == "testing":
            weather = WeatherInfo.get()
            data = {"Free Park Slot": parking_slot, "Weather": weather}
        else:
            data = {"Free Park Slot": parking_slot}
        custom_logger(
            "error", f"{ForUsersParkingInfo.get.__qualname__} result is: {data}"
        )
        return data
