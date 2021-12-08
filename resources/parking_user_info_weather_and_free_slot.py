from resources.parking_capacity_resource import ParkingCapacityRes
from resources.weather_info import WeatherInfo
from flask_restful import Resource


class ForUsersPArkingInfo(Resource):
    def get(self):
        parking_slot = ParkingCapacityRes.get()
        weather = WeatherInfo.get()
        data = {"Free Park Slot": parking_slot, "Weather": weather}
        return data
