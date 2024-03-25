import csv
import json
import pandas as pd
from datetime import date

from Models.Detail import Detail

class FileHelper:
    def __init__(self) -> None:
        filename = f'\\Produtos-PISANO({date.today()}).xlsx'
        self.filePath = self.getPathFromAppsettings() + filename

    def OpenAndReadEansFile(self, eanFilePath: str):
        details: list[Detail] = []
        with open(eanFilePath, newline='', encoding='utf-8') as file:
            line = 0
            reader = csv.reader(file, delimiter=';')

            for row in reader:
                if(line > 0):
                    detail = Detail(row[0], row[1], row[2], row[3], row[4])
                    details.append(detail)
                
                line += 1

        return details

    def getPathFromAppsettings(self):
        with open("src/appsettings.json","r") as file:
            jsonData = json.load(file)

        return jsonData["Paths"]["root"]

    def write_sheet(self, df, sheetName = 'Sheet1'):
        with pd.ExcelWriter(self.filePath) as writer:
            df.to_excel(writer, sheet_name= sheetName, index=False)

    def append_sheet(self, df, sheetName = 'Sheet2'):
        with pd.ExcelWriter(self.filePath, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name= sheetName, index=False)