## Arghavan Abtahi

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App<br/>"
        f"Here are your options:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/*startdate*<br/>"
        f"/api/v1.0/*startdate*/*enddate*<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    percipit = db_session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.asc()).all()
    return jsonify(percipit)

@app.route("/api/v1.0/stations")
def stations():
    stations = db_session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    tobs = db_session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.asc()).all()
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    start = db_session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    start_end = db_session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).group_by(Measurement.date).all()
    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)

