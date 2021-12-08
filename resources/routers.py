from resources.weather_info import WeatherInfo
from resources.parking_user_info_weather_and_free_slot import ForUsersPArkingInfo
from resources.pay_resource import PayResourse
from resources.pay_type_resourse import PayTypeResourse, PayTypeIdResourse
from resources.transactions_resourse import (
    TransactionsResourse,
    TransactionInfoResourse,
)

from resources.user_resource import (
    UserRegisterRes,
    UserLoginRes,
    UserControlRes,
    ReturnAllUsersRes,
)

from resources.tarifs import (
    TarifAllRes,
    TarifPricesRes,
    TarifConcretRes,
    ReturnPricesFromConcretTypeRes,
)

from resources.subsription import (
    SubscriptionRes,
    SubscribeFromIdRes,
    SubscriptionFromType,
)

from resources.parking import (
    ParkingRes,
    ParkingPayRes,
    ParkingAlreadyPay,
    ParkingDetailInfoRes,
)

from resources.parking_capacity_resource import ParkingCapacityRes

routers = (
    (ForUsersPArkingInfo, "/parking_info"),
    (WeatherInfo, "/weather"),
    (UserRegisterRes, "/user/register"),
    (ReturnAllUsersRes, "/users"),
    (UserControlRes, "/user/<int:_id>"),
    (UserLoginRes, "/login"),
    (PayTypeResourse, "/pay_type"),
    (PayTypeIdResourse, "/pay_type/<int:_id>"),
    (TarifAllRes, "/tarif"),
    (TarifPricesRes, "/tarif/price"),
    (TarifConcretRes, "/tarif/price/<int:_id>"),
    (ReturnPricesFromConcretTypeRes, "/tarif/type/<string:type>"),
    (SubscriptionRes, "/subscription"),
    (SubscribeFromIdRes, "/subscription/<int:_id>"),
    (SubscriptionFromType, "/subscription/type/<int:_type>"),
    (ParkingRes, "/parking"),
    (ParkingPayRes, "/parking/pay/<int:id>"),
    (ParkingAlreadyPay, "/parking/already_pay"),
    (ParkingDetailInfoRes, "/parking/detail/<int:_id>"),
    (ParkingCapacityRes, "/parking/capacity"),
    (PayResourse, "/parking/<int:_id>/<string:pay>"),
    (TransactionsResourse, "/transactions"),
    (TransactionInfoResourse, "/transaction"),
)
