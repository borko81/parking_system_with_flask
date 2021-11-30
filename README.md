# parking_system_with_flask

Complete management system of a parking company. Works on a central server on the Internet with a database for all modules. Access to the server is restricted to authorized users only. The authorized users have access to the basic data about the parking lot, such as free places and prices for stays

<h1>User Resourse</h1>
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


