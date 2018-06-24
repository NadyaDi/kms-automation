from _hashlib import new
import collections
import csv
import os

import localSettings


def getDuplicatedTestIds(csvPath):
    listTestId = open(csvPath).readlines() 
    newList = []
    for test in listTestId:
        newList.append(test.split(',')[0])
    
    dupList = [item for item, count in collections.Counter(newList).items() if count > 1]
    print('Found duplicated test: ' + str(dupList))
    
    return dupList


def createListOfDuplicatedLines(csvPath, dupList):
    listTestId = open(csvPath).readlines() 
    newList = []
    for test in listTestId:
        for dupId in dupList:
            if dupId in test:
                if dupId not in newList:
                    newList.append(test)
                  
    return [item for item, count in collections.Counter(newList).items() if count > 1]


def removeDuplicatesFromFile(csvPath, listDuplicatedLines):
    f = open(csvPath,"r") 
    lines = f.readlines()
    f.close()
    i = 0
    f = open(csvPath,"w")
    for line in lines:
        if not line in listDuplicatedLines:
            f.write(line)
        else:
            print(str(i) + ': Duplicated line was removed')
            
    if listDuplicatedLines:
        print('Adding duplicated lines at the end of file')
        for line in listDuplicatedLines:
            f.write(line)         
    f.close()    
    pass    
    
    
def getSortedListOfTestIdOnly(csvPath):    
    listTestId = open(csvPath).readlines() 
    newList = []
    for test in listTestId:
        if 'case' not in test: #not a first line
            newList.append(test.split(',')[0].split('_')[1])
    
    newList.sort(key=int)
    return newList


def createNewSortedCsv(csvPath, csvPathReady, idsList):
    f = open(csvPathReady, 'w')
    listTestId = open(csvPath).readlines()
    f.write(listTestId[0])
    for id in idsList:
        for line in listTestId[1:]:
            if id == line.split(',')[0].split('_')[1]:
                f.write(line)
                break
    
    f.close    


if __name__ == '__main__':
    csvPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSet.csv'))
    csvPathReady = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSetReady.csv'))
    
    listDuplicates = getDuplicatedTestIds(csvPath)
    listDuplicatedLines = createListOfDuplicatedLines(csvPath, listDuplicates)
    removeDuplicatesFromFile(csvPath, listDuplicatedLines)
    idsList = getSortedListOfTestIdOnly(csvPath)
    createNewSortedCsv(csvPath, csvPathReady, idsList)
    pass