# UTKLedgerScraper

For turning those terrible ledgers into something useful...

Requires PyPDF2 (`pip install PyPDF2`)

Usage notes to self and others:

* Log into IRIS at https://irisweb.tennessee.edu
* Go to PI Reporting Self-Service
* Select an account and a month and click Get Report to get a "Financial Summary" PDF. You have to maximize the popup and then can download the PDF.
* Put the PDFs into a folder e.g. `LedgerPDFs`.
* To automatically rename them, run `python3 RenameFiles.py LedgerPDFs/Form*.pdf` 
* Then you can write a script and use the `AccountReport` class which takes a string path to a PDF in its constructor and parse out some useful information from it, make plots, whatever.

