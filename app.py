from flask import Flask, render_template, request, session, logging
import os

app = Flask(__name__)


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
        app.logger.info('data: %s', request.data)

    return render_template('ewok.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
