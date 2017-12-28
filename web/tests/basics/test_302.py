import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "302"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
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
            self,capture,driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
#             self,captur,self.driver = clsTestService.initialize(self, driverFix)
            ##################################################################
            
            ################### TEST REUSABLE CLASS HELPERS ##################
            common = Common(self.driver)
            ##################################################################

            ##################### TEST STEPS - MAIN FLOW #####################
#             writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
#             if common.loginAsUser() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED")
#                 return
#
            common.myMedia.navigateToEntryPage('RedGreenBlueImage.png')
#             common.upload.uploadEntry("filePath", "namename", "descritiondescrition", "tags1,tags2,")
            ##################################################################
            print("DONE")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')