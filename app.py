from flask import Flask, render_template, request, session, logging
import os
from flask_sqlalchemy import SQLAlchemy
from models.data import Temperature, Rain, Gas
from numpy import mean

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


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
