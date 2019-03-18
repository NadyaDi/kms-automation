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
    # Test Name : Jive - Delete through edit entry page 
    # Test description:
    # Upload entry
    # Go to edit entry page > Click on  Delete -> Click on Delete in pop up message
    # in My media verify that the entry was deleted
    #================================================================================================================================
    testNum     = "2494"
    application = enums.Application.JIVE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomationTools.jpg'
    
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Delete through edit entry page", self.testNum)
            
            ######################### TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED navigate to edit entry page")
                return
            
            writeToLog("INFO","Step 3: Going to delete entry '" + self.entryName + "'")
            if self.common.editEntryPage.deleteEnteyFromEditEntryPage() == False:
                writeToLog("INFO","Step 3: FAILED to delete entry '" + self.entryName + "' through edit entry page")
                return

            writeToLog("INFO","Step 3: Going to verify that entry '" + self.entryName + "'  doesn't display in my media")
            if self.common.myMedia.verifyNoResultAfterSearchInMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED entry '" + self.entryName + "' still display in my media although it was deleted")
                return     
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Jive - Delete through edit entry page' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')