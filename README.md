# sqlalchemy-challenge

In this challenge, Python and SQLAlchemy is used to do basic climate analysis and data exploration of your climate database. The following analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib

Step 1

-SQLAlchemy is used to an create_engine to connect to your sqlite database.


-SQLAlchemy automap_base() is used to reflect your tables into classes and a reference is saved to those classes called Station and Measurement.


-Python is linked to the database by creating an SQLAlchemy session.

Precipitation Analysis

-An ORM query is done on the precipitation data and an analysis is done

-The query results is then loaded into the Pandas DataFrame 

-Station Analysis

-An ORM query is designed to retrive temperature data 

-The results is plotted as a histogram with bins=12

Step 2

Climate App

-After completion of all analysis, a Flask API is designed based on the queries developed.

 Flask is used to create routes to specific endpoints on the app.