# Chat REST API

Chat REST API is an API which provides functionality to make your own app.

# About and Technologies
Chat REST API based on Django, using Django REST Framework. 
API provides CRUD actions for chat, JWT based authentication. 

# API Endpoints
Swagger endpoint:
```api/v1/swagger/```

Redoc endpoint:
```api/v1/redoc/```


## Installation

Clone the repository:
```git clone https://github.com/hahan18/chat_restapi.git```

Chat REST API requires [Python 3.10](https://www.python.org/downloads/release/python-3100/) to run.

Make virtual environment using venv in project root:
```python -m venv venv```

Activate venv:
```venv\Scripts\Activate```

Update the Pip, install the requirements and start the server.
```python -m pip install --upgrade pip```

```python -m pip install -r requirements.txt```

In project root where is manage.py file execute:

```python manage.py migrate```

Run the server using:
```python manage.py runserver```

# Improves
Swagger/Redoc docs endpoints.



## Docker
Coming soon...

   
   
   
