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
    #  @Author: Cus Horia
    # Test Name : Setup test for eSearch
    # Test description:
    # Upload three Video entries and filter them by publish statuses: private, unlisted, published, rejected and pending
    # entryName1 has the following status: Private
    # entryName2 has the following status: Unlisted
    # entryName3 has the following statuses: published, rejected and pending
    #================================================================================================================================
    testNum = "21"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    navigateFrom = enums.Location.MY_MEDIA

    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"

    userName2 = "admin"
    userPass2 = "123456"

    entryName1 = "Filter by Status - Video Private"
    entryName2 = "Filter by Status - Video Unlisted"
    entryName3 = "Filter by Status - Video Multiple"

    entryPath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\WhyAutomatedTesting.mp4'
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)

            # Category tests in gallery/add to gallery tabs
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator'

            # Channel for tests in channel/ add to channel tabs
            self.channelForEsearch  = "Channel for eSearch"
            self.channelForModerator = 'channel moderator for eSearch'
            self.SrChannelForEsearch = "SR-Channel for eSearch"

            self.channelForEsearchDescription = "channel for eSearch tests"
            self.channelForEsearchTags = 'channel tag,'
            self.channelForEsearchPrivacy = 'open'
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Step 1: Going to authenticate with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to authenticate with " + self.userName1)
                return

            writeToLog("INFO","Step 2: Going to upload " + self.entryName1 + " entry and leave it as private")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryName1 + " entry and leave it as private")
                return

            writeToLog("INFO","Step 3: Going to upload " + self.entryName2 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to upload " + self.entryName2 + " entry")
                return

            writeToLog("INFO","Step 4: Going to publish " + self.entryName2 + " as unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate('', '', '', enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to publish" + self.entryName2 + " as unlisted")
                return

            writeToLog("INFO","Step 5: Going to upload " + self.entryName3 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to upload " + self.entryName3 + " entry")
                return

            writeToLog("INFO","Step 6: Going to publish the " + self.entryName3 +"  entry")
            if self.common.myMedia.publishSingleEntry(self.entryName3, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 6: FAILED to publish the " + self.entryName3 +"  entry")
                return

            writeToLog("INFO","Step 7: Going to logout from the " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to logout from the " + self.userName1)
                return

            writeToLog("INFO","Step 8: Going to authenticate with user " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to authenticate with " + self.userName2)
                return

            writeToLog("INFO","Step 9: Going to navigate to " + self.categoryForModerator + " category")
            if self.common.category.navigateToCategory(self.categoryForModerator, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to navigate to  " + self.categoryForModerator + " category")
                return

            writeToLog("INFO","Step 10: Going to enter in  " + self.categoryForModerator + " category pending tab")
            if self.common.base.click(self.common.category.CATEGORY_MODERATION_TAB, multipleElements=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to enter in  " + self.categoryForModerator + " category pending tab")
                return

            writeToLog("INFO","Step 11: Going to reject " + self.entryName3 + " entry from the " + self.categoryForModerator + " category")
            if self.common.channel.rejectEntriesInPandingTab(self.entryName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to reject " + self.entryName3 + " entry from the " + self.categoryForModerator + " category")
                return

            writeToLog("INFO","TEST PASSED: All the video entries were successfully created with proper publish statuses")
            #################################################################################

        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)

    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')