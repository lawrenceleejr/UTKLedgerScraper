from PyPDF2 import PdfReader
import re
import math

def removeSingleSpaces(s):
    # print(re.sub(r'(?:^| )\w(?:$| )', ' ', "1 2  3"))
    return re.sub(r'(\S)\s(\S)', '\g<1>\g<2>',s)

def addZerosForMissingFields(s,whitespaceWidth=15):
    for i in range(1,6)[::-1]:
        # print(i)
        s = re.sub(r'([\d)])\s{' + str(whitespaceWidth*i) + ',}([\d(])', '\g<1>' + " "*math.floor(whitespaceWidth*i/2) +'0'+ " "*math.floor(whitespaceWidth*i/2) +'\g<2>',s)
        # print(s)
    return s


def cleanAndCastNumber(s):
    if s.isspace() or s=="": return 0
    s = s.replace(",","")
    prefactor = 1
    if "(" in s and ")" in s:
        s = s.replace("(","").replace(")","")
        prefactor = -1
    if "%" in s:
        s = s.replace("%","")
        prefactor = 0.01
    try:
        return prefactor*float(s)
    except:
        return -9999

class AccountReport:
    def __init__(self, pdfFilename):
        self.pdfFilename = pdfFilename

        self.pdf = PdfReader(pdfFilename)

        self.pdfFilenameNoPath = pdfFilename.split("/")[-1]
        self.fy = self.pdfFilenameNoPath.split("_")[0]
        self.period = self.pdfFilenameNoPath.split("_")[1]
        self.account = self.pdfFilenameNoPath.split("_")[2][:-4]

        self.rawText = self.pdf.pages[0].extract_text()
        self.splitText = [addZerosForMissingFields(removeSingleSpaces(x)) for x in self.rawText.splitlines()]
        self.parseNumbers()

    def parseNumbers(self):

        totalsLineNumber = -1
        for i,line in enumerate(self.splitText):
            # print(f"{i}: {line}")
            if "TOTALCOSTS" in line or "TOTALYEAR-TO-DATECOSTS" in line:
                totalsLineNumber = i

        # Parse the ledger reports for start-up differently
        if self.splitText[0].startswith("U013410060"):

            # Do some god-awful parsing
            block_size = 14
            summary_numbers = self.rawText.splitlines()[totalsLineNumber].strip("TOTAL YEAR-TO-DATE COSTS").strip()
            if len(summary_numbers)<=block_size*4: # Handle the case for no expenditures that month
                current_month = ""
                remaining_summary = summary_numbers
            else:
                current_month = summary_numbers.split(".")[0] + "." + summary_numbers.split(".")[1][0:2]
                remaining_summary = summary_numbers.split(current_month)[1]
            self.totalEncumbrances = cleanAndCastNumber(remaining_summary[block_size:2*block_size])
            self.totalSponsorBudget = cleanAndCastNumber(remaining_summary[0:block_size])
            self.totalCurrentPeriodExpenditures = cleanAndCastNumber(current_month.replace(" ",""))
            self.totalCumulativeExpenditures = cleanAndCastNumber(remaining_summary[2*block_size:3*block_size])
            self.totalManualFundsReservations = 0
            self.totalUnderOverSpent = 0
            #print(summary_numbers)
            #print(current_month)
            #print(remaining_summary)
            #print(remaining_summary[0:block_size], remaining_summary[block_size:2*block_size], remaining_summary[2*block_size:3*block_size])
            #print(self.totalCurrentPeriodExpenditures, self.totalSponsorBudget, self.totalEncumbrances, self.totalCumulativeExpenditures)

        else:
            self.obligatedAmount = cleanAndCastNumber(self.splitText[7].split()[-1])
            self.fAndA = cleanAndCastNumber(self.splitText[9].split()[1])
            self.totalSponsorBudget = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[1])
            self.totalCurrentPeriodExpenditures = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[2])
            self.totalCumulativeExpenditures = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[3])
            self.totalEncumbrances = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[4])
            self.totalManualFundsReservations = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[5])
            self.totalUnderOverSpent = cleanAndCastNumber(self.splitText[totalsLineNumber].split()[6])


# tmpFile = AccountReport("LedgerPDFs/FY2023_Period007_R011065670.pdf")


# temp = vars(tmpFile)
# print("-"*30+"\n")
# for item in temp:
#     if "Text" in item:
#         continue
#     print (item , ' : ' , temp[item])



