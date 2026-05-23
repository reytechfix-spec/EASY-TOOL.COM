# app.py
import os
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*")

# Weka routes zako hapa...

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
