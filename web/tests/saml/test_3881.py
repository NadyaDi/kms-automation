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
    #  @Author: Oleg Sigalov
    # Test Name: SAML Login only
    # Test description: Try to login with right credentials
    # https://kaltura.atlassian.net/wiki/spaces/KMS47/pages/421233135/SAML+Clients+Credentials
    #================================================================================================================================
    testNum     = "3881"
    enableProxy = False
    
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
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Login to SAP")
            if self.common.login.genericLogin('c5183441', '3Bc95nKA', 'https://video.sap.com/', ('id', 'j_username'), ('id', 'j_password'), ('id', 'logOnFormSubmit'), ('id', 'userMenuToggle')) == False:
                writeToLog("INFO","Step 1: FAILED to Login to SAP")
                return
             
            writeToLog("INFO","Step 2: Login to lib.mivideo.it.umich.edu")
            if self.common.login.genericLogin('kalturaz', 'Ycembrapplatcha5', 'http://lib.mivideo.it.umich.edu/user/login', ('id', 'login'), ('id', 'password'), ('id', 'loginSubmit'), ('id', 'userMenuToggleBtn')) == False:
                writeToLog("INFO","Step 2: FAILED Login to lib.mivideo.it.umich.edu")
                return
 
            writeToLog("INFO","Step 3: Login to https://myvideo.siemens.com")
            if self.common.login.genericLogin('buki.peri@kaltura.com', 'DanNiz29!', 'https://myvideo.siemens.com', ('name', 'usr_name'), ('name', 'usr_password'), ('xpath', "//a[contains(@onclick, 'login_Password.submit()')]"), ('id', 'userMenuToggle')) == False:
                writeToLog("INFO","Step 3: FAILED Login to https://myvideo.siemens.com")
                return        
             
            writeToLog("INFO","Step 4: Login to lib.mivideo.it.umich.edu")
            if self.common.login.genericLogin('ydw086', 'Demesne80155', 'https://media.qmplus.qmul.ac.uk/user/login', ('name', 'username'), ('name', 'password'), ('xpath', "//input[@type='submit']"), ('id', 'userMenuToggleBtn')) == False:
                writeToLog("INFO","Step 4: FAILED failed to upload video entry")
                return                    
                  
            #########################################################################
            self.status = "Pass"
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
