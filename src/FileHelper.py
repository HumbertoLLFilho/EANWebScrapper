import csv
import json

from Models.Detail import Detail

def OpenAndReadEansFile(eanFilePath: str):
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

def getPathFromAppsettings():
    with open("src/appsettings.json","r") as file:
        jsonData = json.load(file)

    return jsonData["Paths"]["root"]