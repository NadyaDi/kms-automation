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
    # Test Name : Filter by Publish Statuses - with search - My Media
    # Test description:
    # Verify that my media entries are properly displayed while using a search term and filter them by publish status
    # Quiz needs to be add but we have a blocker issue
    #================================================================================================================================
    testNum = "4504"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    entryName = "Filter by Status"

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
            self.entryName1 = "Filter by Status - Video Private"
            self.entryName2 = "Filter by Status - Video Unlisted"
            self.entryName3 = "Filter by Status - Video Multiple"
            self.entryName4 = "Filter by Status - Audio Private"
            self.entryName5 = "Filter by Status - Audio Unlisted"
            self.entryName6 = "Filter by Status - Audio Multiple"
            self.entryName7 = "Filter by Status - Image Private"
            self.entryName8 = "Filter by Status - Image Unlisted"
            self.entryName9 = "Filter by Status - Image Multiple"
            self.entryName10 = "Filter by Status - Quiz Private - Quiz"
            self.entryName11 = "Filter by Status - Quiz Unlisted - Quiz"
            self.entryName12 = "Filter by Status - Quiz Multiple - Quiz"


            self.allStatuses = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: True, self.entryName6: True, self.entryName7: True, self.entryName8: True, self.entryName9: True, self.entryName10: True, self.entryName11: True, self.entryName12: True}
            self.privateStatus = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: True, self.entryName5: False, self.entryName6: False, self.entryName7: True, self.entryName8: False, self.entryName9: False, self.entryName10: True, self.entryName11: False, self.entryName12: False}
            self.publishedStatus = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False, self.entryName6: True, self.entryName7: False, self.entryName8: False, self.entryName9: True, self.entryName10: False, self.entryName11: False, self.entryName12: True}
            self.pendingStatus = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False, self.entryName6: True, self.entryName7: False, self.entryName8: False, self.entryName9: True, self.entryName10: False, self.entryName11: False, self.entryName12: True}
            self.rejectedStatus = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False, self.entryName6: True, self.entryName7: False, self.entryName8: False, self.entryName9: True, self.entryName10: False, self.entryName11: False, self.entryName12: True}
            self.unlistedStatus = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False, self.entryName5: True, self.entryName6: False, self.entryName7: False, self.entryName8: True, self.entryName9: False, self.entryName10: False, self.entryName11: True, self.entryName12: False}
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to navigate to my media page")
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to my media page")
                return

            writeToLog("INFO","Step 2: Going to make a search in my media page")
            if self.common.myMedia.searchEntryMyMedia(self.entryName, forceNavigate=False, exactSearch=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to make a search in my media page")
                return

            writeToLog("INFO", "STEP 3 Going to filter My Media page entries by: " + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.ALL_STATUSSES) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 3: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                return

            writeToLog("INFO", "STEP 4 Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.allStatuses) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                return

            writeToLog("INFO", "STEP 5: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 5: Failed to clear the search menu")
                return

            writeToLog("INFO", "STEP 6 Going to filter My Media page entries by: " + enums.EntryPrivacyType.PRIVATE.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.PRIVATE) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 6: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                return

            writeToLog("INFO", "STEP 7 Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.PRIVATE.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.privateStatus) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 7: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                return

            writeToLog("INFO", "STEP 8: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 8: Failed to clear the search menu")
                return
            
            writeToLog("INFO", "STEP 9 Going to filter My Media page entries by: " + enums.EntryPrivacyType.PUBLISHED.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.PUBLISHED) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 9: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                return

            writeToLog("INFO", "STEP 10: Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.PUBLISHED.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.publishedStatus) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 10: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                return

            writeToLog("INFO", "STEP 11: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 11: Failed to clear the search menu")
                return
            
            writeToLog("INFO", "STEP 12: Going to filter My Media page entries by: " + enums.EntryPrivacyType.PENDING.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.PENDING) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 12: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.PENDING.value + "'")
                return

            writeToLog("INFO", "STEP 13: Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.PENDING.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.pendingStatus) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 13: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.PENDING.value + "'")
                return

            writeToLog("INFO", "STEP 14: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 14: Failed to clear the search menu")
                return
            
            writeToLog("INFO", "STEP 15: Going to filter My Media page entries by: " + enums.EntryPrivacyType.REJECTED.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.REJECTED) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 15: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                return

            writeToLog("INFO", "STEP 16: Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.REJECTED.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.rejectedStatus) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 16: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                return

            writeToLog("INFO", "STEP 17: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 17: Failed to clear the search menu")
                return
            
            writeToLog("INFO", "STEP 18: Going to filter My Media page entries by: " + enums.EntryPrivacyType.UNLISTED.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PUBLISH_STATUS, enums.EntryPrivacyType.UNLISTED) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 18: FAILED to filter My Media page entries  by '" + enums.EntryPrivacyType.UNLISTED.value + "'")
                return

            writeToLog("INFO", "STEP 19: Going to verify filter My Media page entries by: " + enums.EntryPrivacyType.UNLISTED.value + "'")
            if self.common.myMedia.verifyFiltersInMyMedia(self.unlistedStatus) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 19: FAILED to verify filter My Media page entries  by '" + enums.EntryPrivacyType.UNLISTED.value + "'")
                return

            writeToLog("INFO", "STEP 20: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 20: Failed to clear the search menu")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in My Media page while using filter by publish status")
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
