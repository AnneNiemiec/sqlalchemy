# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# Use Flask to create your routes.
# import Flask
from flask import Flask,jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os

# See Current Path
print(os.getcwd())
database_path = "./ATN Homework/Resources/hawaii.sqlite"

# create engine to hawaii.sqlite
engine = create_engine(f'sqlite:///{database_path}')

# create engine to hawaii.sqlite
# engine = create_engine(f'sqlite:///{database_path}')

# List all routes that are available.
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine,reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")

# Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
def last_year_prcp():
    query_date= dt.date(2017,8,23) - dt.timedelta(days=365)
    recent_data=session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= query_date).all()
    myDict = {date:prcp for date,prcp in recent_data}
    return jsonify(myDict)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    Station_number=session.query(Station.station).all()
    Station_tuples = [item for t in Station_number for item in t]
    # print(Station_tuples)
    return jsonify(Station_tuples)

# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of stations from the dataset.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def list_of_stations():
    Station_number=session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    Most_Active=Station_number[0]
    query_date= dt.date(2017,8,23) - dt.timedelta(weeks=52)
    active_station=session.query(Measurement.tobs).\
        filter(Measurement.date >= query_date).filter(Measurement.station==Most_Active).all()
    Station_tuples = [item for t in active_station for item in t]
    return jsonify(Station_tuples)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# You will need to join the station and measurement tables for some of the queries.
# Use Flask jsonify to convert your API data into a valid JSON response object.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_observations(start,end=None):
    if end == None:
        Station_number=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        Station_number=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date<=end).all()
    Station_tuples = [item for t in Station_number for item in t]
    return jsonify(Station_tuples)

if __name__ == "__main__":
    app.run(debug=True)

    





