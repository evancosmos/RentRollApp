#PDF Readers
from crypt import methods
from io import BytesIO
from backend.PDFreaders import readPDFCrestWell, FirebaseToJSON

#Web App framework for python
from flask import Flask, request, render_template
import flask
from flask_cors import CORS

#Firebase
import firebase_admin
from firebase_admin import credentials, auth

import os

#TODO: Optimize ODR reading, Finish SignUp/LogIn, Display listings of logged in user.

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods= ['GET', 'POST'])
def helloworld():
    return render_template("index.html")

@app.route("/retriveListings", methods=["GET"])
def listings():
    #TODO: Get the listings for the signed in User
    firebaseConnect()
    ret = FirebaseToJSON("TestItem")
    return flask.jsonify(ret)

@app.route('/fileSend', methods=['GET', 'POST'])
def upload_file():
    if(request.method == "POST"):
        print("Got request in static files") 
        print(request.files['static_file'])
        f = request.files['static_file']
        if((f.filename)[-3:] not in ALLOWED_EXTENSIONS):
            resp = {"success": False, "response": "Not a valid file type"}
            return flask.jsonify(resp)
        fObj = BytesIO(f.stream.read())
        firebaseConnect()
        readPDFCrestWell(fObj)
        resp = {"success": True, "response": "file saved!"}
        return flask.jsonify(resp)
    resp = {"success": True}
    return flask.jsonify(resp), 200

def firebaseConnect():
    if not firebase_admin._apps:
        credPath = os.path.dirname(os.path.abspath(__file__)) + "/firebasekeys.json"
        cred = credentials.Certificate(credPath)
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://rent-roll-webapp-default-rtdb.firebaseio.com/"
        })
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
