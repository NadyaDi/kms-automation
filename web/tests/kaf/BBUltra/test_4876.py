import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *
import ctypes
import collections

class Test:
    #================================================================================================================================
    # @Author: Oded Berihon
    # Test Name : Blackboard Ultra - My Media - Sort Media
    # Test description:
    # upload sevaral entries and add them comments.
    # Sort My Media by:
    #    1. Most Recent - The entries' order should be from the last uploaded video to the first one.
    #    2. Alphabetical - The entries' order should be alphabetical
    #    4. Comments - The entries' order should be descending by comments' number
    #================================================================================================================================
    testNum     = "4876"
    application = enums.Application.BLACKBOARD_ULTRA
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    comments = ["Comment 1", "Comment 2", "Comment 3"]
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName1 = clsTestService.addGuidToString("My Media - Sort A", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - Sort B", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Media - Sort C", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("My Media - Sort D", self.testNum)
            
            self.entriesToUpload = {
            self.entryName1: self.filePath, 
            self.entryName2: self.filePath,
            self.entryName3: self.filePath,
            self.entryName4: self.filePath }
            self.entriesToUpload = collections.OrderedDict(self.entriesToUpload)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                   
            for i in range(1,5):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new entry '" + eval('self.entryName'+str(i)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i)))
                    return     
                   
            writeToLog("INFO","Step 5: Going navigate to entry '" + self.entryName1 + "'")    
            if self.common.entryPage.navigateToEntry(self.entryName1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to entry: " + self.entryName1)
                return    
                     
            sleep(2) 
            writeToLog("INFO","Step 6: Going to add comments to entry: " + self.entryName1)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add comments to entry: " + self.entryName1)
                return     
                    
            writeToLog("INFO","Step 7: Going navigate to entry: "+ self.entryName3)    
            if self.common.entryPage.navigateToEntry(self.entryName3, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to entry: " + self.entryName3)
                return 
                    
            sleep(2) 
            writeToLog("INFO","Step 8: Going to add comments to entry: " + self.entryName3)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to add comments to entry: " + self.entryName3)
                return    
                    
            writeToLog("INFO","Step 9: Going navigate to entry: "+ self.entryName4)    
            if self.common.entryPage.navigateToEntry(self.entryName4, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED navigate to entry: " + self.entryName4)
                return 

            sleep(2) 
            writeToLog("INFO","Step 10: Going to add comment to entry: " + self.entryName4)  
            if self.common.entryPage.addComment("Comment 1") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add comment to entry: " + self.entryName4)
                return    
                    
            writeToLog("INFO","Step 11: Going navigate to my media")    
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED navigate to my media")
                return 
            
            sleep(3)
            writeToLog("INFO","Step 12: Going to sort my media by: Alphabetical")  
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.ALPHABETICAL, (self.entryName1, self.entryName2, self.entryName3, self.entryName4)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to sort my media by Alphabetical")
                return 
            sleep(1)
              
            if self.common.isElasticSearchOnPage() == True:  
                writeToLog("INFO","Step 13: Going to sort my media by: Most recent")
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.CREATION_DATE_DESC, (self.entryName4, self.entryName3, self.entryName2, self.entryName1)) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to sort my media by Most recent")
                    return
            else:
                writeToLog("INFO","Step 13: Going to sort my media by: Most recent")   
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.MOST_RECENT , (self.entryName4, self.entryName3, self.entryName2, self.entryName1)) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to sort my media by Most recent")
                    return
         
            sleep(1)
            writeToLog("INFO","Step 14: Going to sort my media by: comments")    
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.COMMENTS, (self.entryName3, self.entryName1, self.entryName4, self.entryName2)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to sort my media by comments")
                return

            ##################################################################
            writeToLog("INFO","TEST PASSED: 'BLACKBOARD_ULTRA - My Media - Sort Media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')