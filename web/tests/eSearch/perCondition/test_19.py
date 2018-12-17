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
    # Upload three Audio entries and filter them by scheduling in: Past, Future and In Scheduling
    #================================================================================================================================
    testNum = "19"

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

    entryName1 = "Filter by Scheduling - Audio future"
    entryName2 = "Filter by Scheduling - Audio past"
    entryName3 = "Filter by Scheduling - Audio In Scheduling"

    entryPath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\waves.mp3'


    entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
    entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
    entryFutureStartDate = (datetime.datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

    entryFutureStartTime = time.time() + (60*60)
    entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(entryFutureStartTime))

    entryPastStartTime = time.time() - (60*60)
    entryPastStartTime= time.strftime("%I:%M %p",time.localtime(entryPastStartTime))

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
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return

            writeToLog("INFO","Step 2: Going to upload " + self.entryName1 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryName1 + " entry")
                return

            writeToLog("INFO","Step 3: Going to publish " + self.entryName1 + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED to publish " + self.entryName1 + " entry")
                return

            writeToLog("INFO","Step 4: Going to set Future time-frame publishing to " + self.entryName1 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime, entryName=self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to set Future time-frame publishing to " + self.entryName1 + " entry")
                return

            writeToLog("INFO","Step 5: Going to upload " + self.entryName2 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to upload " + self.entryName2 + " entry")
                return

            writeToLog("INFO","Step 6: Going to publish " + self.entryName2 + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryName2, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 6: FAILED to publish " + self.entryName2 + " entry")
                return

            writeToLog("INFO","Step 7: Going to set Past time-frame publishing to " + self.entryName2 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryPastStartDate, endTime=self.entryPastStartTime, entryName=self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to set Past time-frame publishing to " + self.entryName2 + " entry")
                return

            writeToLog("INFO","Step 8: Going to upload " + self.entryName3 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to upload " + self.entryName3 + " entry")
                return

            writeToLog("INFO","Step 9: Going to publish " + self.entryName3 + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryName3, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 9: FAILED to publish " + self.entryName3 + " entry")
                return

            writeToLog("INFO","Step 10: Going to set In Scheduling time-frame publishing to " + self.entryName3 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryFutureStartDate,endTime=self.entryFutureStartTime, entryName=self.entryName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to set Future time-frame publishing to " + self.entryName3 + " entry")
                return

            writeToLog("INFO","TEST PASSED: All the audio entries were properly created with Scheduling conditions and published successfully")
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
