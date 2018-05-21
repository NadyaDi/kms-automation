import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test description:

    #================================================================================================================================
    testNum = "665"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryName1 = None
    notExistEntry = None
    entryDescription1 = None
    entryDescription = None
    entryTags = None
    entryTags1 = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    numberOfEntriesToUpload = 3
    entriesList = []
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName1 = clsTestService.addGuidToString("Different Search in my media", self.testNum)
            self.entryName = clsTestService.addGuidToString("search in my media ", self.testNum)
            self.notExistEntry = clsTestService.addGuidToString("negative test", self.testNum)
            self.entryDescription1 = clsTestService.addGuidToString("different description", self.testNum)
            self.entryDescription = clsTestService.addGuidToString("search By Description", self.testNum)
            self.entryTags = clsTestService.addGuidToString("search by Tags,", self.testNum)
            self.entryTags1 = clsTestService.addGuidToString("different Tags,", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.entryDescription1, self.entryTags1) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
               
            writeToLog("INFO","Step 2: Going to upload " + str(self.numberOfEntriesToUpload) + " entries")  
            for i in range(1,4):
                if self.common.upload.uploadEntry(self.filePath, self.entryName+str(i), self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to upload entry' " + self.entryName+str(i) + "'")
                    return 
                self.entriesList.append(self.entryName+str(i))
                                  
            writeToLog("INFO","Step 3: Going to search the different entry by entry name and verify that only this entry display after search in my media")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryName1, self.entryName1, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify that only the different entry display after search by entry name in my media")
                return
                 
            writeToLog("INFO","Step 4: Going to search all entries in entries list by entry name and verify that all similar entries are display after search")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryName, self.entriesList, self.numberOfEntriesToUpload) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify that all similar entries are display after search  by entry name in my media")
                return
             
            writeToLog("INFO","Step 5: Going to search the different entry by description and verify that only this entry display after search in my media")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryDescription1, self.entryName1, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify that only the different entry display after search by description in my media")
                return
                 
            writeToLog("INFO","Step 6: Going to search all entries in entries list by description and verify that all similar entries are display after search")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryDescription, self.entriesList, self.numberOfEntriesToUpload) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify that all similar entries are display after search by description in my media")
                return
             
            writeToLog("INFO","Step 7: Going to search the different entry by tags and verify that only this entry display after search in my media")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryTags1, self.entryName1, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify that only the different entry display after search by tags in my media")
                return
                 
            writeToLog("INFO","Step 8: Going to search all entries in entries list by tags and verify that all similar entries are display after search")  
            if self.common.myMedia.verifyEntriesExistInMyMedia(self.entryTags, self.entriesList, self.numberOfEntriesToUpload) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify that all similar entries are display after search by tags in my media")
                return
             
            writeToLog("INFO","Step 9: Going to search non existing word in my media")  
            if self.common.myMedia.searchEntryMyMedia(self.notExistEntry, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to search in my media")
                return
             
            writeToLog("INFO","Step 10: Going to verify that non existing word isn't found in my media")     
            if self.common.base.is_visible(self.common.myMedia.MY_MEDIA_NO_ENTRIES_FOUND) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED non existing entry was found in my media")
                return
            
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Search in my media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            for i in range(1,4):
                self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName+str(i))
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')