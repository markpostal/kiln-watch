from flask import Flask, render_template, jsonify, send_from_directory
from .Observations import Observations

# Create an instance of the Flask class
app = Flask(__name__)

@app.route("/")
def index():
    page_title = "Kiln Watch"
    return render_template('index.html', title=page_title)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static','favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/static/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('static', path)

@app.route("/records")
def get_data():
    """
    Retrieve the recorded temperature measurements
    """
    data = Observations().data()
    return jsonify(data)


