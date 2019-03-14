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
    # Test Name : BlackBoard: Enable / Disable faculty repository 
    # Test description:
    # 1. Add faculty repository to my institution : Enter my institution > add module > faculty repository
    # 2. Add media to faculty repository
    # 3. Remove faculty repository to my institution : Enter my institution > add module > faculty repository
    #================================================================================================================================
    testNum     = "111"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Fail"
    driver = None
    common = None
    # Test variables

    
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

            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going verify that shared repository module doesn't exist")  
            if self.common.blackBoard.addRemoveSharedRepositoryModule(False) == False:
                writeToLog("INFO","Step 1: FAILED to remove shared repository module")
                return 
               
            writeToLog("INFO","Step 2: Going navigate to blackboard main page") 
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL) == False:
                writeToLog("INFO","Step 2: FAILED navigate to blackboard main page")
                return
            
            writeToLog("INFO","Step 3: Going to add shared repository module")     
            if self.common.blackBoard.addRemoveSharedRepositoryModule(True) == False:
                writeToLog("INFO","Step 3: FAILED to add shared repository module")
                return
            
            writeToLog("INFO","Step 4: Going navigate to blackboard main page") 
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL) == False:
                writeToLog("INFO","Step 4: FAILED navigate to blackboard main page")
                return
            
            writeToLog("INFO","Step 5: Going to remove shared repository module")     
            if self.common.blackBoard.addRemoveSharedRepositoryModule(False) == False:
                writeToLog("INFO","Step 5: FAILED to remove shared repository module") 
                return
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'BlackBoard: Enable / Disable faculty repository' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')