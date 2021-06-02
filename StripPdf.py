import numpy as np
import pandas as pd
from typing import List
import PyPDF2
import pdb

class PDF2CSV():
    def __init__(self, filePath: str):
        self._pdf_file = open(filePath, 'rb')
        self._midSplit = "Selection or command===>____________________________________________________________________________________________________________________________________________________________"
        self._reader = PyPDF2.PdfFileReader(self._pdf_file)
        
        self._codes = []
        self._numbers = []
        self._numberOfPages: int = self._reader.getNumPages()

        self._extractContentFromPdf()
        self._saveDataFrameToCsv()

    def _extractContentFromPdf(self):
        for i in range(self._numberOfPages):
            # Creating a page object
            pageObj = self._reader.getPage(i)

            # Printing Page Number
            print("Page No: ",i)
            
            # Extracting text from page
            # And splitting it into (two) chunks if possible
            text: str = pageObj.extractText().split(self._midSplit)
            
            try:
                # check if 'PAGE' exist in first chunk current page
                text[0] = self._removeTopItems(text[0].split(), text[0].split().index("PAGE"))
            except ValueError:
                # something is wrong with this current pdf page, skip to the next one
                # TODO identify and handle odd cases
                continue
     
            # pop 0
            text[0].pop(0)
            
            # if page contains split point
            if len(text) == 2:
                self._extractCodeAndNumbers(text[0][0], text[1].split())
            # if page is a coninuation of previous page
            else:
                self._extractCodeAndNumbers(text[0][0], text[0])

        # closing the pdf file object
        self._pdf_file.close()

    def _extractCodeAndNumbers(self, correspondingCode: str, text: List[str]):
        for i in range(len(text)):
           try:
               # if string can be converted to an int, append to list
               self._numbers.append(int(text[i]))
               self._codes.append(correspondingCode)
           except ValueError:
               # continue to next element in list
               pass

    def _saveDataFrameToCsv(self):
        # create numpy arrays from lists
        data = np.vstack((np.array(self._numbers), np.array(self._codes))).swapaxes(0,1)
        
        # create pandas dataframe
        df = pd.DataFrame(data, columns=["no", "code"])
        
        # save df as csv
        df.to_csv("Vista_Menu_Authorization_Dataframe.csv", index=False, header=True)

    def _removeTopItems(self, list: List[str], index: int) -> List[str]:
        n = 0
        while (n != index + 1):
            list.pop(0)
            n += 1
        return list

filePath = "VISTA_Menu_Authorizations.pdf"
PDF2CSV(filePath)