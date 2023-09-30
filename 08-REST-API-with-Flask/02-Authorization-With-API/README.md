# Falsk JWT library

We can use the Flask-JWT library to require authorization before being able to create a REST API call.
Users will need to provide a username and password to an authentication page, then they will recieve a key they can attach to their calls.
We can install this library with:
-   pip install Flask-JWT

Error: changed from collections import Mapping to from collections.abc import Mapping

HOW TO GET ACCESS:
GET     : http://127.0.0.1:5000/auth
HEADER  : { Key: Content-Type, Value: application/json }
BODY    : { "username":"FirstUser", "password":"password" }
You will be an access token:
{
    "access_token": "******TOKEN_VALUE*********"
}
NOW,
GET     : http://127.0.0.1:5000/cars
HEADER  : { Key: Authorization, Value: JWT access_token_value }