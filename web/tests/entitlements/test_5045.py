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
    # Test Name : Entitlements - Entry Private with Initial Owner changed to Co Viewer
    # Test description:
    # 1. Verify that the media owner its able to access the entry via media page
    # 2. Verify that the media owner of an entry can be changed
    # 3. Verify that the initial media owner can receive co-viewer rights
    #================================================================================================================================
    testNum = "5045"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables

    typeTest            = "Initial Entry Owner changed to Co Viewer"
    newMediaOwner       = "python_normal"
    newMediaOwnerPass   = "Kaltura1!"
    
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"

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
            self.entryName             = clsTestService.addGuidToString("Entitlements - Owner user changed to Co Viewer", self.testNum)
            self.entryTags             = clsTestService.addGuidToString("entry,", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
     
            writeToLog("INFO","Step 2: Going to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 3: Going to navigate to the Edit Entry Page for " + self.entryName)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to the entry page for " + self.entryName)
                return
            
            writeToLog("INFO","Step 4: Going to change the owner of " + self.entryName + " entry as " + self.newMediaOwner)
            if self.common.editEntryPage.changeMediaOwner(self.newMediaOwner) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to change the owner of " + self.entryName + " entry as " + self.newMediaOwner)
                return
            
            writeToLog("INFO","Step 5: Going to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 6: Going to authenticate using " + self.newMediaOwner)
            if self.common.login.loginToKMS(self.newMediaOwner, self.newMediaOwnerPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to authenticate using " + self.newMediaOwner)
                return
            
            writeToLog("INFO","Step 7: Going to navigate to the entry page of " + self.entryName + " entry as " + self.newMediaOwner)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to the entry page of " + self.entryName + " entry as " + self.newMediaOwner)
                return
            
            writeToLog("INFO","Step 8: Going to navigate to the Edit Entry Page of " + self.entryName + " entry as " + self.newMediaOwner)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 8: FAILED to navigate to the entry page of " + self.entryName + " entry as " + self.newMediaOwner)
                return
            
            writeToLog("INFO","Step 9: Going to add " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " as Co Viewer of " + self.entryName + " entry ")
            if self.common.editEntryPage.addCollaborator(self.entryName, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, False, False, True) == False:
                writeToLog("INFO","Step 9: FAILED to add " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " as Co Viewer of " + self.entryName + " entry ")
                return
            
            writeToLog("INFO","Step 10: Going to log out from " + self.newMediaOwner + " and authenticate with " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.login.logOutThenLogInToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to log out from " + self.newMediaOwner + " and authenticate with " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 11: Going to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " while having Co Viewer rights")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                self.common.myMedia.clearSearch()
                sleep(1)            
                if self.common.myMedia.searchEntryMyMedia(self.entryName, forceNavigate=False) == False:
                    writeToLog("INFO","Step 11.1: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " while having Co Viewer rights")
                    return 
                sleep(2)
                if self.common.myMedia.clickEntryAfterSearchInMyMedia(self.entryName) == False:
                    writeToLog("INFO","Step 11.2: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " while having Co Viewer rights")
                    return                
                sleep(5)              
            ##################################################################
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
            self.common.login.loginToKMS(self.newMediaOwner, self.newMediaOwnerPass)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')