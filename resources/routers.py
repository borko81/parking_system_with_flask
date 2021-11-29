from resources.user_resource import UserRegisterRes, UserLoginRes, UserControlRes, ReturnAllUsersRes

from resources.tarifs import TarifAllRes, TarifPricesRes, TarifConcretRes, ReturnPricesFromConcretTypeRes

from resources.subsription import SubscriptionRes, SubscribeFromIdRes, SubscriptionFromType

from resources.parking import ParkingRes, ParkingPayRes, ParkingAlreadyPay, ParkingDetailInfoRes

from resources.parking_capacity_resource import ParkingCapacityRes

routers = (
    (UserRegisterRes, "/user/register"),
    (ReturnAllUsersRes, "/users"),
    (UserControlRes, "/user/<int:_id>"),
    (UserLoginRes, "/login"),
    (TarifAllRes, "/tarif"),
    (TarifPricesRes, "/tarif/price"),
    (TarifConcretRes, "/tarif/price/<int:_id>"),
    (ReturnPricesFromConcretTypeRes, '/tarif/type/<string:type>'),
    (SubscriptionRes, "/subscription"),
    (SubscribeFromIdRes, "/subscription/<int:_id>"),
    (SubscriptionFromType, "/subscription/type/<int:_id>"),
    (ParkingRes, "/parking"),
    (ParkingPayRes, "/parking/pay/<int:id>"),
    (ParkingAlreadyPay, "/parking/already_pay"),
    (ParkingDetailInfoRes, "/parking/detail/<int:_id>"),
    (ParkingCapacityRes, "/parking/capacity")
)
