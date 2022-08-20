#Read text from PDFs
from pdfminer.high_level import extract_text
#Read text from images https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
from PIL import Image
from pytesseract import pytesseract #Requires the tesseract executable on the system.

#TODO: Fix duplicated print, implment ODR

class rentRollEntity:
    def __init__(self):
        self.leaseNum = ""
        self.operatingName = ""
        self.sqrFt = ""
        self.status = ""
        self.renOption = ""
        self.leaseExpire = ""
        self.renNotice = ""
        self.origCom = ""

    def printRoll(self):
        print("Lease number: " + self.leaseNum + "\n Operating Name: " + self.operatingName + "\n Square Feet: " + self.sqrFt + "\n Status: " + self.status + "\n Renewal Option: " + self.renOption + "\n Lease Expires " + self.leaseExpire + "\n Renewal Notice: " + self.renNotice + "\n Orig Com: " + self.origCom + "\n\n")

class rentRolls:
    def __init__(self) -> None:
        self.rolls = []

    def addRoll(self, newRoll):
        self.rolls.append(newRoll)

    def listRolls(self):
        for roll in self.rolls:
            roll.printRoll()

def readImage(filename):
    img = Image.open(filename)

    text = pytesseract.image_to_string(img)

    print(text)
    allRoll = rentRolls()
    return allRoll

def readPDFTemplate1(filename):
    text = extract_text(filename)
    textLines = text.splitlines()
    #Once "TCC" is read from the start of a line, make a new roll
    allRoll = rentRolls()
    itemCount = 0
    for line in textLines[:500]:
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

    allRoll.listRolls()
    return allRoll

def main():
    readImage('1650 lease rent roll.png')
    #readPDFTemplate1('2018-05-16 - Tamarack - Base Rent Roll.pdf')

if __name__ == "__main__":
    main()
