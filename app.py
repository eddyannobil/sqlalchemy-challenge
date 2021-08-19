
import datetime as dt
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
# Temperature Function
#################################################
def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.

        Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
        TMIN, TAVG, and TMAX
        """
        session = Session(engine)
        return session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start_date).filter(measurements.date <= end_date).all()
        
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )   


@app.route("/api/v1.0/precipitation")
def prcp():
    
    """Return a list of all precipitation data"""
    # Query all precipitation data
    session = Session(engine)
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(measurements.date, measurements.prcp).\
    filter(measurements.date >= last_twelve_months).\
    order_by(measurements.date).all()

    prcp_list = []
    #prcp_list = dict(results)
    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
    
        prcp_list.append(prcp_dict)
    
    session.close()
    return jsonify(prcp_list)
    

@app.route("/api/v1.0/stations")
def mystations():
    
    """Return a list of all station names"""
    # Query all station names
    session = Session(engine)
    results = session.query(stations.station,stations.name).all()
    
    station_list = []
    #station_list = dict(results)
    for station in results:
        station_dict = {}
        station_dict["station"] = station[0]
        station_dict["name"] = station[1]
    
        station_list.append(station_dict)

    session.close()
    return jsonify(station_list)
    

@app.route("/api/v1.0/tobs")
def mytobs():

    """Return a list of temperature observations (TOBS) for the previous year"""
    # Query all the dates and temperature observations of the most active station for the last year of data
    session = Session(engine)
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)
 
    results = session.query(measurements.date,measurements.tobs).\
    filter(measurements.date >= last_twelve_months).\
    filter(measurements.station == "USC00519281").\
    order_by(measurements.date).all()
    

    temp_list = []
    #temp_list = dict(results)
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp[0]
        temp_dict["tobs"] = temp[1]
    
        temp_list.append(temp_dict)

    session.close()

    return jsonify(temp_list)  

@app.route("/api/v1.0/<start_date>")
def start(start_date):

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start"""
    # Query all list of the minimum temperature, the average temperature, and the max temperature for a given start.
    session = Session(engine)

    results = (calc_temps(start_date,start_date))
 
    

    temp_list = []
      #temp_list = dict(results)  
    for temp in results:
        temp_dict = {}
        temp_dict["min"] = temp[0]
        temp_dict["avg"] = temp[1]
        temp_dict["max"] = temp[2]
    
        temp_list.append(temp_dict)
    
    session.close()
    return jsonify(temp_list)     

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start and start-end range"""
    # Query all list of the minimum temperature, the average temperature, and the max temperature for a given start and start-end range.
    session = Session(engine)
    results = (calc_temps(start,end))
 
    temp_list = []
      #temp_list = dict(results)
    for temp in results:
        temp_dict = {}
        temp_dict["min"] = temp[0]
        temp_dict["avg"] = temp[1]
        temp_dict["max"] = temp[2]
    
        temp_list.append(temp_dict)
    
    session.close()
    return jsonify(temp_list)     

if __name__ == '__main__':
    app.run(debug=True)
