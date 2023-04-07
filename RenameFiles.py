import os,sys
from PyPDF2 import PdfReader
"""pip install PyPDF2"""

import shutil

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

    # print(text) #useful for debugging
    textlines = text.splitlines()
    line3 = textlines[3].split()
    accountNumber = line3[1]+line3[2]

    fiscalYear = findElementAfterMatch(textlines[1],"FY").replace(")","")
    period = findElementAfterMatch(textlines[1],"(PERIOD")

    newName = f"FY{fiscalYear}_Period{period}_{accountNumber}.pdf"

    newFile = "/".join(file.split("/")[:-1])+"/"+newName
    print(f"... Copying {file} to a file called {newFile}\n")
    shutil.copyfile(file, newFile)

