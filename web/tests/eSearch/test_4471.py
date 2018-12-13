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
    # Test Name : Filter by Duration - with search - Category page - pending tab
    # Test description:
    # Verify that category entries are properly displayed in pending tab while using a search term and filter them by Duration
    #================================================================================================================================
    testNum = "4471"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    categoryName = "category for eSearch moderator"
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
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to navigate to Category page - pending tab")
            if self.common.channel.navigateToPendingaTab(self.categoryName, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate Category page - pending tab")
                return

            writeToLog("INFO","Step 2: Going to make a search in Category page - pending tab")
            if self.common.channel.makeSearchInPending(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to make a search in Category page - pending tab")
                return

            writeToLog("INFO", "STEP 3 Going to filter Category page - pending tab entries by: " + enums.Duration.ANY_DURATION.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.ANY_DURATION) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 3: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.ANY_DURATION.value + "'")
                return

            writeToLog("INFO", "STEP 3 Going to verify filter Category page - pending tab entries by: " + enums.Duration.ANY_DURATION.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.allDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 3: FAILED to verify filter Category page - pending tab entries  by '" + enums.Duration.ANY_DURATION.value + "'")
                return

            writeToLog("INFO", "STEP 4: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 5: Going to filter Category page - pending tab entries by: " + enums.Duration.TEN_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.TEN_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 5: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.TEN_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 6: Going to verify filter Category page - pending tab entries by: " + enums.Duration.TEN_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.tenDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 6: FAILED to verify filter Category page - pending tab entries  by '" + enums.Duration.TEN_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 7: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 7: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 8: Going to filter Category page - pending tab entries by: " + enums.Duration.THIRTY_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.THIRTY_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 8: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.THIRTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 9: Going to verify filter global entries by: " + enums.Duration.THIRTY_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.thirtyDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 9: FAILED to verify filter global entries  by '" + enums.Duration.THIRTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 10: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 10: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 11: Going to filter Category page - pending tab entries by: " + enums.Duration.SIXTY_MINUTES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.SIXTY_MINUTES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 11: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.SIXTY_MINUTES.value + "'")
                return


            writeToLog("INFO", "STEP 12: Going to verify filter Category page - pending tab entries by: " + enums.Duration.SIXTY_MINUTES.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.sixtyDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 12: FAILED to verify filter Category page - pending tab entries  by '" + enums.Duration.SIXTY_MINUTES.value + "'")
                return

            writeToLog("INFO", "STEP 13: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 13: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 14: Going to filter Category page - pending tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.CUSTOM) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 14: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 15: Going to verify filter Category page - pending tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.customDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 15: FAILED to verify filter Category page - pending tab entries  by '" + enums.Duration.CUSTOM.value + "'")
                return

            writeToLog("INFO", "STEP 16: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 16: Failed to clear the search menu")

            writeToLog("INFO", "STEP 17: Going to filter Category page - pending tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.DURATION, enums.Duration.CUSTOM) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 17: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.CUSTOM.value + "'")

            writeToLog("INFO", "STEP 18 Going to filter Category page - pending tab entries by: " + enums.Duration.CUSTOM.value + " using special entry limits")
            if self.common.myMedia.filterCustomDuration(55)== False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 18: FAILED to filter Category page - pending tab entries  by '" + enums.Duration.CUSTOM.value + " using special entry limits")

            writeToLog("INFO", "STEP 19 Going to verify filter Category page - pending tab entries by: " + enums.Duration.CUSTOM.value + "'")
            if self.common.channel.verifyFiltersInPendingTab(self.specialDuration) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 19: FAILED to verify filter Category page - pending tab entries  by '" + enums.Duration.CUSTOM.value + "'")
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in Category page - pending tab while using filter by duration with a search term")
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