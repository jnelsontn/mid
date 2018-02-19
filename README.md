## Feature Request App

Front-End (Client directory)
API (webapp directory).

## Installation:

Clone down the repository and ```pip install -r requirements.txt``` to install required python dependencies.
Please modify the ```secret.py``` file and modify the string to create a unique SECRET_KEY.

A fixtures file with sample data has been included. To load the fixtures file
```python manage.py loaddata initial.json``` from the webapp directory. As the API will send HTML back to the client
for certain response, run ```python manage.py collectstatic``` to build the Django static files.

Initiate the Django test server by running: ```python manage.py runserver```. A web server (Apache, Nginx, etc.) is required to server the client/ data. Depending on your configuration, you will need to modify the Django settings in the manage.py file, specifically ALLOWED_HOSTS, CORS_ORIGIN_WHITELIST.

Note, if the service hosting the html content is on a different machine, the apiUrl in the index.html will need to be modified to reflect the IP address and port number of the API server.

## Tech Stack

* Server Side Scripting: Python 3.6.4
* Server Framework: Django 1.11.10 w/Django REST Framework 3.3.7
* ORM: Django
* Javascript: JQuery 3.3.1

