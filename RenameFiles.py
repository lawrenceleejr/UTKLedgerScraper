import os,sys
from PyPDF2 import PdfReader
"""pip install PyPDF2"""

import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta

print("Typical usage: python3 RenameFiles.py LedgerPDFs/Form*.pdf\n\n")

listOfInputFilenames = sys.argv[1:]

print("Going to autogenerate new filenames for:"+"\n".join([x for x in listOfInputFilenames]))

def findElementAfterMatch(inputString,subString,relativePos = 1):
    inputStringParts = inputString.split()
    return inputStringParts[inputStringParts.index(subString)+relativePos]

for file in listOfInputFilenames:
    print(f"Copying {file} to new shiny name")
    reader = PdfReader(file)

    # getting a specific page from the pdf file
    page = reader.pages[0]
    text = page.extract_text()
    textlines = text.splitlines()

    # Special handling for start-up ledgers
    if textlines[0].startswith("U013410060"):
        start_date = findElementAfterMatch(textlines[0], "Period:")
        fiscal_date = datetime.strptime(start_date, "%m-%d-%Y") + relativedelta(months=6)
        accountNumber = textlines[1].split()[0]
        fymonth = int(fiscal_date.strftime('%m'))
        newName = f"FY{fiscal_date.strftime('%Y')}_Period{fymonth:03}_{accountNumber}.pdf"

    else:
        # print(text) #useful for debugging
        line3 = textlines[3].split()
        accountNumber = line3[1]+line3[2]

        print(textlines[1])
        fiscalYear = findElementAfterMatch(textlines[1],"FY").replace(")","")
        period = findElementAfterMatch(textlines[1],"(PERIOD")

        newName = f"FY{fiscalYear}_Period{period}_{accountNumber}.pdf"

    newFile = "/".join(file.split("/")[:-1])+"/"+newName
    print(f"... Copying {file} to a file called {newFile}\n")
    shutil.copyfile(file, newFile)

