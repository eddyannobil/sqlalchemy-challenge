import numpy as np
import datetime as dt
import pandas as pd
import sys

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )   


@app.route("/api/v1.0/precipitation")
def prcp():
    
    

    """Return a list of all precipitation data"""
    # Query all precipitation data
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(measurements.date, measurements.prcp).\
    filter(measurements.date >= last_twelve_months).\
    order_by(measurements.date).all()

    prcp_list = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
    
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)
    



@app.route("/api/v1.0/tobs")
def tobs():

    """Return a list of temperature observations (TOBS) for the previous year"""
    # Query all station names
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)
 
    results = session.query(measurements.date,measurements.tobs).\
    filter(measurements.date >= last_twelve_months).\
    filter(measurements.station == "USC00519281").\
    order_by(measurements.date).all()
    

    temp_list = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp[0]
        temp_dict["tobs"] = temp[1]
    
        temp_list.append(temp_dict)

    return jsonify(temp_list)  

    

if __name__ == '__main__':
    app.run(debug=True)
