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
    #  @Author: Michal Zomper
    # Test Name : Navigate
    # Test description:
    # in admin page go to navigate tab :
    #    add pre / post links - some of the like do sameWindow=yes and some sameWindow=no
    #    switch between navigation style - Horizontal / Vertical  
    
    #================================================================================================================================
    testNum = "641"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    
    
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
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
#             writeToLog("INFO","Step 1: Going to set navigation style to: " + enums.NavigationStyle.VERTICAL)
#             if self.common.admin.setNavigationStyle(navigationStyle=enums.NavigationStyle.VERTICAL) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to set navigation style to: " + enums.NavigationStyle.VERTICAL)
#                 return
                
            self.common.admin.addPrePostLinkItem(enums.NavigationPrePost.PRE, "Ynet", "https://www.ynet.co.il/home/0,7340,L-8,00.html", enums.SameWindowPrePost.YES)

                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Navigate' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            self.common.admin.setNavigationStyle(navigationStyle=enums.NavigationStyle.HORIZONTAL)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')