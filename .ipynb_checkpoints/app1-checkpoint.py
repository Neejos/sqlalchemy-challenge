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





from flask import Flask

app=Flask(__name__)

@app.route("/")
def home()
    return(f"Welcome to the Home Page<br/>"
        f"The following are the available links:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end>")
if __name__ == "__main__":
    app.run(debug=True)

    