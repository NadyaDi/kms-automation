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
    
    newList = [item for item, count in collections.Counter(newList).items() if count > 1]
    print('Found duplicated test: ' + str(newList))      
    return newList
    
    
    # Example for listRemoveId: ['test_687', 'test_673', 'test_676', 'test_767', 'test_679']
#     def removeDuplicatesLines(self, csvPath, listRemoveId):    
        
        

if __name__ == '__main__':
    csvPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSet.csv'))
    listDuplicates = getDuplicatedTestIds(csvPath)
    f = open(csvPath,"r") 
    lines = f.readlines()
    f.close()
    i = 0
    f = open(csvPath,"w")
    for line in lines:
        for dup in reversed(listDuplicates):
            if not dup in line:
                f.write(line)
                break
            else:
                listDuplicates.remove(dup)
                i +=1
                print(str(i))
                break 
            
    f.close()    
    pass




    
#         for line in lines:
#         for dup in reversed(listDuplicates):
#             if not dup in line:
#                 f.write(line)
#                 break
#             else:
#                 listDuplicates.remove(dup)
#                 break