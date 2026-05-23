from flask import Flask, render_template, jsonify, request
import os
import hashlib
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey12345'

# File za kuhifadhi data
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # Default admin account
    return {
        "REYTECHFX": {
            "password": hashlib.sha256("valentina241".encode()).hexdigest(),
            "email": "reytechfix@gmail.com",
            "role": "admin",
            "is_active": True
        }
    }

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "EASY TOOL API is running!",
        "version": "0.02",
        "endpoints": {
            "/": "Home page",
            "/api/login": "Login endpoint (POST)",
            "/api/status": "API status",
            "/api/test": "Test endpoint"
        }
    })

@app.route('/api/status')
def status():
    return jsonify({"status": "online", "message": "Server is running"})

@app.route('/api/test')
def test():
    return jsonify({"success": True, "message": "API is working!"})

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"})
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"success": False, "error": "Username and password required"})
        
        users = load_users()
        
        if username not in users:
            return jsonify({"success": False, "error": "Invalid username or password"})
        
        user = users[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user['password'] != password_hash:
            return jsonify({"success": False, "error": "Invalid username or password"})
        
        return jsonify({
            "success": True,
            "username": username,
            "role": user.get('role', 'user'),
            "message": f"Welcome {username}!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
