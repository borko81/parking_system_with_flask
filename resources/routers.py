from resources.user_resource import UserRegisterRes, UserLoginRes, UserControlRes

from resources.tarifs import TarifAllRes, TarifPricesRes, TarifConcretRes, ReturnPricesFromConcretTypeRes

from resources.subsription import SubscriptionRes, SubsciprConcretRes, SubscriptionFromType

from resources.parking import ParkingRes, ParkingPayRes, ParkingAlreadyPay, ParkingTetailInfoRes

from resources.parking_capacity_resource import ParkingCapacityRes

routers = (
    (UserRegisterRes, "/user/register"),
    (UserControlRes, "/user/<int:_id>"),
    (UserLoginRes, "/login"),
    (TarifAllRes, "/tarif"),
    (TarifPricesRes, "/tarif/price"),
    (TarifConcretRes, "/tarif/price/<int:_id>"),
    (ReturnPricesFromConcretTypeRes, '/tarif/type/<string:type>'),
    (SubscriptionRes, "/subscription"),
    (SubsciprConcretRes, "/subscription/<int:_id>"),
    (SubscriptionFromType, "/subscription/type/<int:_id>"),
    (ParkingRes, "/parking"),
    (ParkingPayRes, "/parking/pay/<int:id>"),
    (ParkingAlreadyPay, "/parking/already_pay"),
    (ParkingTetailInfoRes, "/parking/detail/<int:_id>"),
    (ParkingCapacityRes, "/parking/capacity")
)
