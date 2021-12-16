# Parking_system_with_flask

Complete management system of a parking company. Works on a central server on the Internet with a database for all modules. Access to the server is restricted to authorized users only. The unauthorized users have access to the basic data about the parking lot, such as free places and prices for stays

<h1 >Swagger url</h1>
<pre>http://127.0.0.1:5000/apidocs/</pre>

<h1>Up and running</h1>
<p>
Insert needed modules with command: python -m pip install -r requirements.txt.
Аpi running with command: flask run or python app.py.
To work with api, needed to register new user, two privileg: admin and staff When new user register is sending email to owner with this information. Insert or update new tarif plan, then add price for stay. Subscribe model has two type:
common and vip, everyone should have their own prices for stays write in table tar_el. Subscribe there may or may not be a photo uploaded to the car, the photo is kept in cloudinary. The card is entered according to whether the previous stay has already been paid or not is re-entered with status input or the measured result is updated with status output, adding a price for the estimated stay. Upon exit, the amount can be paid in cash or through wise. The day ends with a report keeping the data on the paid bills
</p>
<h1>URL Documentation</h1>
<h2>User Resourse</h2>
<h2>Add new User</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/user/register -X POST -H "Content-Type:application/json" -d '{"name": "Name G Name", "password": "A123", "type":"admin"}</pre>
<h4>Response</h4>
<pre>
When valid data
{
    "type": "Admin",
    "id": 12,
    "name": "N G N"
}
When unvalid data
{
    "message": "Invalid username Name G Name"
}
</pre>
<h2>Return all Users</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/users -H "Content-Type:application/json" -H "Authorization: Bearer{{token}}"</pre>
<h4>Response</h4>
<pre>
When valid data
[
    {
        "type": "Staff",
        "id": 9,
        "name": "Name G Name"
    },
    {
        "type": "Admin",
        "id": 11,
        "name": "A A A"
    },
    {
        "type": "Admin",
        "id": 12,
        "name": "N G N"
    }
]
When unvalid data
{
    "message": "Invalid or missing token"
}
</pre>
<h2>Update User</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/user/9 -X PUT -H "Content-Type:application/json" -H "Authorization: Bearer {{token}}" -d '{"name": "N N N"}'</pre>
<pre>curl 127.0.0.1:5000/user/9 -X PATCH -H "Content-Type:application/json" -H "Authorization: Bearer {{token}}" -d '{"name": "N N N"}'</pre>
<h4>Response</h4>
<pre>
When valid data
{
    "type": "Staff",
    "id": 9,
    "name": "N N N"
}
When unvalid data
{
    "message": "Invalid username N N N"
}
</pre>
<h2>Delete User</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/user/9 -X DELETE -H "Content-Type:application/json" -H "Authorization: Bearer {{token}}"</pre>
<h4>Response</h4>
<pre>
When valid data
204
When unvalid data
{
    "message": "Invalid id 91"
}
</pre>
<h1>Tarif Plan</h1>
<h2>Return all tarif's</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/tarif -X GET -H 'Content-Type:application/json' -H 'Authorization: Bearer {{token}}'</pre>
<h4>Response</h4>
<pre>
When valid data
{
    "all_tarife": [
        {
            "name": "Common",
            "id": 2
        },
        {
            "name": "Vip",
            "id": 45
        }
    ]
}
When unvalid data
{
    "message": "Invalid or missing token"
}
</pre>
<h2>Post new</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/tarif -X GET -POST 'Content-Type:application/json' -H 'Authorization: Bearer {{token}}' -d '{"name": "Member"}'</pre>
<h4>Response</h4>
<pre>
When valid data
{
  "name": "Member"
}
When unvalid data
{
    "message": "Invalid or missing token"
}
When unvalid argument (not valid in enum)
{
    "message": "Error acquire when try to commit data"
}
When try to add same name (unique only)
{
    "message": "Error with unique variable"
}
</pre>
<h1>Tarif Prices</h1>
<h2>Show all prices</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/tarif/price</pre>
<h4>Response</h4>
<pre>
[
    {
        "stay": "00:01",
        "price": 1,
        "tarif_id": 2
    },
    {
        "stay": "00:01",
        "price": 1,
        "tarif_id": 45
    },
    {
        "stay": "03:01",
        "price": 2,
        "tarif_id": 2
    }
]
</pre>
<h2>Add new price</h2>
<h4>Request</h4>
<pre>curl 127.0.0.1:5000/tarif/price -X POST -H "Content-Type:application/json" -d '{"tarif_id": 2, "stay":"00:01", "price":1}' -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
{
    "stay": "00:01",
    "price": 1,
    "tarif_id": 2
}
</pre>
<h2>Return price from concret id</h2>
<h4>Request all user make request</h4>
<pre>curl 127.0.0.1:5000/tarif/price/2</pre>
<h4>Response</h4>
<pre>
When valid id
{
    "stay": "00:01",
    "price": 1,
    "tarif_id": 45
}
When id is not valid
{
    "message": "Invalid id"
}
</pre>
<h2>Edit price from concret id</h2>
<h4>Request only admin do that</h4>
<pre>curl 127.0.0.1:5000/tarif/price/2 -X PUT -H "Content-Type:application/json" -d '{"price": 20} -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
When valid id
{
    "stay": "00:01",
    "price": 1,
    "tarif_id": 45
}
When id is not valid
{
    "message": "Invalid id"
}
</pre>
<h2>Delete price from concret id</h2>
<h4>Request only admin do that</h4>
<pre>curl 127.0.0.1:5000/tarif/price/2 -X DELETE -H "Content-Type:application/json" -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
When valid id
{
    "stay": "00:01",
    "price": 1,
    "tarif_id": 45
}
When id is not valid
{
    "message": "Invalid id"
}
</pre>
<h2>Return prices only for input type</h2>
<h4>Request all do that</h4>
<pre>curl 127.0.0.1:5000/tarif/type/vip</pre>
<h4>Response</h4>
<pre>
When valid id
[
    {
        "stay": "00:01",
        "price": 1,
        "tarif_id": 45
    }
]
When type is not valid
{
    "message": "Invalid type"
}
</pre>
<h1>Parking capacity Use for check has or not any free slot to enter new car in parking</h1>
<h2>Return free slot in parking</h2>
<h4>Request all do that</h4>
<pre>curl 127.0.0.1:5000/parking/capacity</pre>
<h4>Response</h4>
<pre>
5
</pre>
<h2>Post new value (only first record I get!)</h2>
<h4>Request only admin do that</h4>
<pre>curl 127.0.0.1:5000/parking/capacity -X POST -H "Content-Type:application/json" -H 'Authorization: Bearer {{token}} -d '{"capacity": 25}'</pre>
<h4>Response</h4>
<pre>
{
    "message": "Success insert parking capacity"
}
</pre>
<h2>Edit Record</h2>
<h4>Request only admin do that</h4>
<pre>curl 127.0.0.1:5000/parking/capacity -X PUT -H "Content-Type:application/json" -H 'Authorization: Bearer {{token}} -d '{"capacity": 25}'</pre>
<h4>Response</h4>
<pre>
{
    "message": "Successfully change capacity"
}
</pre>
<h2>Delete Record, delete while has any records. If you shoud to delete, delete all and then post new!</h2>
<h4>Request only admin do that</h4>
<pre>curl 127.0.0.1:5000/parking/capacity -X DELETE -H "Content-Type:application/json" -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
{
    "message": "Successfully change capacity"
}
</pre>

