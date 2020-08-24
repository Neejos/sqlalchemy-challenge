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


from flask import Flask,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    return(f"Welcome to the Home Page<br/>"
    
        f"The following are the available links:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temps: /api/v1.0/tobs<br/>"
        f"Temp_Summary for days after the entered date: /api/v1.0/startDate/<br/>"
        f"Temp_Summary for a days between the dates entered: /api/v1.0/startDate/endDate/")

# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Design a query to retrieve the last 12 months of precipitation data.


@app.route("/api/v1.0/precipitation")
def precipitation_data():
    session1=Session(engine)
    """Return the dates and the precipitation data as json"""
    
    date=dt.date(2016, 7,31) # 12 month before the last date recorded in the given data
    measurement_data=session1.query(Measurements.station,Measurements.date,Measurements.prcp).filter(Measurements.date >date).all()
    session1.close()
    return jsonify(measurement_data)

# List the stations and the no of readings per station in descending order to find the most active station
@app.route("/api/v1.0/stations")
def stations_names():
    session2=Session(engine)
    stats=[Measurements.station,
      func.count(Measurements.tobs)]
    active_stations=session2.query(*stats).\
        group_by(Measurements.station).\
        order_by(func.count(Measurements.tobs).desc()).all()
    all_stations = []
    for station_info,count_info in active_stations:
        tobs_dict = {}
        tobs_dict["station_id"] = station_info
        tobs_dict["count_info"] = count_info
        all_stations.append(tobs_dict)

    stations=[row[0] for row in active_stations]
    most_active_station=stations[0]
    session2.close()
    print(f"The most active station is {most_active_station}")
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():
    session3=Session(engine)
    most_active_station="USC00519281"
    temps=session3.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.station==most_active_station).\
        filter(func.strftime("%Y",Measurements.date)=="2016").all()
    
    return jsonify(temps)

#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/startDate/<Date>")
def summary(Date):
    session4=Session(engine)
    sel1=[Measurements.date,
        func.min(Measurements.tobs),
        func.avg(Measurements.tobs),
        func.max(Measurements.tobs)]
    result=session4.query(*sel1).\
        filter(func.strftime("%Y-%m-%d",Measurements.date)>= func.strftime("%Y-%m-%d",Date)).\
        group_by(Measurements.date).all()
    
    all_Temps = []
    for date_info,Tmin_info,Tavg_info,Tmax_info in result:
        all_dict = {}
        all_dict["date_info"] = date_info
        all_dict["Tmin_info"] = Tmin_info
        all_dict["Tavg_info"] = Tavg_info
        all_dict["Tmax_info"] = Tmax_info

        all_Temps.append(all_dict)
    
    return jsonify(all_Temps)

@app.route("/api/v1.0/startDate/endDate/<StartDate>/<EndDate>")
def summary1(StartDate,EndDate):
    session5=Session(engine)
    sel2=[Measurements.date,
        func.min(Measurements.tobs),
        func.avg(Measurements.tobs),
        func.max(Measurements.tobs)]
    result1=session5.query(*sel2).\
        filter(func.strftime("%Y-%m-%d",Measurements.date)>= func.strftime("%Y-%m-%d",StartDate)).\
        filter(func.strftime("%Y-%m-%d",Measurements.date)< func.strftime("%Y-%m-%d",EndDate)).\
        group_by(Measurements.date).all()
    

    all_Temps1 = []
    for date_info,Tmin_info,Tavg_info,Tmax_info in result1:
        all_dict1 = {}
        all_dict1["date_info"] = date_info
        all_dict1["Tmin_info"] = Tmin_info
        all_dict1["Tavg_info"] = Tavg_info
        all_dict1["Tmax_info"] = Tmax_info

        all_Temps1.append(all_dict1)
    
    return jsonify(all_Temps1)

    

    


if __name__ == "__main__":
    app.run(debug=True)

    