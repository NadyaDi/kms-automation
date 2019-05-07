import pytest
import enums
from clsCommon import Common
import clsTestService
from utilityTestFunc import *


class Test:
    #================================================================================================================================
    # @Author: Oleg Sigalov
    # Test Name : Pitch - Login Test 
    # Test description:
    #================================================================================================================================
    testNum     = "5165"
    application = enums.Application.PITCH
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
            
            writeToLog("INFO","Step 1: Going to logout")
            if self.common.pitch.logOutPitch() == None:
                writeToLog("INFO","Step 1: FAILED failed to logout")
                return
               
            writeToLog("INFO","TEST PASSED: 'Pitch - Login Test'  was done successfully")
            self.status = 'Pass'
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