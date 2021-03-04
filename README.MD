# Description
Application is designed to gather specyfic informations about geographic localizations from given (as input by user) ip or domain.
Once user is logged in, system gives an access to variety areas of implemented functionalities. Thus it is possible to check given ip/url with using web browser (registration process must be done here!), but due to logically use of an app its highly preferable to use rest-api (so that it could be use as more flexible api). 

## Tech stack
Application guarantees fully working JWT, session and basic authentications which is handled by django framework (3.1.6). Application stands on gunicron server with nginx as a reverse proxy. Rest-api is done with an use of default rest-framework in version 3.12.2 and geolocalization is provided by authored API (which is an wrapper for ipstack.com python api). Locally for testing purposes - its using sqlite database - in "production" release it consists on postresql (Docker/Heroku).

## Usage

As clients visit index page it could be redirected to geo_app view (if logged in) else to the registration process form.
Creating entries in the system is possible in two ways - by web browser frontend api - or by rest requests on given endpoint (ad: restful api).

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`geoloc/register/` | POST | Registration process
`geoloc/login/` | GET | Login process
`geoloc/index/` | GET | Dedicated frontend for geo_app

Some examples of an requests:
```
REQ:
GET /geoloc/register/ HTTP/1.1

RES:
HTTP/1.1 200 OK
Date: Thu, 04 Mar 2021 12:44:27 GMT
Server: WSGIServer/0.2 CPython/3.7.5
Content-Type: text/html; charset=utf-8
Vary: Cookie
Content-Length: 1703
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Set-Cookie:  csrftoken=vqQtf4dlcEZCel0to54tvOxpWnXic8mK1kOChoLy7znHPIT3hcT1u7nYX2sKTh0g; expires=Thu, 03 Mar 2022 12:44:27 GMT; Max-Age=31449600; Path=/; SameSite=Lax

```

```
REQ:
GET /geoloc/index/ HTTP/1.1
RES:
HTTP/1.1 302 Found
Date: Thu, 04 Mar 2021 12:49:02 GMT
Location: /geoloc/register/?next=/geoloc/index/

```


# Restful api
## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`geoloc/api/v1/get/:id` | GET | Get a single entry
`geoloc/api/v1/create/` | PUT | Create a single entry with given data
`geoloc/api/v1/create/` | PUT | Create a single entry with only ip given
`geoloc/api/v1/update/:id` | PUT | Update a single entry
`geoloc/api/v1/delete/:id` | DELETE | Delete a single entry


Request with jwt authorization:
```
GET /geoloc/api/v1/get/96/ HTTP/1.1
Host: localhost:8000
Accept: application/json
Accept-Language: pl,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE0NjA0NjI4LCJqdGkiOiIyZmYxYzNlNjE5YWQ0NWFmYjQwNjdlNmNmNzA5ZDEzNiIsInVzZXJfaWQiOjF9.C3CuiWYRwQ2RIKxeoBNTrJ4t533IH8Jp85BOwZZyCr0
Upgrade-Insecure-Requests: 1
```
RES
```
HTTP/1.1 200 OK
Date: Mon, 01 Mar 2021 13:12:21 GMT
Server: WSGIServer/0.2 CPython/3.7.5
Content-Type: application/json
Vary: Accept, Cookie
Allow: GET
X-Frame-Options: DENY
Content-Length: 88
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

[{"id":96,"ip":"2607:f8b0:4004:810::200e","protocol":"ipv6","region_id":72,"user_id":1}]
```

Create new request with ip given:
```
Accept: application/json
User-Agent: curl/7.55.1
Accept: */*
Content-Type: application/json
Content-Length: 30
Connection: close
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE0ODYyOTEwLCJqdGkiOiJhYjAwNmJjOTg4ZWM0ZWFhYjRhNDAxM2EzMWY5NzY2MiIsInVzZXJfaWQiOjF9.XUBWpVuGhzwpP-gxec3xP3aeUPXny5vWgyhzPEn5JSY
Content-Length: 30

{"geo_location":"youtube.com"}
```
RES
```
Content-Type: application/json
Vary: Accept, Cookie
Allow: PUT
Content-Length: 16
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{"created":true}
```


# Setup

-Docker
Configured to run with docker - but running locally or on heroku requires minor changes in settings.py. Run command below from '\sofomo_rekrutacja\':
```
docker-compose -f docker-compose.prod.yml build
docker-compose down && docker-compose up
```
Now container is running, check it out at http://localhost:1337.

Entering into docker container (same folder as in previous step):
```
docker-compose exec web /bin/sh
```

-Locally
Comment out docker or heroku options. Analogically uncomment local options in settings.py.
```
python manage.py test && python manage.py runserver
``` 



Request with basic authorziation:

```
# curl --user zyhu:lol123 http://localhost:8000/geoloc/api/v1/get/49/
```