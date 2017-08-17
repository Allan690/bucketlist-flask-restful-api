# Bucketlist-Flask-Restful-API

[![Build Status](https://travis-ci.org/iankigen/Bucketlist-Flask-RESTful-API.svg?branch=develop)](https://travis-ci.org/iankigen/Bucketlist-Flask-RESTful-API)
[![Coverage Status](https://coveralls.io/repos/github/iankigen/Bucketlist-Flask-RESTful-API/badge.svg?branch=develop)](https://coveralls.io/github/iankigen/Bucketlist-Flask-RESTful-API?branch=develop)

A Flask RESTful API implementing Token Based Authentication, pagination and searching with Endpoints that enable users to:

- Register and login.
- Create, update, view and delete a bucket list.
- Add, update, view or delete items in a bucket list.

## Example request with response 

```
Curl

curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F name=test -F password=test  'http://127.0.0.1:5000/auth/register'

Request url

http://127.0.0.1:5000/auth/register

Response body

{
  "message": "Registration successful."
}

Response code

201

Response header

{
  "date": "Thu, 17 Aug 2017 03:37:59 GMT",
  "server": "Werkzeug/0.12.2 Python/3.6.1",
  "content-length": "44",
  "content-type": "application/json"
}
```

*Note* After user login, ensure you  specify the generated token in the header:
```
token: <token>
```
## Virtual environment

Create a an isolated python environment for the API.

```
$ cd api_folder
$ virtualenv api_env
```

## Dependencies
Install all package requirements in your python virtual environment.
```
pip install -r requirements.txt
```
## Initialize the database
You need to initialize database and tables by running migrations.

```
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

```

## Start The Server
Start the server which listens at port 5000 by running the following command:
```
python api.py
```

## Pagination

The API enables pagination by passing in *page* and *limit* as arguments in the request url as shown in the following example:

```
http://127.0.0.1:5000/bucketlist?page=1&limit=10

```

## Searching

The API implements searching based on the name using a GET parameter *q* as shown below:

```
http://127.0.0.1:5000/bucketlist?q=example
```

###Available Endpoints

| Endpoint | Description |
| ---- | --------------- |
| [POST /auth/register](#) |  Register user. Request should have _name_ and _password_ in form data. |
| [POST /auth/login](#) | Login user. Session token is valid for 30 minutes. |
| [POST /auth/logout](#) | Logout user. |
| [POST /bucketlists/](#) | Create a new bucket list. Request should have _desc_ in form data. |
| [GET /bucketlists/](#) | List all the created bucket lists. |
| [GET /bucketlists/:id](#) | Get single bucket list. |
| [PUT /bucketlists/:id](#) | Update single bucket list. Request should have _desc_ in form data. |
| [DELETE /bucketlists/:id](#) | Delete single bucket list. |
| [POST /bucketlists/:id/items](#) | Add a new item to this bucket list. Request should have _goal_ in form data. |
| [PUT /bucketlists/:id/items/:item_id](#) | Update the bucket list completion status to true. |
| [DELETE /bucketlists/:id/items/:item_id](#) | Delete this single bucket list item. |
| [GET /bucketlists?limit=10](#) | Get 10 bucket list records belonging to user. |
| [GET /bucketlists?q=example](#) | Search for bucket lists with example in desc. |
