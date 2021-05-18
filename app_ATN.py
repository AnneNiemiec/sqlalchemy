# 1. import Flask
from flask import Flask,jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

# Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")

def last_year_prcp():
    query_date= dt.date(2017,8,23) - dt.timedelta(days=365)
    recent_data=session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= query_date).all()
    myDict = {date:prcp for date,prcp in recent_data}
    return jsonify(myDict)


