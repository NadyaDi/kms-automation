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
    #  @Author: 
    #================================================================================================================================
    testNum = "4699"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    description = "Description"
    tags = "tag1,"
    
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
            self.entryName = clsTestService.addGuidToString("Add new webcam recording", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            #Edit name, description and tags
#             writeToLog("INFO","Step 1: Going to add new webcam recording")  
#             if self.common.upload.addNewWebcamRecording(self.entryName, self.description, self.tags, timeToStopRecording="10") == False:
#                 writeToLog("INFO","Step 1: FAILED to add new webcam recording")
#                 return 
#             
#             writeToLog("INFO","Step 2: Going to to verify that new recording is displayed in My Media")  
#             if self.common.myMedia.searchEntryMyMedia(self.entryName) == False:
#                 writeToLog("INFO","Step 2: FAILED to found new rcording in My Media")
#                 return 
            
            # Create new webcam while clicking record again        
            writeToLog("INFO","Step 1: Going to add new webcam recording")  
            if self.common.upload.addNewWebcamRecording(self.entryName, self.description, self.tags, timeToStopRecording="00:05", recordAgain=True, numOfRecordinAgain=3) == False:
                writeToLog("INFO","Step 1: FAILED to add new webcam recording")
                return                  
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Add new recording")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            sleep(2)                         

            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')