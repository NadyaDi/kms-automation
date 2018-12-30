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
    # Test Name: D2L - Edit Media Gallery Metadata
    # Test description:
    # Go to media gallery , click on action > edit > change the gallery matadata
    # Go back to gallery page and verify that the new metadata display 
    #================================================================================================================================
    testNum     = "2556"
    application = enums.Application.D2L
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    newDescription = "Edit Description" 
    newTags = "Edit Tags,"
    galleryame = "New1"
    
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
            self.entryName = clsTestService.addGuidToString("Edit Entry page - Close discussion", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                 
            writeToLog("INFO","Step 1: Going navigate to gallery page")   
            if self.common.kafGeneric.navigateToGallery(self.galleryame) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED navigate to gallery page")
                return
            
            writeToLog("INFO","Step 2: Going to edit gallery metadata")   
            if self.common.kafGeneric.editGalleryMatedate(self.newDescription, self.newTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED edit gallery metadata")
                return
                    

            
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'D2L - Edit Media Gallery Metadata' was done successfully")
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