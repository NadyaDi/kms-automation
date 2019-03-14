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
    # Test Name : Entitlements - Entry Private with Co Publisher and Demoted Co Publisher
    # Test description:
    # 1. Verify that the media owner its able to access the entry via media page
    # 2. Verify that a Co Publisher user can be assigned
    # 3. Verify that the Co Publisher user is able to access the entry
    # 4. Verify that the Demoted Co Publisher user is no longer able to access the entry
    #================================================================================================================================
    testNum = "4983"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "Co Publisher User and Demoted Co Publisher user"
    coPublisherUser     = "python_normal"
    coPublisherPass     = "Kaltura1!"
    
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
            self.entryName             = clsTestService.addGuidToString("Entitlements - Co Publisher user", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
     
            writeToLog("INFO","Step 2: Going to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 3: Going to navigate to the Edit Entry Page of " + self.entryName)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to the entry page of " + self.entryName)
                return
            
            writeToLog("INFO","Step 4: Going to add " + self.coPublisherUser + " as Co Publisher of " + self.entryName + " entry ")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.coPublisherUser, False, True) == False:
                writeToLog("INFO","Step 4: FAILED to add " + self.coPublisherUser + " as Co Publisher of " + self.entryName + " entry ")
                return
                        
            writeToLog("INFO","Step 5: Going to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 5: FAILED to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 6: Going to authenticate using " + self.coPublisherUser)
            if self.common.login.loginToKMS(self.coPublisherUser, self.coPublisherPass) == False:
                writeToLog("INFO","Step 6: FAILED to authenticate using " + self.coPublisherUser)
                return
            
            writeToLog("INFO","Step 7: Going to navigate to the entry page for " + self.entryName + " entry as " + self.coPublisherUser)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 7: FAILED to navigate to the entry page for " + self.entryName + " entry as " + self.coPublisherUser)
                return
            
            writeToLog("INFO","Step 8: Going to log out from " + self.coPublisherUser)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 8: FAILED to log out from " + self.coPublisherUser)
                return
            
            writeToLog("INFO","Step 9: Going to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                writeToLog("INFO","Step 9: FAILED to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 10: Going to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step10: FAILED to navigate to the entry page for " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 11: Going to navigate to the Edit Entry Page of " + self.entryName)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 11: FAILED to navigate to the entry page of " + self.entryName)
                return
            
            writeToLog("INFO","Step 12: Going to remove the " + self.coPublisherUser + " from the collaboration list of " + self.entryName + " entry")
            if self.common.editEntryPage.removeCollaborator(self.coPublisherUser) == False:
                writeToLog("INFO","Step 12: FAILED to remove the " + self.coPublisherUser + " from the collaboration list of " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 13: Going to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 13: FAILED to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 14: Going to authenticate using " + self.coPublisherUser)
            if self.common.login.loginToKMS(self.coPublisherUser, self.coPublisherPass) == False:
                writeToLog("INFO","Step 14: FAILED to authenticate using " + self.coPublisherUser)
                return
            
            writeToLog("INFO","Step 15: Going to verify that the " + self.coPublisherUser + " user is no longer able to access the " + self.entryName + " after has been demoted")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) != False:
                writeToLog("INFO","Step 15: FAILED to verify that the " + self.coPublisherUser + " user is no longer able to access the " + self.entryName + " after has been demoted")
                return
            ##################################################################
            self.status = "Pass"
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