import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def welcome():
 return(
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation"
         f"<br/>"
        f"/api/v1.0/stations"
         f"<br/>"
        f"/api/v1.0/tobs"
         f"<br/>"
        f"/api/v1.0/<start>"
         f"<br/>"
        f"/api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation():
           # Create our session (link) from Python to the DB
    session = Session(engine)

    precipitation_score = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >='2016-08-23').filter(Measurement.date <='2017-08-24').order_by(Measurement.date).all()
    session.close()
    percp_total = []

    for date, prcp in precipitation_score: 
        perc_date = {}
        perc_date["date"] = date
        perc_date["prcp"] = prcp
        percp_total.append(perc_date)
    return jsonify(percp_total)

@app.route("/api/v1.0/stations")
def stations (): 
    session = Session(engine)

    station_count=session.query(Station.name,Station.station)
    session.close()
    stations = []
    for name,station in station_count:
        station_total={}
        station_total["name"] = name 
        station_total["station"] = station 
        stations.append(station_total)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs(): 
    session = Session(engine)
    last_date_entered=session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    query_date=dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation_score = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >='2016-08-23').filter(Measurement.date <='2017-08-24').order_by(Measurement.date).all()
    session.close()
    tobs = []
    for date, prcp in precipitation_score:
        perc_total = {}
        perc_total["date"] = date 
        perc_total["prcp"] = prcp 
        tobs.append(perc_total)
    return jsonify(tobs)

@app.route ("/api/v1.0/<start>")
def start1(start): 
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    input_date = start - one_year
    end_date = dt.date(2017,8,23)
    trip_data=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= input_date).filter(Measurement.date <= end_date).all()
    trip = list(trip_data)
    return jsonify(trip)


@app.route ("/api/v1.0/<start>/<end>")
def startend(start,end): 
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end=dt.datetime.strptime(end, '%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    input_start_date = start - one_year
    input_end_date = end - one_year
    trip_data=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= input_start_date).filter(Measurement.date <= input_end_date).all()
    trip = list(trip_data)
    return jsonify(trip)
if __name__ == "__main__":
    app.run(debug=True)   