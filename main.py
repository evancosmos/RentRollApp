#PDF Readers
from backend.PDFreaders import readPDFCrestWell, FirebaseToJSON, firebaseConnect

#Output to site/database with json
import json

#Web App framework for python
from flask import Flask, request, flash, redirect, url_for, render_template
import flask
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os

#TODO: Optimize ODR reading, Add user accounts.

UPLOAD_FOLDER = './backend/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods= ['GET', 'POST'])
def helloworld():
    firebaseConnect()
    return render_template("index.html")

@app.route("/users", methods=["GET"])
def users():
    print("users endpoint reached...")
    ret = FirebaseToJSON("TestItem")
    return flask.jsonify(ret)

@app.route('/fileSend', methods=['GET', 'POST'])
def upload_file():
    if(request.method == "POST"):
        print("Got request in static files") 
        print(request.files['static_file'])
        f = request.files['static_file']

        readPDFCrestWell(f.stream.read())
        resp = {"success": True, "response": "file saved!"}
        return flask.jsonify(resp)
    resp = {"success": True, "response": "Non-post"}
    return flask.jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
