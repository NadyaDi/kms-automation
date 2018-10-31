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


class Test:
    #================================================================================================================================
    # @Author: Michal Zomper
    # Test Name : Edit Entry Metadata 
    # Test description:
    # upload media
    # go to media edit page and change media: name / description / tags 
    #================================================================================================================================
    testNum     = "589"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    newEntryName = None
    description = "Description" 
    newDescription = "Edit description"
    tags = "Tags,"
    newTags = "Edit Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'

    
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
            self.entryName = clsTestService.addGuidToString("Entry Metadata", self.testNum)
            self.newEntryName = clsTestService.addGuidToString("Edit Entry Metadata", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                 
            writeToLog("INFO","Step 1: Going to upload entry")   
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                    
            writeToLog("INFO","Step 2: Going navigate to edit entry page")    
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to edit entry '" + self.entryName + "' page")
                return 
                
            writeToLog("INFO","Step 3: Going to change entry metadata  (entry name, description, tags)")
            if self.common.editEntryPage.changeEntryMetadata(self.entryName, self.newEntryName, self.newDescription, self.newTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to edit entry metadata")
                return  
            
            writeToLog("INFO","Step 4: Going navigate entry page")    
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.newEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry: " + self.newEntryName)
                return
            
            writeToLog("INFO","Step 5: Going to verify entry new  metadata  (entry name, description, tags)")
            # We add the word 'tags' since we don't delete the tags that was insert when the entry was uploaded
            if self.common.entryPage.verifyEntryMetadata(self.newEntryName, self.newDescription, self.tags.lower()[:-1] + self.newTags.lower()[:-1]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify entry new  metadata")
                return  
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Edit Entry Metadata ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            if self.common.myMedia.deleteSingleEntryFromMyMedia(self.newEntryName) == False:
                self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')