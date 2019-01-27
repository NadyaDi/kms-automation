import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # test Name: Entry page - Publish to category from entry page
    # Test description: publish entry to category from entry page
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions' -Publish -> choose category to publish to -> Click save
    # -> Check that entry is displayed in category
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "694"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    categoryName = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('publishEntryToCategoryFromEntryPage', self.testNum)
            self.categoryName = clsTestService.addGuidToString("Publish to category from entry page", self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            
            writeToLog("INFO","Step 1: Going to create category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.entryDescription, None) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create category")
                return
            
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return     
            
            writeToLog("INFO","Step 4: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to upload entry")
                return      
              
            writeToLog("INFO","Step 5: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to entry page")
                return           
              
            writeToLog("INFO","Step 6: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED - New entry is still processing")
                return
                  
            writeToLog("INFO","Step 7: Going to publish entry to category from entry page")
            if self.common.myMedia.publishSingleEntry(self.entryName, [self.categoryName], "", publishFrom = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entry to category from entry page")
                return                 
            
            writeToLog("INFO","Step 8: Going to navigate to category")
            if self.common.category.navigateToCategory(self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to category")
                return             
                          
            writeToLog("INFO","Step 9: Going to search entry in category")
            if self.common.category.searchEntryInCategory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to find entry in category")
                return                                                                           
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Entry page - Publish to category from entry page' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
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