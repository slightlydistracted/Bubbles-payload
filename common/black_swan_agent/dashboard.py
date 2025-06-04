import json
import time
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Path to your smart wallet file
SMART_WALLET_FILE = 'smart_wallets.json'

# Read the smart wallets from the JSON file
def get_smart_wallets():
    try:
        with open(SMART_WALLET_FILE, 'r') as file:
            wallets = json.load(file)
        return wallets
    except Exception as e:
        return f"Error loading wallets: {e}"

# Update the dashboard with the smart wallets
def update_wallets():
    wallets = get_smart_wallets()
    return wallets

# Route to render the main dashboard page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event for updating wallets in real-time
@socketio.on('connect')
def handle_connect():
    print('Client connected, sending wallet updates')
    while True:
        wallets = update_wallets()  # Get latest wallets
        socketio.emit('wallet_update', wallets)  # Send update to client
        time.sleep(5)  # Delay for 5 seconds before sending the next update

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
