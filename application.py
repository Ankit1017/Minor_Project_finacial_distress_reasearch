from flask import Flask, Response, render_template, request, stream_with_context,url_for,redirect
from dqn_data_visiualizer import dqn_based_data
from bat_data_visualizer import bat_reduced_data
application = Flask(__name__)
@application.route("/")
def index1() -> str:
    return render_template("home.html")
@application.route('/dqn')
def index() -> str:
    return render_template('index1.html')
@application.route('/start', methods=['POST'])
def start() -> str:
    file_path = request.form['file_path']
    return redirect(url_for('display', file_path=file_path))
@application.route('/display')
def display() -> str:
    return render_template('display.html')
@application.route('/stream')
def stream() -> str:
    file_path = request.args.get('file_path')
    return Response(stream_with_context(dqn_based_data(file_path)), mimetype='text/event-stream')
@application.route("/at")
def index2() -> str:
    return render_template("index.html")
@application.route("/chart-data")
def chart_data() -> Response:
    response = Response(stream_with_context(bat_reduced_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response