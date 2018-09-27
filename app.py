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


class WindSpeed(db.Model):
    """
    Windspeed storage.
    """
    __tablename__ = 'windspeeds'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(ARRAY(Float), nullable=False)
    times = Column(ARRAY(DateTime), nullable=False)
    date = Column(Date, nullable=False)
    sensor_id = Column(String, nullable=False)

    def __repr__(self):
        return '<wind_speed {}>'.format(self.id)


@app.route('/')
def hello_world():
    return 'Oh hello!'


@app.route('/data', methods=['GET', 'POST'])
def ewv5000():

    if request.method == 'POST':
        temp = Temperature()
        rain = Rain()
        gas = Gas()
        humid = Humid()
        data = request.get_json()

        temp.values = temp.values + list(data['temp'])
        rain.value = data['rain']
        gas.value = data['press']
        humid.value = data['humid']

        db.session.add(temp)
        db.session.add(rain)
        db.session.add(gas)
        db.session.add(humid)
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
