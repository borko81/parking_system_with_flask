from flask_restful import Resource

from resources.parking_capacity_resource import ParkingCapacityRes
from services.weather_info import WeatherInfo


class ForUsersParkingInfo(Resource):
    def get(self):
        parking_slot = ParkingCapacityRes.get()
        weather = WeatherInfo.get()
        data = {"Free Park Slot": parking_slot, "Weather": weather}
        return data
