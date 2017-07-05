from flask import Flask, render_template, request, session, logging
import os
from flask_sqlalchemy import SQLAlchemy
from numpy import mean
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Boolean,
    event,
)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Temperature(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'temperatures'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<temp {}>'.format(self.id)


class Rain(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'rains'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<rain {}>'.format(self.id)


class Gas(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'gases'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<gas {}>'.format(self.id)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


@app.route('/')
def hello_world():
    return 'Oh hello!'


@app.route('/ewok-village-5000', methods=['GET', 'POST'])
def ewv5000():

    if request.method == 'POST':
        data = request.get_json()
        temp = Temperature()
        rain = Rain()
        gas = Gas()
        temp.value = mean(data['temp'])
        rain.value = mean(data['rain'])
        gas.value = mean(data['gas'])

        db.session.add(temp)
        db.session.add(rain)
        db.session.add(gas)
        db.session.commit()

    return render_template('ewok.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
