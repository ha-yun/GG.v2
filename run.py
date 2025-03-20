import eventlet
eventlet.monkey_patch() 

from flask import Flask, render_template
from flask_socketio import SocketIO
from socket_service import socketio

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, debug=True, port=5000, host="0.0.0.0")
