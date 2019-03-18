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
    # Test Name: BB: Edit Entry page - Disable comments
    # Test description:
    # Upload entry -> Go to entry page > Add comments
    # Go to edit entry page -> option tab and  disabled comments option
    # Go to entry page -> Check that comment isn't displayed and there is no option to add new comments 
    #================================================================================================================================
    testNum     = "590"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    commnet = "Comment"
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
            self.entryName = clsTestService.addGuidToString("Edit Entry page - Disable comments", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                 
            writeToLog("INFO","Step 1: Going to upload entry")   
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                    
            writeToLog("INFO","Step 2: Going navigate to entry page")    
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom =enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED navigate to  entry '" + self.entryName + "' page")
                return 
                
            writeToLog("INFO","Step 3: Going to add new comment to entry")
            if self.common.entryPage.addComment(self.commnet) == False:
                writeToLog("INFO","Step 34: FAILED to add new comment")
                return 
            
            writeToLog("INFO","Step 4: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
                return    
            
            writeToLog("INFO","Step 5: Going to click on option tab and enable - disabled comment")
            if self.common.editEntryPage.changeEntryOptions(True, False, False) == False:
                writeToLog("INFO","Step 5: FAILED to click on option tab and enable disabled comments option")
                return    
            
            writeToLog("INFO","Step 6: Going to navigate to entry page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to entry page")
                return   
            
            writeToLog("INFO","Step 7: Going to verify that comments section isn't displayed in entry page")
            if self.common.entryPage.checkEntryCommentsSection(self.commnet, True, False) == False:
                writeToLog("INFO","Step 7: FAILED - Comments section still displayed in entry page")
                return   
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'BB :Edit Entry Metadata ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')