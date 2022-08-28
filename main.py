#PDF Readers
from io import BytesIO
from backend.PDFreaders import readPDFCrestWell, FirebaseToJSON

#Web App framework for python
from flask import Flask, request, render_template
import flask
from flask_cors import CORS

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
        if((f.filename)[-3:] not in ALLOWED_EXTENSIONS):
            resp = {"success": False, "response": "Not a valid file type"}
            return flask.jsonify(resp)
        fObj = BytesIO(f.stream.read())
        readPDFCrestWell(fObj)
        resp = {"success": True, "response": "file saved!"}
        return flask.jsonify(resp)
    resp = {"success": True, "response": "Non-post"}
    return flask.jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