<h1>Subscription</h1>
<h2>Show all subscription</h2>
<h4>Request only login user view that</h4>
<pre>curl curl 127.0.0.1:5000/subscription -H "Content-Type:application/json" -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
when successfull
[
    {
        "id": 1,
        "card": "1234",
        "active_date_from": "2021-11-27 12:55:53.025131",
        "active_date_to": null,
        "name": "",
        "tar_type_id": 2,
        "email": "test@abv.bg"
    },
    {
        "id": 3,
        "card": "2222",
        "active_date_from": "2021-11-27 13:04:56.275593",
        "active_date_to": "2021-11-27 00:00:00",
        "name": "",
        "tar_type_id": 2,
        "email": null
    },
    {
        "id": 17,
        "card": "AAAA",
        "active_date_from": "2021-11-27 13:44:00.969637",
        "active_date_to": "2021-11-30 00:00:00",
        "name": "",
        "tar_type_id": 45,
        "email": null
    },
    {
        "id": 19,
        "card": "AA11",
        "active_date_from": "2021-11-28 18:40:38.018789",
        "active_date_to": null,
        "name": "",
        "tar_type_id": 2,
        "email": null
    },
    {
        "id": 20,
        "card": "AA22",
        "active_date_from": "2021-11-28 18:40:38.018789",
        "active_date_to": null,
        "name": "",
        "tar_type_id": 2,
        "email": null
    },
    {
        "id": 21,
        "card": "AA33",
        "active_date_from": "2021-11-28 18:40:38.018789",
        "active_date_to": null,
        "name": "",
        "tar_type_id": 2,
        "email": null
    }
]
When unvalid token acquire
{
    "message": "Invalid or missing token"
}
</pre>
<h2>Show all subscription</h2>
<h4>Request only login user do that</h4>
<pre>curl 127.0.0.1:5000/subscription -X POST -H "Content-type:application/json" -d '{"card": "1234", "email":"test@abv.bg", "tar_type_id": 2}' -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
{
    "message": "Successfully added card with id 22"
}
When email already exists return
{
    "message": "Card already exists"
}
</pre>
<h2>Show subscription from input id</h2>
<h4>Request only login user do that</h4>
<pre>curl 127.0.0.1:5000/subscription/21 -H "Content-type:application/json" -H 'Authorization: Bearer {{token}}</pre>
<h4>Response</h4>
<pre>
{
    "active_date_to": null,
    "id": 21,
    "name": "",
    "tar_type_id": 2,
    "card": "AA33",
    "active_date_from": "2021-11-28 18:40:38.018789",
    "email": null
}
When not found this id return
{
    "message": "Invalid id 214"
}
</pre>
<h2>Change subscription from input id</h2>
<h4>Request only login user do that</h4>
<pre>curl 127.0.0.1:5000/subscription/21 -H "Content-type:application/json" -H 'Authorization: Bearer {{token}} -d '{"card": "4321", "tar_type_id": 2, "all": "test"}'</pre>
<h4>Response</h4>
<pre>
When input data is valid return
{
    "active_date_to": null,
    "id": 21,
    "name": "",
    "tar_type_id": 45,
    "card": "123456",
    "active_date_from": "2021-11-28 18:40:38.018789",
    "email": "test12@abv.bg"
}
When card already exists in other subscribe, or email is already exists return
{
    "message": "Error acquire when try to commit data"
}
</pre>
<h2>Delete subscription from input id</h2>
<h4>Request only login user do that</h4>
<pre>curl 127.0.0.1:5000/subscription/21 -X DELETE -H "Content-type:application/json" -H 'Authorization: Bearer {{token}}'</pre>
<h4>Response</h4>
<pre>
When input data is valid return
204
When not found that id return
{
    "message": "Invalid id 211"
}
</pre>
<h2>Get All subscribe, input param is type id, return all card who belong to that type_id</h2>
<h4>Request only login user do that</h4>
<pre>curl 127.0.0.1:5000/subscription/type/45 -H "Content-type:application/json" -H 'Authorization: Bearer {{token}}'</pre>
<h4>Response</h4>
<pre>
When input data is valid return
[
    {
        "tar_type_id": 45,
        "active_date_to": "2021-11-30 00:00:00",
        "active_date_from": "2021-11-27 13:44:00.969637",
        "email": null,
        "id": 17,
        "name": "",
        "card": "AAAA"
    },
    {
        "tar_type_id": 45,
        "active_date_to": null,
        "active_date_from": "2021-11-28 18:40:38.018789",
        "email": "test12@abv.bg",
        "id": 21,
        "name": "",
        "card": "123456"
    }
]
When not found that type_id return
[]
</pre>
<h1>Parking system</h1>
<h2>Returns all cards that are still in the parking lot and have not paid</h2>
<h4>Request</h4>
<pre>
curl --location --request GET 'http://127.0.0.1:5000/parking' --header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>  
<pre>
Invalid data:
{
    "message": "Invalid or missing token"
}
Valid data:
[
    {
        "id": 11,
        "income": "2021-12-01 12:25:24.339172",
        "card": "1234"
    },
    {
        "id": 12,
        "income": "2021-12-01 12:39:19.151390",
        "card": "123456"
    }
]
</pre>
<h2>Adds a new card in the parking lot, if the card is already there and has not been paid yet, the information with the financial part is updated</h2>
<h4>Request</h4>
<pre>
curl --location --request POST 'http://127.0.0.1:5000/parking' --header 'Content-Type: application/json' --header 'Authorization: Bearer {{token}}' --data-raw '{"card": "123456"}'
</pre>
<h4>Response</h4>  
<pre>
When car not found return:
{
    "message": "This card not found on server, try with another"
}
When Data is corect return:
{
    "id": 11,
    "income": "2021-12-01 12:25:24.339172",
    "card": "1234"
}
When not enough free space return
{
    "message": "Not Enough space in park"
}
When card has expired time return
{
    "message": "This card is nо longer valid"
}
</pre>
When card found ot parking and card not payment yet return
<pre>
{
    "message": "Card found",
    "card": "12345",
    "price": 1.0,
    "id": 91,
    "income": "2021-12-16 13:11:26.890717",
    "outcome": "2021-12-16 13:24:49.351589",
    "cart_type_id": "2",
    "cart_type_name": "Common"
}
</pre>
<h2>Return Parking Detail Only Admin allowed to do that</h2>
<h4>Request</h4>
<pre>
curl --location --request GET 'http://127.0.0.1:5000/parking/detail/11' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>  
<pre>
When data is valid return:
{
    "card": "123456",
    "otc_id": null,
    "pay": true,
    "tarif_id": 45,
    "id": 12,
    "income": "2021-12-01 12:39:19.151390",
    "outcome": null,
    "price": null
}
When id not found return
{
    "message": "Not found this id 115"
}
When not user make request return:
{
    "message": "You do not have the rights to access this resource"
}
</pre>
<h2>Edit Card in Park, card give from id</h2>
<h4>Request</h4>
<pre>
curl --location --request PUT 'http://127.0.0.1:5000/parking/detail/12' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}' \
--data-raw '{
    "card": "123456",
    "otc_id": null,
    "pay": true,
    "tarif_id": 45,
    "id": 12,
    "income": "2021-11-01 12:39:19.151390",
    "outcome": null,
    "price": null
}'
</pre>
<h4>Response</h4>  
<pre>
Whene data is valid:
{
    "card": "123456",
    "otc_id": null,
    "pay": true,
    "tarif_id": 45,
    "id": 12,
    "income": "2021-11-01 12:39:19.151390",
    "outcome": null,
    "price": null
}
When card pay is True return:
{
    "message": "Card is already payed, not allow editing!"
}
</pre>
<h2>Delete card from park, only if not already payed</h2>
<h4>Request</h4>
<pre>
curl --location --request DELETE 'http://127.0.0.1:5000/parking/detail/12' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>  
<pre>
Whene data is valid:
204
When card pay is True return:
{
    "message": "Card is already payed, not allow editing!"
}
</pre>
<h2>Return all card in park who not payed</h2>
<h4>Request</h4>
<pre>
curl --location --request GET 'http://127.0.0.1:5000/parking' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>
<pre>
[
{
    "id": 86,
    "income": "2021-12-10 13:50:25.898783",
    "card": "A123"
},
{
    "id": 87,
    "income": "2021-12-10 13:50:31.327451",
    "card": "A1234"
}
]
</pre>
<h2>Return info for concret parking id</h2>
<h4>Request</h4>
<pre>
curl --location --request GET 'http://127.0.0.1:5000/parking/detail/77' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
</h4>Response</h4>
<pre>{
"id": 77,
"outcome": "2021-12-08 11:40:27.589098",
"card": "12345",
"otc_id": 4,
"tarif_id": 2,
"price": 1.0,
"pay": true,
"income": "2021-12-08 10:40:05.677984"
}
</pre>
<h2>Delete card from park, if stay is less then 1 minute, required payment is still not payed</h2>
<h4>Request</h4>
<pre>
curl --location --request DELETE 'http://127.0.0.1:5000/parking/detail/84' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>
<pre>
204
</pre>
When bill already pay return
<pre>404, Card is already payed, not allow editing!</pre>
<h2>Edit card data, admin is required, need not pay too</h2>
<h4>Request</h4>
<pre>
curl --location --request PUT 'http://127.0.0.1:5000/parking/detail/12' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{roken}}' \
--data-raw '{
    "card": "123456",
    "otc_id": null,
    "pay": true,
    "tarif_id": 45,
    "id": 12,
    "income": "2021-11-01 12:39:19.151390",
    "outcome": null,
    "price": null
}'
</pre>
When bill already pay return
<pre>404, Card is already payed, not allow editing!</pre>

