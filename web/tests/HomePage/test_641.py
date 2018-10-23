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
    preLinkName = "Google"
    preLinkValue = "https://www.google.co.il/"
    postLinkName = "Mako"
    postLinkValue = "https://www.mako.co.il/"
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
            
            writeToLog("INFO","Step 1: Going to set navigation style to: " + enums.NavigationStyle.VERTICAL.value)
            if self.common.admin.setNavigationStyle(navigationStyle=enums.NavigationStyle.VERTICAL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to set navigation style to: " + enums.NavigationStyle.VERTICAL.value)
                return
 
            writeToLog("INFO","Step 2: Going to set pre link in admin page")    
            if self.common.admin.addPrePostLinkItem(enums.NavigationPrePost.PRE, self.preLinkName, self.preLinkValue, enums.SameWindowPrePost.YES) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to set pre link in admin page")
                return
             
            writeToLog("INFO","Step 3: Going to set post link in admin page")    
            if self.common.admin.addPrePostLinkItem(enums.NavigationPrePost.POST, self.postLinkName, self.postLinkValue, enums.SameWindowPrePost.NO) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to set post link in admin page")
                return
             
            writeToLog("INFO","Step 4: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 5: Going to verify that navigation bar is vertical")
            if self.common.home.openVerticalNavigationBar() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify and open vertical navigate bar")
                return
                
            writeToLog("INFO","Step 6: Going to check pre link, open in same window: '" + enums.SameWindowPrePost.YES + "' in vertical navigation mode")    
            if self.common.home.checklinkFormNavBarOnInNewWindow(self.postLinkName, self.postLinkValue, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify pre link open in different window and the url is correct in vertical navigation mode")
                return
            
            writeToLog("INFO","Step 7: Going to check post link, open in same window: '" + enums.SameWindowPrePost.NO + "' in vertical navigation mode")    
            if self.common.home.checklinkFormNavBarOnInNewWindow(self.postLinkName, self.postLinkValue, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify pre link open in different window and the url is correct in vertical navigation mode")
                return
            
            
            
            
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