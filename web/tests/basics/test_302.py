import time, pytest

from clsCommon import Common
from clsTestService import clsTestService
from localSettings import *
import localSettings
from login import Login
from upload import Upload
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testService = clsTestService()
    testNum     = "302"
    enableProxy = False
    
    supported_platforms = testService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    
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
#             self,capture,driver = self.testService.initializeAndLoginAsUser(self, driverFix)
            self,capture,self.driver = self.testService.initialize(self, driverFix)
            ##################################################################
            
            ################### TEST REUSABLE CLASS HELPERS ##################
            common = Common(self.driver)
            upload = Upload(self.driver)
            ##################################################################

            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED")
                return
            
            upload.upload("filePath", "namename", "descritiondescrition", "tags1,tags2,")
            ##################################################################
            print("DONE")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status =self.testService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        self.testService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')