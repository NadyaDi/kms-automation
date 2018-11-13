import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Oleg Sigalov
    # Test Name: Set serviceUrl in Admin
    # Test description: Set new service Url for all instances in the csv file
    #================================================================================================================================
    testNum     = "0002"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    #serviceUrl = 'https://www.kaltura.com'
    serviceUrl = 'https://pa-front-stg.kaltura.com'
    verifySSL = True
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize and open browser
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)  
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Get a list of all instances with its Admin username and password")
            instacesDict = getListOfInstances()
            if len(instacesDict) == 0: 
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to get a list of all instances")
                return
             
            writeToLog("INFO","Step 2: Login to admin and set service url")
            for instance, cred in instacesDict.items():
                if self.common.admin.setServiceUrl(instance, cred[0], cred[1], self.serviceUrl, self.verifySSL) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to set service url for instance: " + str(instance))
                  
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')
