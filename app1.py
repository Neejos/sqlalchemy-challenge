import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()


# reflect the tables
Base.prepare(engine,reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurements=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Design a query to retrieve the last 12 months of precipitation data.
date=dt.datetime(2016, 7,31) #
measurement_data=session.query(Measurements.date,Measurements.prcp).filter(Measurements.date >date).all()

# Unpack the `date` and `prcp` from measurements_data and save into separate lists
date_info=[row[0] for row in measurement_data]
prcp_info=[row[1] for row in measurement_data]

dict1=dict(zip(date_info,prcp_info))
dict1

# List the stations and the counts in descending order
session2=Session(engine)
stats=[Measurements.station,
      func.min(Measurements.tobs),
      func.max(Measurements.tobs),
      func.avg(Measurements.tobs),
      func.count(Measurements.tobs)]
active_station=session2.query(*stats).\
        group_by(Measurements.station).\
        order_by(func.count(Measurements.tobs).desc()).all()

stations=[row[0] for row in active_station]
most_active_station=stations[0]

session3=Session(engine)
temps=


from flask import Flask,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    return(f"Welcome to the Home Page<br/>"
    
        f"The following are the available links:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startDate<br/>"
        f"/api/v1.0/startDate/endDate>")

@app.route("/api/v1.0/precipitation")
def precipitation_data():
    """Return the dates and the precipitation data as json"""
    return jsonify(dict1)

@app.rote("/api/v1.0/stations")
def stations_names():
    return jsonify(stations)

@app.route("/api/v1.0/tobs<br/>")
def temp():
    return



if __name__ == "__main__":
    app.run(debug=True)

    