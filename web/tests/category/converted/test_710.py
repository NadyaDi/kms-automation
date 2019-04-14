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
    #  @Author: Inbar Willman
    # Test Name : Categories - Edit Entry link
    # Test description:
    # Upload entry and publish to category -> Search entry in category -> Click on edit button
    # Test clean up: Delete uploaded entry
    #================================================================================================================================
    testNum = "710"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    categoryName = None
    userContributerName = "private"
    userContributerPass = "123456"
    LoginPageUrl = "https://2373952.qakmstest.dev.kaltura.com/user/login"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
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
            self.entryName = clsTestService.addGuidToString("ClickEditFromCategory", self.testNum)
            self.categoryName = clsTestService.addGuidToString('Automation Category', self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to create open category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.entryDescription) == False:
                writeToLog("INFO","Step 1: FAILED to create open category")
                return
             
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
            
            
            writeToLog("INFO","Step 4: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 4: FAILED failed to upload entry")
                return
                      
            writeToLog("INFO","Step 5: Going to publish entry to category")            
            if self.common.myMedia.publishSingleEntry(self.entryName, [self.categoryName], [], publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False:
                writeToLog("INFO","Step 5: FAILED to publish entry to category")
                return            
                                        
            writeToLog("INFO","Step 6: Going to navigate to category page")            
            if self.common.category.navigateToCategory(self.categoryName) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to category page")
                return             
                 
            writeToLog("INFO","Step 7: Going to refresh category")            
            if self.common.category.refreshNowCategory(60) == False:
                writeToLog("INFO","Step 7: FAILED to navigate to category page")
                return   
            
            # Additional sleep - do not delete
            sleep(5)
            self.common.base.refresh()
                             
            writeToLog("INFO","Step 8: Going to navigate to entry's edit page")            
            if self.common.category.navigateToEditEntryPageFromCategoryWhenNoSearchIsMade(self.entryName) == False:
                writeToLog("INFO","Step 8: FAILED to click entry Edit button, Entry name: '" + self.entryName + "'")
                return                                          
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Navigate to edit page from category page' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')