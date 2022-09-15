#Read text from PDFs
from crypt import methods
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

import json

#Hosting Service
import firebase_admin
from firebase_admin import db

class operatingStatementYear:
    def __init__(self) -> None:
        self.rentalIncome = ""
        self.recoverableOperatingCosts = ""
        self.adminFee = ""
        self.other = ""
        self.parkadeOperations = ""
        self.totalOperatingIncome = ""
        self.year = ""

    def retAsDict(self):
        newDict = {
            "Rental Income": self.rentalIncome,
            "Recoverable Operating Costs": self.recoverableOperatingCosts,
            "Admin Fee": self.adminFee,
            "Other": self.other,
            "Parkcade Operations": self.parkadeOperations,
            "Total Operating Income": self.totalOperatingIncome,
        }
        return newDict

class operatingStatment:
    def __init__(self) -> None:
        self.opYears = {}

    def addYear(self, opStatementYear: operatingStatementYear):
        self.opYears[opStatementYear.year] = opStatementYear.retAsDict()

    def getDict(self):
        return self.opYears

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

def readPDFWestBroad(fObj):
    LAPParms = LAParams(line_overlap=0.1, char_margin=0.1, line_margin=0.1, word_margin=0.1, boxes_flow=None, detect_vertical=False, all_texts=False)
    text = extract_text(fObj, None, None, 0, True, "utf-8", LAPParms)
    textLines = text.splitlines()

    op2017 = operatingStatementYear()
    op2017.year = 2017
    op2016 = operatingStatementYear()
    op2016.year = 2016
    op2015 = operatingStatementYear()
    op2015.year = 2015
    op2014 = operatingStatementYear()
    op2014.year = 2014
    op2013 = operatingStatementYear()
    op2013.year = 2013

    masterDict = {"Budget 2017": {}, "Budget 2016" : {}, "Actual 2015" : {}, "Actual 2014" : {}, "Actual 2013" : {}}
    itemCount = 0

    #What item we are looking at based on bools
    rentalIncomeBool = False
    recoverableOpCostBool = False
    adminFee = False
    otherBool = False

    for line in textLines[:200]: #Since we're reading left to right things look a little ugly in here
        #print(line)
        if(line == ''):
            pass
        elif(rentalIncomeBool):
            if(itemCount == 5):
                op2017.rentalIncome = line
            elif(itemCount == 4):
                op2016.rentalIncome = line
            elif(itemCount == 3):
                op2015.rentalIncome = line
            elif(itemCount == 2):
                op2014.rentalIncome = line
            elif(itemCount == 1):
                op2013.rentalIncome = line
            itemCount-= 1
            if(itemCount < 1):
                rentalIncomeBool = False
        elif(recoverableOpCostBool):
            if(itemCount == 5):
                op2017.recoverableOperatingCosts = line
            elif(itemCount == 4):
                op2016.recoverableOperatingCosts = line
            elif(itemCount == 3):
                op2015.recoverableOperatingCosts = line
            elif(itemCount == 2):
                op2014.recoverableOperatingCosts = line
            elif(itemCount == 1):
                op2013.recoverableOperatingCosts = line
            itemCount-= 1
            if(itemCount < 1):
                recoverableOpCostBool = False
        elif(adminFee):
            if(itemCount == 5):
                op2017.adminFee = line
            elif(itemCount == 4):
                op2016.adminFee = line
            elif(itemCount == 3):
                op2015.adminFee = line
            elif(itemCount == 2):
                op2014.adminFee = line
            elif(itemCount == 1):
                op2013.adminFee = line
            itemCount-= 1
            if(itemCount < 1):
                adminFee = False
        elif(otherBool):
            if(itemCount == 5):
                op2017.other = line
            elif(itemCount == 4):
                op2016.other = line
            elif(itemCount == 3):
                op2015.other = line
            elif(itemCount == 2):
                op2014.other = line
            elif(itemCount == 1):
                op2013.other = line
            itemCount-= 1
            if(itemCount < 1):
                otherBool = False
        elif(line == "Rental Income"): #A new item is made. Address
            rentalIncomeBool = True
            itemCount = 5
        elif(line == "Recoverable Operating Costs"):
            recoverableOpCostBool = True
            itemCount = 5
        elif(line == "Admin Fee"):
            adminFee = True
            itemCount = 5
        elif(line == "Other"):
            otherBool = True
            itemCount = 5

    #Put new item in database
    #JSONToFirebase(json.dumps(allRoll.retMasterDict(), ensure_ascii=False, indent=0, separators=(',', ':')), "TestItem")

    masterDict = operatingStatment()
    masterDict.addYear(op2017)
    masterDict.addYear(op2016)
    masterDict.addYear(op2015)
    masterDict.addYear(op2014)
    masterDict.addYear(op2013)
    print(masterDict.getDict())
    return

def readPDFColliers(fObj):
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
    #JSONToFirebase(json.dumps(allRoll.retMasterDict(), ensure_ascii=False, indent=0, separators=(',', ':')), "TestItem")

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

if __name__ == "__main__":
    with open("../TestRolls/Operating Statements/Broadway - NOI - Commercial.pdf", "rb") as f:
        allRoll = readPDFWestBroad(f)

    #out_file = open("out.json", "w")
    #json.dump(allRoll.retMasterDict(), out_file, ensure_ascii=False, indent=0, separators=(',', ':'))
    #out_file.close()
    