#Read text from PDFs
from crypt import methods
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

import json

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

def readPDFCrestWell(filename): #For this template, a new item is begins when an line starts with "TCC"
    #For this template, I have to iterate twice to get pdfminersix to read Base rent correctly. See difference in LAPParms
    LAPParmsBR = LAParams(0.5, 2, 0.2, 0.1, None, False, False)
    textBR = extract_text(filename, None, None, 0, True, "utf-8", LAPParmsBR)
    textLinesBR = textBR.splitlines()

    loopedOnce = False
    BaseRentDict = {}
    brLineItem = ""
    brCount = 0
    oldLeaseNum = ""
    validCodes = ["TCC", "SPA", "WBC", "SPR", "LAK"]

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
        elif((line[:9] == "Base Rent") and (loopedOnce)):
            brLineItem += line
            brCount = 1
        elif(brCount > 0):
            brLineItem = brLineItem + " " + line
            brCount += 1
            if(brCount > 3):
                brLineItem += ". "
                brCount = 0
    BaseRentDict[oldLeaseNum] = brLineItem

    LAPParms = LAParams(0.5, 2, 0.2, 0.1, 0.5, False, False)
    text = extract_text(filename, None, None, 0, True, "utf-8", LAPParms)
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
    rollToJSON(allRoll)
    return allRoll

def rollToJSON(rentRoll):

    x = rentRoll.retMasterDict()

    #To out.json:
    filename = 'backend/out.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(x, f, ensure_ascii=False, indent=4)

    return filename