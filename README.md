Author: Lai Man Tang
Github: https://github.com/littlecloud1/Simple-restaurant
Date: 8-20-2018

# Simple-restaurant 
This project build a simple restaurant achieved CRUD.  (udacity coursework)

## Requirement
  1. Python 3 version < 3.7 (cgi.parse_multipart does not work on 3.7)
  2. SQLAlchemy
  
  To install SQLAlchemy:
  pip install sqlalchemy
  
## Files
Inputfile:
  #webserver-restaurant.py#: do_POST and do_GET function for restaurant CRUD 
  #webserver-post.py#: return whatever user input
  #lotsofmenu.py#: Restaurant database from Udacity, I modify it to python 3 version
  
## How To run:

#### To run a simple get and post server:
python webserver-post.py

and access localhost:8080/hello

#### To run the restaurant server you have to import the database from udacity
python lotsofmenu.py

Then run the server:
python webserver-restaurant.py

and access localhost:8080/restaurants