<h2>Insert ot update card in park</h2>
<p>If park not has not payed card, insert new one, else found id and update with outgoing time data and price</p>
<h4>Request</h4>
<pre>
curl --location --request POST 'http://127.0.0.1:5000/parking' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}' \
--data-raw '{
    "card": "12345"
}'
</pre>
<h4>Response</h4>
<pre>
When card stay is less then 1 minute return:
This card stay less then 1 minute, you may want to delete record with id
When not found card return: 
This card not found on server, try with another
When not enough free slot in park return:
Not enough place
When not valid data expired for card return:
This card is nо longer valid
</pre>
When card is income insert
<pre>
{
    "card": "12345",
    "income": "2021-12-13 17:26:26.437234",
    "id": 88
}
</pre>
When card is outcome insert (update)
<pre>
{
    "message": "Found",
    "card": "12345",
    "price": 1.0,
    "id": 88
}
</pre>
<h2>Paymnet</h2>
<h4>Payment Request</h4>
<pre>
For cash
curl --location --request POST 'http://127.0.0.1:5000/parking/85/cash' \
--header 'Content-Type: application/json' \
--data-raw ''
With wise
curl --location --request POST 'http://127.0.0.1:5000/parking/78/wise' \
--header 'Content-Type: application/json' \
--data-raw ''
</pre>
<h4>Response, result is write in table transaction, return</h4>
<pre>"Success pay id: 88, sum: 1.00."</pre>
<h2>Show Transactions, admin rights is required</h2>
<h4>Request</h4>
<pre>
For all transacions
curl --location --request GET 'http://127.0.0.1:5000/transactions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
For concret transacion, found by id or transaction number, number get from wise payment
curl --location --request GET 'http://127.0.0.1:5000/transaction?id=2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}' \
--data-raw '{
    "by trans_id": http://127.0.0.1:5000/transaction?trans_id=50320289
    "by id": http://127.0.0.1:5000/transaction?id=2
}'
</pre>
<h4>Response</h4>
<pre>
For all transaction
[
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T12:46:47.913695",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320057,
        "id": 2
    },
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T12:51:10.905650",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320067,
        "id": 3
    },
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T12:53:31.490152",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320072,
        "id": 4
    },
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T13:02:41.123741",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320097,
        "id": 5
    },
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T13:51:51.300187",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320276,
        "id": 6
    },
    {
        "pay_type": 2,
        "pr_id": 77,
        "created_on": "2021-12-08T13:56:10.092252",
        "payment_name": {
            "name": "wise"
        },
        "transaction_id": 50320289,
        "id": 7
    },
    {
        "pay_type": 1,
        "pr_id": 78,
        "created_on": "2021-12-08T14:17:15.982583",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 10
    },
    {
        "pay_type": 1,
        "pr_id": 78,
        "created_on": "2021-12-08T14:16:23.194071",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 9
    },
    {
        "pay_type": 1,
        "pr_id": 83,
        "created_on": "2021-12-10T13:51:23.390760",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 11
    },
    {
        "pay_type": 1,
        "pr_id": 86,
        "created_on": "2021-12-10T13:51:37.874737",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 12
    },
    {
        "pay_type": 1,
        "pr_id": 85,
        "created_on": "2021-12-10T13:53:39.151693",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 13
    },
    {
        "pay_type": 1,
        "pr_id": 88,
        "created_on": "2021-12-13T17:33:05.919786",
        "payment_name": {
            "name": "cash"
        },
        "transaction_id": -2,
        "id": 14
    }
]
<p>For concret id or transaction id
{
    "pay_type": 2,
    "pr_id": 77,
    "created_on": "2021-12-08T12:51:10.905650",
    "payment_name": {
        "name": "wise"
    },
    "transaction_id": 50320067,
    "id": 3
}
</pre>
<h2>OTC generate and show, login required</h2>
<h4>Generate otc, all already payment card is close in otc id</h4>
<pre>
curl --location --request POST 'http://127.0.0.1:5000/otc' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>
<pre>
{
    "message": "Success",
    "otc_id": 5
}
</pre>
<h4>Show otc id, login required, request</h4>
<pre>
curl --location --request GET 'http://127.0.0.1:5000/otc/5' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{token}}'
</pre>
<h4>Response</h4>
<pre>
{
    "created_on": "2021-12-13T17:41:29.016606",
    "park_otc": [
        {
            "card": "12345",
            "tarif_id": 2,
            "outcome": "2021-12-13 17:30:56.839602",
            "pay": true,
            "park_pay": [
                {
                    "pay_type": 1,
                    "pr_id": 88,
                    "created_on": "2021-12-13T17:33:05.919786",
                    "payment_name": {
                        "name": "cash"
                    },
                    "transaction_id": -2,
                    "id": 14
                }
            ],
            "income": "2021-12-13 17:26:26.437234",
            "otc_id": 5,
            "price": 1.0,
            "id": 88
        }
    ],
    "user_id": 17,
    "id": 5
}
</pre>
