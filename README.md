[![Sanjay Rai](https://img.shields.io/badge/Sanjay%20Rai-FlaskRestApi-green.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Flask Rest API Prototype

### Installation
 
Clone the GitHub repo with the following command:
 
http:
>`$ git clone https://github.com/raissanjay/Flask-Rest-Api-Prototype.git

cd into the folder and install a [virtual environment](https://virtualenv.pypa.io/en/stable/)

`$ virtualenv -p python3 venv`

Activate the virtual environment

`$ source venv/bin/activate`

Install all app requirements

`$ sudo pip install -r requirements.txt`

Start your server by running 
`python manage.py runserver`. 
Use a GUI platform like [postman](https://www.getpostman.com/) to communicate with the api.

### Running Tests
The application tests are based on python’s unit testing framework unittest.
To run tests with pytest, run `pytest tests`
To run tests with nosetest, run `nosetests tests`
To run tests with unittest, run `python -m unittest tests`

### API Endpoints

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
POST /login |Logs a user in | PUBLIC
POST /register | Registers a user | PUBLIC
POST /books | Creates a new book | PRIVATE
GET /books | Lists all stored books | PRIVATE
GET /books/id | Gets a single book | PRIVATE
PUT /books/id | Updates bucket list with the suppled id | PRIVATE
PATCH /books/id | Updates bucket list with the suppled id | PRIVATE
DELETE /books/id | Deletes a single book | PRIVATE

### The MIT License (MIT)

Copyright (c) 2018 [Sanjay Rai]

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
