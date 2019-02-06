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
    # @Author: Inbar Willman
    # Test Name : D2L: Discussions BSE From My Media 
    # Test description:
    # Upload new media -> Go to discussions -> Create new discussion -> click on wysisyg -> Choose media from 'My Media' tab
    # Verify that embed is displayed and played 
    #================================================================================================================================
    testNum     = "2908"
    application = enums.Application.D2L
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    discussionName = None
    timeToStop = "0:07"
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
            self.entryName = clsTestService.addGuidToString("EmbedFromMyMedia", self.testNum)
            self.discussionName = clsTestService.addGuidToString("Embed video from My Media", self.testNum)
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
                  
            writeToLog("INFO","Step 3: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate entry page")
                return
                  
            writeToLog("INFO","Step 4: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to wait until media end upload process")
                return  
              
            writeToLog("INFO","Step 5: Going to create embed discussion")    
            if self.common.d2l.createEmbedDiscussion(self.discussionName, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create embed discussion")
                return             
              
            writeToLog("INFO","Step 6: Going to to verify embed announcement")    
            if self.common.kafGeneric.verifyEmbedEntry(self.entryName, '', self.timeToStop, enums.Application.D2L) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify embed announcement")
                return     
             
            writeToLog("INFO","Step 7: Going to to delete embed announcement")    
            if self.common.d2l.deleteDiscussion(self.discussionName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to delete embed announcement")
                return              
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Create embed discussion from My Media tab ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.deleteDiscussion(self.discussionName, True)   
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')