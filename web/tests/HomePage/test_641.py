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
            if self.common.admin.addPrePostLinkItem(enums.NavigationPrePost.PRE, self.preLinkName, self.preLinkValue, enums.SameWindowPrePost.NO) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to set pre link in admin page")
                return
                
            writeToLog("INFO","Step 3: Going to set post link in admin page")    
            if self.common.admin.addPrePostLinkItem(enums.NavigationPrePost.POST, self.postLinkName, self.postLinkValue, enums.SameWindowPrePost.YES) == False:
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
             
            writeToLog("INFO","Step 6: Going to verify that pre/post links display in the correct place in vertical nav bar")    
            if self.common.home.verifyPreAndPostLinkPositionOnNavBar(self.preLinkValue, self.postLinkValue) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify that pre/post links display in the correct place in vertical nav bar")
                return
                 
            writeToLog("INFO","Step 7: Going to check pre link, open in same window: '" + enums.SameWindowPrePost.NO.value + "' in vertical navigation mode")    
            if self.common.home.verifylinkFormNavBarInNewWindow(enums.NavigationStyle.VERTICAL, self.preLinkName, self.preLinkValue, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify pre link open in different window and that the url is correct in vertical navigation mode")
                return
            sleep(3)
            
            writeToLog("INFO","Step 8: Going to click on post link")
            linkNameTmp = (self.common.home.HOME_LINK_IN_NAV_BAR_VERTICAL_MENU[0], self.common.home.HOME_LINK_IN_NAV_BAR_VERTICAL_MENU[1].replace('LINK_NAME', self.postLinkName))
            if self.common.base.click(linkNameTmp) == False:
                self.status = "Fail"
                writeToLog("INFO","FAILED to click on link in nav bar")
                return
            sleep(2)  
             
            writeToLog("INFO","Step 9: Going to check post link, open in same window: '" + enums.SameWindowPrePost.YES.value + "' in vertical navigation mode")    
            if self.common.base.verifyUrl(self.postLinkValue , False, 3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify post link open in same window and that the url is correct in vertical navigation mode")
                return
             
            writeToLog("INFO","Step 10: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to home page")
                return
             
            writeToLog("INFO","Step 11: Going to set navigation style to: " + enums.NavigationStyle.HORIZONTAL.value)
            if self.common.admin.setNavigationStyle(navigationStyle=enums.NavigationStyle.HORIZONTAL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to set navigation style to: " + enums.NavigationStyle.HORIZONTAL.value)
                return
            
            writeToLog("INFO","Step 12: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 13: Going to verify that navigation bar is horizontal")
            if self.common.base.is_visible(self.common.home.HOME_HORIZONTAL_MENU_NAV_BAR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to verify that navigate bar is horizontal")
                return
            
            writeToLog("INFO","Step 14: Going to verify that pre/post links display in the correct place in vertical nav bar")    
            if self.common.home.verifyPreAndPostLinkPositionOnNavBar(self.preLinkValue, self.postLinkValue) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to verify that pre/post links display in the correct place in vertical nav bar")
                return
            sleep(3)  
            
            writeToLog("INFO","Step 15: Going to check pre link, open in same window: '" + enums.SameWindowPrePost.NO.value + "' in vertical navigation mode")    
            if self.common.home.verifylinkFormNavBarInNewWindow(enums.NavigationStyle.HORIZONTAL, self.preLinkName, self.preLinkValue, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify pre link open in different window and that the url is correct in vertical navigation mode")
                return
             
            writeToLog("INFO","Step 16: Going to click on post link")
            linkNameTmp = (self.common.home.HOME_LINK_IN_NAV_BAR_HORIZONTAL_MENU[0], self.common.home.HOME_LINK_IN_NAV_BAR_HORIZONTAL_MENU[1].replace('LINK_NAME', self.postLinkName))
            if self.common.base.click(linkNameTmp) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to click on link in nav bar")
                return
            sleep(2)  
            
            writeToLog("INFO","Step 17: Going to check post link, open in same window: '" + enums.SameWindowPrePost.YES.value + "' in vertical navigation mode")    
            if self.common.base.verifyUrl(self.postLinkValue , False, 3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to verify post link open in same window and that the url is correct in vertical navigation mode")
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
            self.common.admin.deletePrePostLink(enums.NavigationPrePost.PRE, self.preLinkName)
            self.common.admin.deletePrePostLink(enums.NavigationPrePost.POST, self.postLinkName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')