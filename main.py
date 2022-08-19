from pdfminer.high_level import extract_text

class rentRollEntity:
    def __init__(self, leaseNum, operatingName, sqrFt, status, baseRentCat, beginDate, endDate, rate, baseRentNotes):
        self.leaseNum = 0
        self.operatingName = 0
        self.sqrFt = 0
        self.status = 0
        self.baseRentCat = 0
        self.beginDate = 0
        self.endDate = 0
        self.rate = 0
        self.baseRentNotes = 0

class rentRolls:
    def __init__(self) -> None:
        self.rolls = None

    def addRoll(self, newRoll):
        self.rolls = self.rolls + newRoll


def main():
    text = extract_text('2018-05-16 - Tamarack - Base Rent Roll.pdf')
    textLines = text.splitlines()
    #Once TCC is read make a new item
    mainRoll = rentRolls()
    for lines in textLines[:200]:
        print(lines)

if __name__ == "__main__":
    main()
