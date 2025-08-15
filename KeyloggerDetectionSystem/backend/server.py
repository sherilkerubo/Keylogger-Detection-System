from flask import Flask, jsonify
from flask_cors import CORS
from monitor import scan_system

app = Flask(__name__)
CORS(app)  # Enable CORS so the frontend can access the backend

@app.route('/')
def home():
    return '✅ Keylogger Detection Backend is running!'

@app.route('/scan', methods=['GET'])
def scan():
    try:
        result = scan_system()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
