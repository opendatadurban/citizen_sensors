from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Oh hello!'


@app.route('/ewok-village-5000')
def ewv5000():

    return render_template('ewok.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
