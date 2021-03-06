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
    # Test Name : Filter by Duration - with search - Add to Gallery - SR tab
    # Test description:
    # Verify that Add to Gallery - SR tab entries are properly displayed while using a search term and filter them by duration
    #================================================================================================================================
    testNum = "4478"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    gallery = "category for eSearch moderator"
    sRChannel = "SR-Channel for eSearch"
    entryName = "Filter by Duration"
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
            self.entryName1 = "Filter by Duration - Under ten minutes"
            self.entryName2 = "Filter by Duration - Under thirty minutes"
            self.entryName3 = "Filter by Duration - Under sixty minutes"
            self.entryName4 = "Filter by Duration - Under onehundredandeighty minutes"
            self.entryName5 = "Filter by Duration - Over onehundredandeighty minutes"

            self.allDuration = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: True}
            self.tenDuration = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: False, self.entryName5: False}
            self.thirtyDuration = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False, self.entryName5: False}
            self.sixtyDuration = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False}
            self.customDuration = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: False}
            self.specialDuration = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: True, self.entryName5: False}
            self.betweenDuration = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: True, self.entryName5: False}
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to navigate to Add to Gallery")
            if self.common.category.navigateToAddToCategory(self.gallery) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate Add to Gallery")
                return

            writeToLog("INFO","Step 2: Going to navigate to Add to Gallery - SR tab")
            if self.common.channel.navigateToSrTabInAddToChannel(self.sRChannel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to Add to Gallery - SR tab")
                return

            writeToLog("INFO","Step 3: Going to make a search in Add to Gallery - SR tab")
            if self.common.channel.searchInAddToChannel(self.entryName, tabToSearcFrom=enums.AddToChannelTabs.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to make a search in Add to Gallery - SR tab")
                return

            writeToLog("INFO", "STEP 4: Going to filter Add to Gallery - SR tab entries by: " + enums.Duration.ANY_DURATION.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.ANY_DURATION) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: FAILED to filter Add to Gallery - SR tab entries  by '" + enums.Duration.ANY_DURATION.value + "'")
                return

            writeToLog("INFO", "STEP 5 Going to verify filter Add to Gallery - SR tab entries by: " + enums.Duration.ANY_DURATION.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.allDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 5: FAILED to verify filter Add to Gallery - SR tab entries  by '" + enums.Duration.ANY_DURATION.value + "'")
                return

            writeToLog("INFO", "STEP 6: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 6: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 7 Going to filter Add to Gallery - SR tab entries by: " + enums.Duration.TEN_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.TEN_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 7: FAILED to filter Add to Gallery - SR tab entries  by '" + enums.Duration.TEN_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 8 Going to verify filter Add to Gallery - SR tab entries by: " + enums.Duration.TEN_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.tenDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 8: FAILED to verify filter Add to Gallery - SR tab entries  by '" + enums.Duration.TEN_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 9: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 9: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 10: Going to filter Add to Gallery - SR tab entries by: " + enums.Duration.THIRTY_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.THIRTY_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 10: FAILED to filter Add to Gallery - SR tab entries  by '" + enums.Duration.THIRTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 11 Going to verify filter Add to Gallery - SR tab entries by: " + enums.Duration.THIRTY_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.thirtyDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 11: FAILED to verify filter Add to Gallery - SR tab entries  by '" + enums.Duration.THIRTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 12: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 12: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 13 Going to filter Add to Gallery - SR tab entries by: " + enums.Duration.SIXTY_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.SIXTY_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 13: FAILED to filter Add to Gallery - SR tab entries  by '" + enums.Duration.SIXTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 13 Going to verify filter Add to Gallery - SR tab entries by: " + enums.Duration.SIXTY_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.sixtyDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 13: FAILED to verify filter Add to Gallery - SR tab entries  by '" + enums.Duration.SIXTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 14: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 14: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 15 Going to filter Add to Gallery - SR tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.CUSTOM) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 15: FAILED to filter Add to Gallery - SR tab entries  by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 16 Going to verify filter Add to Gallery - SR tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.customDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 16: FAILED to verify filter Add to Gallery - SR tab entries  by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 17: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 17: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 18 Going to filter Add to Gallery SR Tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.CUSTOM) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 18: FAILED to filter Add to Gallery SR Tab entries by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 19 Going to filter Add to Gallery SR Tab entries by: " + enums.Duration.CUSTOM.value + " using special entry limits")
            if self.common.myMedia.filterCustomDurationUsingSidebar(55, True) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 19: FAILED to filter Add to Gallery SR Tab entries by '" + enums.Duration.CUSTOM.value + " using special entry limits")
                return

            writeToLog("INFO", "STEP 20 Going to verify filter Add to Gallery SR Tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.specialDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 20: FAILED to verify filter Add to Gallery SR Tab entries  by '" + enums.Duration.CUSTOM.value + "'")
                return
                
            writeToLog("INFO", "STEP 21: Going to modify the custom duration limit to default")
            if self.common.myMedia.filterCustomDuration(-65, value="3600")== False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 21: FAILED to modify the custom duration limit to default")
                return
                 
            writeToLog("INFO", "STEP 22: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 22: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 23: Going to filter Global page entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.CUSTOM) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 23: FAILED to filter Global page entries  by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 24: Going to filter Global page entries by: " + enums.Duration.CUSTOM.value + " using special entry limits")
            if self.common.myMedia.filterCustomDurationUsingSidebar(35, True) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 24: FAILED to filter Global page entries  by '" + enums.Duration.CUSTOM.value + " using special entry limits")
                return

            writeToLog("INFO", "STEP 25: Going to filter Global page entries by: " + enums.Duration.CUSTOM.value + " using special entry limits")
            if self.common.myMedia.filterCustomDurationUsingSidebar(-45, False) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 25: FAILED to filter Global page entries  by '" + enums.Duration.CUSTOM.value + " using special entry limits")
                return
                
            writeToLog("INFO", "STEP 26: Going to verify filter Global page entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.betweenDuration, enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 26: FAILED to verify filter Global page entries  by '" + enums.Duration.CUSTOM.value + "'")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in Add to Gallery SR Tab while using filter by duration with a search term")
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
