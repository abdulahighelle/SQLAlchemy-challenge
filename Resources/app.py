from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")
conn= engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
        return (
        f"Welcome to the Hawaii Climate Analysis API!<br><br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
            )

#Convert the query results to a dictionary using `date` as the key and `prcp` as the value.


@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()

    precip_list = []    
    for precip_data in precip_data:
        precip_dict = {}
        precip_dict["date"] = precip_data.date
        precip_dict["prcp"] = precip_data.prcp
        precip_list.append(precip_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    
    Station_list = session.query(Station.name).all()
    
    station_names = list(np.ravel(Station_list))
    
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    
# Query the dates and temperature observations of the most active station for the previous year of data.
    
    temp_data = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).all()

    temp_list = []    
    for temp_data in temp_data:
        temp_dict = {}
        temp_dict["date"] = temp_data.date
        temp_dict["tobs"] = temp_data.tobs
        temp_list.append(temp_dict)


# Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(temp_list)



# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.



# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

@app.route("/api/v1.0/<start>")
def start(start):
    s_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start)
    
    start_list = list(np.ravel(s_temps))

    
    return jsonify(start_list)



# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    s_e_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end)
    
    startend_list = list(np.ravel(s_e_temps))
    
    return jsonify(startend_list)



if __name__ == "__main__":
    app.run(debug=True)