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


class Test:
    
    #================================================================================================================================
    #  @Author: Ori Flchtman
    # Test Name: SAML Regression SP Initiated
    # Test the configuration of the SAML module in KMS/Admin and verify user can log in to KMS and add media using SAML SP configuration
    # 
    #================================================================================================================================
    testNum     = "2360"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    userName1 = "orifl@mailinator.com"
    userPass1 = "Kaltura1!"
    loginRedirectUrl = "http://il-qaapache-test.kaltura.com/saml2/idp/SSOService.php"
    logoutRedirectUrl = "http://il-qaapache-test.kaltura.com/simplesaml/saml2/idp/SingleLogoutService.php"
    
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
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Enable SAML Module")
            if self.common.admin.enableSamlModule(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to Login to KMS/Admin")
                return
             
            writeToLog("INFO","Step 2: Setup General configuration")
            if self.common.login.samlGeneralConfig(self.loginRedirectUrl, self.logoutRedirectUrl, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED Setup General configuration")
                return
  
#             writeToLog("INFO","Step 3: Login to https://myvideo.siemens.com")
#             if self.common.login.genericLogin('buki.peri@kaltura.com', 'DanNiz29!', 'https://myvideo.siemens.com', ('name', 'usr_name'), ('name', 'usr_password'), ('xpath', "//a[contains(@onclick, 'login_Password.submit()')]"), ('id', 'userMenuToggle')) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED Login to https://myvideo.siemens.com")
#                 return        
#              
#             writeToLog("INFO","Step 4: Login to lib.mivideo.it.umich.edu")
#             if self.common.login.genericLogin('ydw086', 'Demesne80155', 'https://media.qmplus.qmul.ac.uk/user/login', ('name', 'username'), ('name', 'password'), ('xpath', "//input[@type='submit']"), ('id', 'userMenuToggleBtn')) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED failed to upload video entry")
#                 return                    
                  
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
