# ----------------------------i
# 1. SET UP THE FLASK WEATHER APP
# ----------------------------


# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)


# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Welcome Route
@app.route("/")

#Routing information added
def welcome():
	return(
	'''
	f"Welcome to Climate Analysis API!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
	f"/api/v1.0/temp/start/end"
	''')


#<br/> tags and f string formatting in this context is for formatting HTML content on separate lines

#Precipitation Route
@app.route("/api/v1.0/precipitation")

def precipitation():
	# Calculate the date one year ago from the most recent date
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query: get date and precipitation for prev_year
	precipitation = session.query(Measurement.date,Measurement.prcp).\
		filter(Measurement.date >= prev_year).all()
		
	# Create dictionary w/ jsonify()--format results into .JSON
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)



#Stations Route
@app.route("/api/v1.0/stations")

def stations():
	results = session.query(Station.station).all()
	
	# Unravel results
	stations = list(np.ravel(results))
	return jsonify(stations=stations) 


# Tobs Route
app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



#Statistics Route
# Provide both start and end date routes:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start='2017-06-01',end='2017-06-30'):
	# Query: min, avg, max temps; create list called `sel`, if not given start or end date
	#We know that in this case, end date is 08/23/2017
	
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

	# Add `if-not` statement to determine if no start/end date given
	if not end:
		results = session.query(*sel).\
			filter(Measurement.date >= start).\
			filter(Measurement.date <= end).all()
		temps = list(np.ravel(results))
	    return jsonify(temps=temps)

		#(*sel) - asterik indicates multiple results from query: minimum, average, and maximum temperatures

	# Query: Calc statistics data
	results = session.query(*sel).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()
	temps = list(np.ravel(results))
	return jsonify(temps=temps)


if __name__ == '__main__':
    app.run(debug=True)





    #THE Statistical OUTPUT returns
	# NOTE: Add following to path to address in browser:
		# /api/v1.0/temp/2017-06-01/2017-06-30
		# result: ["temps":[71.0,77.21989528795811,83.0]]