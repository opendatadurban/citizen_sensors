from flask import Flask, render_template, request, jsonify
import os
import json
from flask_sqlalchemy import SQLAlchemy
from numpy import mean
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Boolean,
    event,
    ARRAY
)


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sensors:sensors@localhost/sensors'

db = SQLAlchemy(app)


class Temperature(db.Model):
    """
    Temperature storage.
    """
    __tablename__ = 'temperatures'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<temp {}>'.format(self.id)

class Humidity(db.Model):
    """
    Humidity storage.
    """
    __tablename__ = 'humidity'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<humid {}>'.format(self.id)

class WindSpeed(db.Model):
    """
    Windspeed storage.
    """
    __tablename__ = 'windspeeds'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<wind_speed {}>'.format(self.id)

class WindDirection(db.Model):
    """
    Wind direction storage.
    """
    __tablename__ = 'winddirections'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<wind_dir {}>'.format(self.id)

class Gas(db.Model):
    """
    Gas storage.
    """
    __tablename__ = 'gases'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<gas {}>'.format(self.id)

class PM10(db.Model):
    """
    PM10 storage.
    """
    __tablename__ = 'pm10s'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<pm_10 {}>'.format(self.id)

class PM25(db.Model):
    """
    PM25 storage.
    """
    __tablename__ = 'pm25s'

    id = Column(Integer, autoincrement=True, primary_key=True)
    values = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<pm_25 {}>'.format(self.id)

@app.route('/')
def hello_world():
    return 'Oh hello!'


@app.route('/data', methods=['GET', 'POST'])
def ewv5000():

    if request.method == 'POST':
        temp = Temperature()
        wind_speed = WindSpeed()
        wind_dir = WindDirection()
        gas = Gas()
        humid = Humidity()
        pm_10 = PM10()
        pm_25 = PM25()
        data = request.get_json()

        temp.values = temp.values + list(data['temp'])
        temp.times = temp.times + list(data['temp_time'])
        temp.sensor_id = temp.sensor_id + list(data['ID'])

        gas.values = gas.values + list(data['gas'])
        gas.times = gas.times + list(data['gas_time'])
        gas.sensor_id = gas.sensor_id + list(data['ID'])

        humid.value = humid.values + list(data['humid'])
        humid.times = humid.times + list(data['temp_time'])
        humid.sensor_id = humid.sensor_id + list(data['ID'])

        wind_speed.values = wind_speed.values + list(data['wind_speed'])
        wind_speed.times = wind_speed.times + list(data['winds_time'])
        wind_speed.sensor_id = wind_speed.sensor_id + list(data['ID'])

        wind_dir.values = wind_dir.values + list(data['wind_dir'])
        wind_dir.times = wind_dir.times + list(data['windd_time'])
        wind_dir.sensor_id = wind_dir.sensor_id + list(data['ID'])

        pm_10.values = pm_10.values + list(data['pm_10'])
        pm_10.times = pm_10.times + list(data['dust_time'])
        pm_10.sensor_id = pm_10.sensor_id + list(data['ID'])

        pm_25.values = pm_25.values + list(data['pm_25'])
        pm_25.times = pm_25.times + list(data['dust_time'])
        pm_25.sensor_id = pm_25.sensor_id + list(data['ID'])


        db.session.add(temp)
        db.session.add(wind_speed)
        db.session.add(wind_dir)
        db.session.add(gas)
        db.session.add(humid)
        db.session.add(pm_10)
        db.session.add(pm_25)
        db.session.commit()

    return render_template('data.html')


@app.route('/_stream', methods=['GET'])
def stream():
    query = db.session.query(Temperature.value).order_by(Temperature.id.desc()).limit(50)[::-1]
    query2 = db.session.query(Rain.value).order_by(Rain.id.desc()).limit(50)[::-1]
    query3 = db.session.query(Gas.value).order_by(Gas.id.desc()).limit(50)[::-1]
    query4 = db.session.query(Humid.value).order_by(Humid.id.desc()).limit(50)[::-1]

    temperature = [[i, x[0]] for i, x in enumerate(query)]
    temperature.insert(0, ['Time', 'Temperature'])

    rain = [[i, x[0]] for i, x in enumerate(query2)]
    rain.insert(0, ['Time', 'Uncalibrated Temp'])

    gas = [[i, x[0]] for i, x in enumerate(query3)]
    gas.insert(0, ['Time', 'Pressure'])

    humidity = [[i, x[0]] for i, x in enumerate(query4)]
    humidity.insert(0, ['Time', 'Humidity'])

    response = {'temperature': temperature, 'rain': rain, 'gas': gas, 'humidity': humidity}

    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
