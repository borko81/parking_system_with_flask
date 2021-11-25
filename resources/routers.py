from user import UserRegisterRes, UserLoginRes, UserControlRes

from tarifs import (
    TarifAllRes,
    TarifPricesRes,
    TarifConcretRes,
)

from subsription import SubscriptionRes, SubsciprConcretRes, SubscriptionFromType

from parking import ParkingRes, ParkingPayRes, ParkingAlreadyPay, ParkingTetailInfoRes

routes = (
    (UserRegisterRes, "/user/register"),
    (UserControlRes, "/user/<int:_id>"),
    (UserLoginRes, "/login"),
    (TarifAllRes, "/tarif"),
    (TarifPricesRes, "/tarif/price"),
    (TarifConcretRes, "/tarif/price/<int:_id>"),
    (SubscriptionRes, "/subscription"),
    (SubsciprConcretRes, "/subscription/<int:_id>"),
    (SubscriptionFromType, "/subscription/type/<int:_id>"),
    (ParkingRes, "/parking"),
    (ParkingPayRes, "/parking/pay/<int:id>"),
    (ParkingAlreadyPay, "/parking/already_pay"),
    (ParkingTetailInfoRes, "/parking/detail/<int:_id>"),
)
