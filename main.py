#PDF Readers
from backend.PDFreaders import readPDFCrestWell

#Output to site/database with json
import json

#Hosting Service
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Web App framework for python
from flask import Flask, request, flash, redirect, url_for, render_template
import flask
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os

#TODO: Optimize ODR reading, Generalize the starting 3 chars for Template 1 reading, Get Hosting Fully online, Add user accounts, Connect database to processes. 

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
    return render_template("index.html")

@app.route("/users", methods=["GET"])
def users():
    print("users endpoint reached...")
    with open("backend/out.json", "r") as f:
        data = json.load(f)
    return flask.jsonify(data)

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

def firebaseConnect():
    cred = credentials.Certificate("./backend/firebasekeys.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rent-roll-webapp-default-rtdb.firebaseio.com/"
    })
    return

def JSONToFirebase(JSONfile, DataBaseRef):
    with open(JSONfile, 'r') as f:
        file_contents = json.load(f)

    ref = db.reference(DataBaseRef)
    ref.set(file_contents)
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
