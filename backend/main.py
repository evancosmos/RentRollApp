#Read text from PDFs
from crypt import methods
from pdfminer.high_level import extract_text

#Output to site/database with json
import json

#Hosting Service
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Web App framework for python
from flask import Flask, request
import flask
from flask_cors import CORS

#TODO: Train ODR, Fix data collection fron PDF Template 1

class rentRollEntity: #Individual Items on a Rent Roll
    def __init__(self):
        self.leaseNum = ""
        self.operatingName = ""
        self.sqrFt = ""
        self.status = ""
        self.renOption = ""
        self.leaseExpire = ""
        self.renNotice = ""
        self.origCom = ""
        self.baseRentLines = ""

    def retAsDict(self):
        newDict = {
            "Lease": self.leaseNum,
            "Operating Name": self.operatingName,
            "Square Feet": self.sqrFt,
            "Status": self.status,
            "Renewal Option": self.renOption,
            "Lease Expires": self.leaseExpire,
            "Renewal Notice": self.renNotice,
            "Origination Com": self.origCom
        }
        return newDict

class rentRoll: #The collection of items on a rent roll
    def __init__(self) -> None:
        self.rolls = []

    def addRoll(self, newRoll):
        self.rolls.append(newRoll)

    def retMasterDict(self):
        newMasterDict = {}
        id = 0
        for roll in self.rolls:
            newMasterDict[str(id)] = roll.retAsDict()
            id += 1
        return newMasterDict

#Flask START
def flaskConnect():
    app = Flask(__name__)
    CORS(app)
        
    @app.route("/")
    def helloworld():
        return "Hello World!"

    @app.route("/users", methods=["GET"])
    def users():
        print("users endpoint reached...")
        with open("out.json", "r") as f:
            data = json.load(f)
        return flask.jsonify(data)

    app.run()
    return

#Firebase START
def firebaseConnect():
    cred = credentials.Certificate("./firebasekeys.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rent-roll-webapp-default-rtdb.firebaseio.com/"
    })
    return

def JSONToFire(JSONfile, DataBaseRef):
    with open(JSONfile, 'r') as f:
        file_contents = json.load(f)

    ref = db.reference(DataBaseRef)
    ref.set(file_contents)
    return

def readPDFTemplate1(filename): #For this template, a new item is begins when an line starts with "TCC"
    text = extract_text(filename)
    textLines = text.splitlines()
    #Once "TCC" is read from the start of a line, make a new roll
    allRoll = rentRoll()
    itemCount = 0
    for line in textLines[:500]: #Remember to remove the :500 limiter after testing
        #print(line)
        if(line == ''):
            itemCount = itemCount - 1
        elif(line[:3] == "TCC"): #A new item is made.
            newRoll = rentRollEntity()
            newRoll.leaseNum = line
        elif(itemCount == 1):
            newRoll.operatingName = line
        elif(itemCount == 2):
            newRoll.sqrFt = line
        elif(itemCount == 3):
            newRoll.status = line
        elif(itemCount == 4):
            pass
        elif(itemCount == 5):
            newRoll.renOption = line
        elif(itemCount == 6):
            pass
        elif(itemCount == 7):
            newRoll.leaseExpire = line
        elif(itemCount == 8):
            pass
        elif(itemCount == 9):
            newRoll.renNotice = line
        elif(itemCount == 10):
            pass
        elif(itemCount == 11):
            newRoll.origCom = line
            allRoll.addRoll(newRoll)
            itemCount = -1
        else:
            itemCount = itemCount - 1
        itemCount += 1

    return allRoll

def rollToJSON(rentRoll):

    x = rentRoll.retMasterDict()

    #To out.json:
    filename = 'out.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(x, f, ensure_ascii=False, indent=4)

    return filename

def main():
    #readImage('1650 lease rent roll.png')
    flaskConnect()
    gotRoll = readPDFTemplate1('2018-05-16 - Tamarack - Base Rent Roll.pdf')
    jsonRolls = rollToJSON(gotRoll)

    firebaseConnect()
    JSONToFire(jsonRolls, 'Test12')

if __name__ == "__main__":
    main()