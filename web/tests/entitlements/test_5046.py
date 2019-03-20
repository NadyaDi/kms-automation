import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Entitlements - Entry Private with Co Viewer
    # Test description:
    # 1. Verify that the media owner its able to access the entry via media page
    # 2. Verify that the media owner its able to add as a collaborator a Co Viewer User
    # 3. Verify that the Co-Viewer user its able to access the assigned entry
    #================================================================================================================================
    testNum = "5046"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables

    typeTest           = "Private entry that has a Co Viewer user"
    coViewerUser       = "python_normal"
    userPass           = "Kaltura1!"
    
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'    
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
            # Variables used in order to proper create the Entry
            self.entryName             = clsTestService.addGuidToString("Entitlements - Private Entry with Co Viewer", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
     
            writeToLog("INFO","Step 2: Going to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 3: Going to navigate to the Edit Entry Page for " + self.entryName)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to the entry page for " + self.entryName)
                return
            
            writeToLog("INFO","Step 4: Going to add " + self.coViewerUser + " as Co Viewer of " + self.entryName + " entry ")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.coViewerUser, False, False, True) == False:
                writeToLog("INFO","Step 4: FAILED to add " + self.coViewerUser + " as Co Viewer of " + self.entryName + " entry ")
                return
            
            writeToLog("INFO","Step 5: Going to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " and authenticate with " + self.coViewerUser)
            if self.common.login.logOutThenLogInToKMS(self.coViewerUser, self.userPass)  == False:
                writeToLog("INFO","Step 5: FAILED to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " and authenticate with " + self.coViewerUser)
                return
            
            writeToLog("INFO","Step 6: Going to navigate to the entry page for " + self.entryName + " entry as " + self.coViewerUser + " while having Co Viewer rights")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                self.common.myMedia.clearSearch()
                sleep(1)            
                if self.common.myMedia.searchEntryMyMedia(self.entryName, forceNavigate=False) == False:
                    writeToLog("INFO","Step 6.1: FAILED to navigate to the entry page for " + self.entryName + " entry as " + self.coViewerUser + " while having Co Viewer rights")
                    return 
                sleep(2)
                if self.common.myMedia.clickEntryAfterSearchInMyMedia(self.entryName) == False:
                    writeToLog("INFO","Step 6.2: FAILED to navigate to the entry page for " + self.entryName + " entry as " + self.coViewerUser + " while having Co Viewer rights")
                    return                
                sleep(5)                 
            ##################################################################
            self.status="Pass"
            writeToLog("INFO","TEST PASSED: Entry Page has been successfully verified for a " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')