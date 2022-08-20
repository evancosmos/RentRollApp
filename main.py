#Read text from PDFs
from pdfminer.high_level import extract_text

#Output to site/database with json
import json

#Read text from images https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
from PIL import Image
from pytesseract import pytesseract #Requires the tesseract executable on the system. https://linuxhint.com/install-tesseract-ocr-linux/

#Hosting Service
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Web App framework for python
from flask import Flask, request

#FLASK START
""" app = Flask(__name__)
    
@app.route("/", methods=['GET', 'POST'])
def helloworld():
    if request.method == 'POST':
        f = request.files['the_file'] #Get the file, send it to database

    return "<p>Hello World<p> <button>Upload</button> <button>Upload</button>" """
#FLASK END

#TODO: Train ODR, Set up database connections, Set up frontend connections.

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

def readImage(filename):
    img = Image.open(filename)

    text = pytesseract.image_to_string(img)

    print(text)
    allRoll = rentRoll()
    return allRoll

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
        elif(line[0:3] == "TCC"): #A new item is made
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
    gotRoll = readPDFTemplate1('2018-05-16 - Tamarack - Base Rent Roll.pdf')
    jsonRolls = rollToJSON(gotRoll)

    firebaseConnect()
    JSONToFire(jsonRolls, 'Test12')

if __name__ == "__main__":
    main()
