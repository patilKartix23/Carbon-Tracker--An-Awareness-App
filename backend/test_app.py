from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({
        "message": "Climate Tracker API v1.0",
        "status": "running"
    })

@app.route('/test')
def test():
    return jsonify({"test": "success"})

if __name__ == '__main__':
    print("Starting simple test server on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
