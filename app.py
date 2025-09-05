from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/upload", methods = ["POST"]) # when in the adress of localhost5000 + /upload there is a POST request

def upload_video():
    # return a JSON string that represent an object
    return jsonify({
        "stress_level": "medium"
    })
