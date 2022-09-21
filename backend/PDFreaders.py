#Read text from PDFs
from asyncore import read
from crypt import methods
from doctest import master
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

import json

#Hosting Service
import firebase_admin
from firebase_admin import db

#TODO: Replace rent roll classes with dicts for readability.

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
            "Origination Com": self.origCom,
            "Rent Info": self.baseRentLines
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

def readPDFWestBroad(fObj, user):
    LAPParms = LAParams(line_overlap=0.1, char_margin=0.1, line_margin=0.1, word_margin=0.1, boxes_flow=None, detect_vertical=False, all_texts=False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()

    masterDict = {"Budget 2017": {}, "Budget 2016" : {}, "Actual 2015" : {}, "Actual 2014" : {}, "Actual 2013" : {}}
    yearMax = len(masterDict)
    
    #Loop vars
    itemLeftCount = 0
    curHead = ""

    for line in textLines: #Since we're reading left to right things look a little ugly in here
        line = line.replace(",", "")
        #print(line)
        if(line == ''):
            pass
        elif(itemLeftCount == (yearMax - 1)):
            masterDict["Budget 2016"][curHead] = line
            itemLeftCount -= 1
        elif(itemLeftCount == (yearMax - 2)):
            masterDict["Actual 2015"][curHead] = line
            itemLeftCount -= 1
        elif(itemLeftCount == (yearMax - 3)):
            masterDict["Actual 2014"][curHead] = line
            itemLeftCount -= 1
        elif(itemLeftCount == (yearMax - 4)):
            masterDict["Actual 2013"][curHead] = line
            itemLeftCount -= 1
        elif(line.isnumeric()):
            masterDict["Budget 2017"][curHead] = line
            itemLeftCount = yearMax - 1
        else:
            curHead = line
            if(line == "ACTUAL "):
                curHead = "Year"

    #Put new item in database
    JSONToFirebase(json.dumps(masterDict, ensure_ascii=False, indent=0, separators=(',', ':')), user)

    return masterDict

def readPDFColliers(fObj, user):
    LAPParms = LAParams(line_overlap=0.5, char_margin=2, line_margin=0.4, word_margin=0.1, boxes_flow=0.2, detect_vertical=False, all_texts=False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()

    allRoll = rentRoll()
    itemCount = 0
    brCount = 0
    newRoll = rentRollEntity()

    for line in textLines:
        #print(line)
        if(line == ''):
            itemCount = itemCount - 1
        elif(line[:4].isnumeric()): #A new item is made. Address
            newRoll = rentRollEntity()
            newRoll.leaseNum = line
        elif(itemCount == 1): #Op Name
            newRoll.operatingName = line
        elif(itemCount == 2): #Sqr Ft
            newRoll.sqrFt = line
        elif(itemCount == 3): #Commencement Date
            newRoll.status = line
        elif(itemCount == 4): #Expiration Date
            pass
        elif(itemCount == 5): #Term
            newRoll.renOption = line
        elif(itemCount == 6): #Escalation Date
            pass
        elif(itemCount == 7): #Base Rent
            newRoll.leaseExpire = line
        elif(itemCount == 8): #Current Annual Rate
            pass
        elif(itemCount == 9): #Renewal Options
            newRoll.renNotice = line
        elif(itemCount == 10):
            pass
        else:
            itemCount = itemCount - 1
        itemCount += 1

    allRoll.addRoll(newRoll)

    #Put new item in database
    JSONToFirebase(json.dumps(allRoll.retMasterDict(), ensure_ascii=False, indent=0, separators=(',', ':')), user)

    return allRoll

def readPDFCrestWell(fObj, user): #For this template, a new item is begins when an line starts with "TCC"
    #For this template, I have to iterate twice to get pdfminersix to read Base rent correctly. See difference in LAPParms

    LAPParmsBR = LAParams(0.5, 2, 0.2, 0.1, None, False, False)
    textBR = extract_text(fObj, None, None, 0, True, "utf-8", LAPParmsBR)
    textLinesBR = textBR.splitlines()

    loopedOnce = False
    BaseRentDict = {}
    brLineItem = ""
    brCount = 0
    oldLeaseNum = ""
    validCodes = ["TCC", "SPA", "WBC", "SPR", "LAK", "COR", "DEP"]
    validRentInfo = ["Base Rent", "Free Rent", "Fixturing", "Month to "]

    for line in textLinesBR:
        #print(line)
        if(line == ''):
            pass
        elif(line[:3] in validCodes):
            if(loopedOnce):
                BaseRentDict[oldLeaseNum] = brLineItem
                brLineItem = ""
            oldLeaseNum = line
            loopedOnce = True
        elif((line[:9] in validRentInfo) and (loopedOnce)):
            brLineItem += line
            brCount = 1
        elif(brCount > 0):
            brLineItem = brLineItem + " " + line
            brCount += 1
            if(brCount > 3):
                brLineItem += ". "
                brCount = 0
    BaseRentDict[oldLeaseNum] = brLineItem

    LAPParms = LAParams(0.5, 1.5, 0.2, 0.1, 0.9, False, False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()
    #Once "TCC" is read from the start of a line, make a new roll
    allRoll = rentRoll()
    itemCount = 0
    brCount = 0
    newRoll = rentRollEntity()

    for line in textLines:
        #print(line)
        if(line == ''):
            itemCount = itemCount - 1
        elif(line[:3] in validCodes): #A new item is made.
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
            itemCount = -1
            try:
                newRoll.baseRentLines = BaseRentDict[newRoll.leaseNum]
            except:
                newRoll.baseRentLines = "Missing Base Rent Data"
            allRoll.addRoll(newRoll)
        else:
            itemCount = itemCount - 1
        itemCount += 1

    allRoll.addRoll(newRoll)

    #Put new item in database
    JSONToFirebase(json.dumps(allRoll.retMasterDict(), ensure_ascii=False, indent=0, separators=(',', ':')), user)

    return allRoll

def JSONToFirebase(JSONstr, DataBaseRef):
    print(DataBaseRef)
    ref = db.reference(DataBaseRef)
    ref.set(json.loads(JSONstr))
    return

def FirebaseToJSON(DataBaseRef):
    ref = db.reference(DataBaseRef)
    return ref.get()

def chooseReader(fObj, user="notsignedin"):
    LAPParms = LAParams(line_overlap=0.1, char_margin=0.1, line_margin=0.1, word_margin=0.1, boxes_flow=None, detect_vertical=False, all_texts=False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)

    if(text[:8] == "West Bro"):
        readPDFWestBroad(fObj, user)
    elif(text[:8] == "Rent Rol"):
        readPDFColliers(fObj, user)
    elif(text[:8] == "Actuals "):
        readPDFCrestWell(fObj, user)

    return

if __name__ == "__main__":
    with open("../TestRolls/Operating Statements/Broadway - NOI - Commercial.pdf", "rb") as f:
        allRoll = chooseReader(f)

    with open("../TestRolls/Colliers/Broadway Commercial Rent Roll.pdf", "rb") as f:
        allRoll = chooseReader(f)

    with open("../TestRolls/Crestwell/2018-05-16 - Depot 170 - Base Rent Roll.pdf", "rb") as f:
        allRoll = chooseReader(f)

    """ out_file = open("out.json", "w")
    json.dump(allRoll, out_file, ensure_ascii=False, indent=0, separators=(',', ':'))
    out_file.close() """
    