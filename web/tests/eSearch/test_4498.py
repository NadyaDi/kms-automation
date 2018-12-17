import time, pytest
import sys,os
from _ast import Num
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Filter by Scheduling - with search - Add to channel - SR tab
    # Test description:
    # Verify that Add to channel - SR tab entries are properly displayed while being filtered by scheduling with a search term
    #================================================================================================================================
    testNum = "4498"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    entryName = "Filter by Scheduling"
    channelName = "Channel for eSearch"
    sRChannel = "SR-Channel for eSearch"
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

            # Entries and dictionaries
            self.entryName1 = "Filter by Scheduling - YT future"
            self.entryName2 = "Filter by Scheduling - YT past"
            self.entryName3 = "Filter by Scheduling - YT in scheduling"
            self.entryName4 = "Filter by Scheduling - Video future"
            self.entryName5 = "Filter by Scheduling - Video past"
            self.entryName6 = "Filter by Scheduling - Video In Scheduling"
            self.entryName7 = "Filter by Scheduling - Quiz future - Quiz"
            self.entryName8 = "Filter by Scheduling - Quiz past - Quiz"
            self.entryName9 = "Filter by Scheduling - Quiz In Scheduling - Quiz"
            self.entryName10 = "Filter by Scheduling - Audio future"
            self.entryName11 = "Filter by Scheduling - Audio past"
            self.entryName12 = "Filter by Scheduling - Audio In Scheduling"
            self.entryName13 = "Filter by Scheduling - Image future"
            self.entryName14 = "Filter by Scheduling - Image past"
            self.entryName15 = "Filter by Scheduling - Image In Scheduling"

            self.allAvailabilities = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: True, self.entryName6: True, self.entryName7: True, self.entryName8: True, self.entryName9: True, self.entryName10: True, self.entryName11: True, self.entryName12: True, self.entryName13: True, self.entryName14: True, self.entryName15: True}
            self.futureScheduling = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: True, self.entryName5: False, self.entryName6: False, self.entryName7: True, self.entryName8: False, self.entryName9: False, self.entryName10: True, self.entryName11: False, self.entryName12: False, self.entryName13: True, self.entryName14: False, self.entryName15: False}
            self.availableNow = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False, self.entryName6: True, self.entryName7: False, self.entryName8: False, self.entryName9: True, self.entryName10: False, self.entryName11: False, self.entryName12: True, self.entryName13: False, self.entryName14: False, self.entryName15: True}
            self.pastScheduling = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False, self.entryName5: True, self.entryName6: False, self.entryName7: False, self.entryName8: True, self.entryName9: False, self.entryName10: False, self.entryName11: True, self.entryName12: False, self.entryName13: False, self.entryName14: True, self.entryName15: False}
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to navigate to 'Add to channel'")
            if self.common.channel.navigateToAddToChannel(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to to navigate to 'Add to channel'")
                return

            writeToLog("INFO","Step 2: Going to navigate to 'Add to channel' - 'SR' tab")
            if self.common.channel.navigateToSrTabInAddToChannel(self.sRChannel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to to navigate to 'Add to channel' - 'SR' tab")
                return

            writeToLog("INFO","Step 3: Going to make a search in 'Add to channel' - 'SR' tab")
            if self.common.channel.searchInAddToChannel(self.entryName, tabToSearcFrom=enums.AddToChannelTabs.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to make a search in 'Add to channel' - 'SR' tab")
                return

            writeToLog("INFO", "STEP 4: Going to filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.ALL.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SCHEDULING, enums.Scheduling.ALL) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: FAILED to filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.ALL.value + "'")
                return
 
            writeToLog("INFO", "STEP 5: Going to verify filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.ALL.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.allAvailabilities, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 5: FAILED to verify filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.ALL.value + "'")
                return
 
            writeToLog("INFO", "STEP 6: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 6: Failed to clear the search menu")
                return
 
            writeToLog("INFO", "STEP 7: Going to filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.FUTURE_SCHEDULING.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SCHEDULING, enums.Scheduling.FUTURE_SCHEDULING) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 7: FAILED to filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.FUTURE_SCHEDULING.value + "'")
                return
 
            writeToLog("INFO", "STEP 8: Going to verify filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.FUTURE_SCHEDULING.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.futureScheduling, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 8: FAILED to verify filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.FUTURE_SCHEDULING.value + "'")
                return
 
            writeToLog("INFO", "STEP 9: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 9: Failed to clear the search menu")
                return
 
            writeToLog("INFO", "STEP 10: Going to filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.AVAILABLE_NOW.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SCHEDULING, enums.Scheduling.AVAILABLE_NOW) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 10: FAILED to filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.AVAILABLE_NOW.value + "'")
                return
 
            writeToLog("INFO", "STEP 11: Going to verify filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.AVAILABLE_NOW.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.availableNow, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 11: FAILED to verify filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.AVAILABLE_NOW.value + "'")
                return
 
            writeToLog("INFO", "STEP 12: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 12: Failed to clear the search menu")
                return
 
            writeToLog("INFO", "STEP 13 Going to filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.PAST_SCHEDULING.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SCHEDULING, enums.Scheduling.PAST_SCHEDULING) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 13: FAILED to filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.PAST_SCHEDULING.value + "'")
                return
 
            writeToLog("INFO", "STEP 14: Going to verify filter 'Add to channel' - 'SR' tab entries by: " + enums.Scheduling.PAST_SCHEDULING.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.pastScheduling, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 14: FAILED to verify filter 'Add to channel' - 'SR' tab entries  by '" + enums.Scheduling.PAST_SCHEDULING.value + "'")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in 'Add to channel' - 'SR' while using filter by scheduling")
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
