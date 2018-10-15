import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
from KalturaClient.Plugins.Core import KalturaPrivacyType, KalturaContributionPolicyType, KalturaAppearInListType
import enums
from upload import UploadEntry


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Categories - Sort media on category page
    # Test description:
    # Create category 

    #================================================================================================================================
    testNum = "1025"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description"
    tags = "Tags,"
    catagoryName = None
    entryName = None
    filePath= localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    comment1 = "Enable comments in category"
    comment2 = "Disable comments in category"

    
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
            self.catagoryName = clsTestService.addGuidToString("Enable Disable comments in category", self.testNum)
            self.entryName = clsTestService.addGuidToString("Enable Disable comments in category", self.testNum)
            self.entry1 = UploadEntry(self.filePath, self.entryName, self.description, "", timeout=60, retries=3)
       
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.catagoryName, self.description, None) == False:
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
             
            writeToLog("INFO","Step 4: Going to add media to category")
            if self.common.category.addNewContentToCategory(self.catagoryName, self.entry1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add media to category")
                return
            
            self.common.category.refreshNowCategory()   
            sleep(3)
            writeToLog("INFO","Step 5: Going to verify entry found in category")
            if self.common.category.searchEntryInCategory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to find entry '" + self.entryName + "' in category: " + self.catagoryName)
                return
             
            writeToLog("INFO","Step 6: Going navigate to edit category page")
            if self.common.category.navigateToEditCategoryPage(self.catagoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to edit category page")
                return
            sleep(2)
            
            writeToLog("INFO","Step 7: Going to enable comments in category")
            if self.common.channel.enableDisableCommentsInChannel(self.catagoryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to enable comments in category: " + self.catagoryName)
                return
            sleep(2)
            
            writeToLog("INFO","Step 8: Going navigate to entry from category page")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.catagoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to entry from category page")
                return
            
            writeToLog("INFO","Step 9: Going to add comment to entry from category page")
            if self.common.entryPage.addComment(self.comment1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to add comment to entry: " + self.entryName)
                return
            
            writeToLog("INFO","Step 10: Going navigate to edit category page")
            if self.common.category.navigateToEditCategoryPage(self.catagoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to edit category page")
                return
            sleep(2)
            
            writeToLog("INFO","Step 11: Going to disable comments in category")
            if self.common.channel.enableDisableCommentsInChannel(self.catagoryName, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to disable comments in category: " + self.catagoryName)
                return
            sleep(2)
            
            writeToLog("INFO","Step 12: Going navigate to entry from category page")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.catagoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED navigate to entry from category page")
                return
            
            writeToLog("INFO","Step 13: Going to add comment to entry from category page")
            if self.common.entryPage.addComment(self.comment2) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED, user was able to add comment to entry from category page although comment is disable in category")
                return
            writeToLog("INFO","Step 13: Preview step failed as expected: comments in category is disabled")
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Categories - Enable Disable comments in category' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")        
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)         
            self.common.apiClientSession.deleteCategory(self.catagoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')