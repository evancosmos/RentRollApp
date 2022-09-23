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

#TODO: Add readers more templates.

#For each rent roll, there are mutlbile tenants. For each tenant, extract this info to a python dictionary:
#Operating Name, Unit, Base Rent, Monthly Rent, Annual Rent, Area, Start Date, End Date, Term, Escalation Date. See MS Teams for alternate names these might be under.
#In the case of missing values add a blank string.

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


    LAPParms = LAParams(line_overlap=0.5, char_margin=2, line_margin=0.4, word_margin=0.1, boxes_flow=0.2, detect_vertical=False, all_texts=False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()

    return

def readPDFCrestWell(fObj, user): #For this template, a new item is begins when an line starts with "TCC"
    #For this template, I have to iterate twice to get pdfminersix to read Base rent correctly. See difference in LAPParms

    masterDict = {}

    LAPParmsBR = LAParams(0.5, 2, 0.2, 0.1, None, False, False)
    textBR = extract_text(fObj, None, None, 0, True, "utf-8", LAPParmsBR)
    textLinesBR = textBR.splitlines()

    loopedOnce = False
    BaseRentDict = {}
    BaseRentEntityDict = {}
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
                BaseRentDict[oldLeaseNum] = BaseRentEntityDict
                BaseRentEntityDict = {}
            oldLeaseNum = line
            loopedOnce = True
        elif((line[:9] in validRentInfo) and (loopedOnce)):
            BaseRentEntityDict["Years"] = line
            brCount = 1
        elif(brCount == 1):
            BaseRentEntityDict["Begin Date"] = line
            brCount += 1
        elif(brCount == 2):
            BaseRentEntityDict["End Date"] = line
            brCount += 1
        elif(brCount == 3):
            BaseRentEntityDict["Rate"] = line
            brCount = 0
            
    BaseRentDict[oldLeaseNum] = BaseRentEntityDict

    LAPParms = LAParams(0.5, 1.5, 0.2, 0.1, 0.9, False, False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()
    #Once "TCC" is read from the start of a line, make a new roll
    itemCount = 0
    brCount = 0

    for line in textLines:
        #print(line)
        if(line == ''):
            itemCount = itemCount - 1
        elif(line[:3] in validCodes): #A new item is made.
            curItemDict = {}
            curItemDict["Lease Number"] = line
        elif(itemCount == 1):
            curItemDict["Operating Name"] = line
        elif(itemCount == 2):
            curItemDict["Area"] = line
        elif(itemCount == 3):
            curItemDict["Status"] = line
        elif(itemCount == 4):
            pass
        elif(itemCount == 5):
            curItemDict["Renewal Date"] = line
        elif(itemCount == 6):
            pass
        elif(itemCount == 7):
            curItemDict["Lease Expire"] = line
        elif(itemCount == 8):
            pass
        elif(itemCount == 9):
            curItemDict["Renewal Notice"] = line
        elif(itemCount == 10):
            pass
        elif(itemCount == 11):
            curItemDict["Ori Com"] = line
            itemCount = -1
            try:
                curItemDict["Base Rent"] = BaseRentDict[curItemDict["Lease Number"]]
            except:
                curItemDict["Base Rent"] = "Missing Base Rent Data"
            indexNameForMaster = (curItemDict["Operating Name"]).replace("#", "")
            masterDict[indexNameForMaster] = curItemDict
        else:
            itemCount = itemCount - 1
        itemCount += 1

    #Put new item in database
    JSONToFirebase(json.dumps(masterDict, ensure_ascii=False, indent=0, separators=(',', ':')), user)

    return masterDict

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
    elif(text[:8] == "Actuals "):
        readPDFCrestWell(fObj, user)

    return

if __name__ == "__main__":
    """ with open("../TestRolls/Operating Statements/Broadway - NOI - Commercial.pdf", "rb") as f:
        allRoll = chooseReader(f)

    with open("../TestRolls/Colliers/Broadway Commercial Rent Roll.pdf", "rb") as f:
        allRoll = chooseReader(f)"""

    """ with open("../TestRolls/Crestwell/2018-05-16 - Depot 170 - Base Rent Roll.pdf", "rb") as f:
        allRoll = chooseReader(f) """

    """ out_file = open("out.json", "w")
    json.dump(allRoll, out_file, ensure_ascii=False, indent=0, separators=(',', ':'))
    out_file.close() """
    