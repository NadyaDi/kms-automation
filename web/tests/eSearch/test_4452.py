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
    # Test Name : Filter by Captions - no search - Add new quiz
    # Test description:
    # Verify that add new quiz entries are properly displayed while using no search term and filter them by captions
    #================================================================================================================================
    testNum = "4452"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    entryName = "Filter by caption"
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
            self.entryName1 = "Filter by caption - with caption audio"
            self.entryName2 = "Filter by caption - with caption video"
            self.entryName3 = "Filter by caption - without caption youtube"
            self.entryName4 = "Filter by caption - without caption audio2"
            self.entryName5 = "Filter by caption - without caption video2"

            self.filterByAvailable = {self.entryName1: True, self.entryName2: True, self.entryName3: False, self.entryName4: False, self.entryName5: False}
            self.filterByNotAvailable = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: True, self.entryName5: True}
            self.filterByAll = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: True}

            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going navigate to add new quiz page")
            if self.common.kea.navigateToEditorMediaSelection(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED navigate to add new quiz page")
                return

            writeToLog("INFO","Step 2: Going to filter add quiz page entries by: " + enums.Captions.ALL.value)
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.ALL) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to filter add quiz page entries  by '" + enums.Captions.ALL.value + "'")
                    return

            writeToLog("INFO","Step 3: Going to verify add quiz page entries filter by: " + enums.Captions.ALL.value)
            if self.common.kea.verifyFiltersInEditor(self.filterByAll) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify add quiz page entries  by '" + enums.Captions.ALL.value + "'")
                return

            writeToLog("INFO", "STEP 4: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: Failed to clear the search menu")
                return

            writeToLog("INFO","Step 5: Going to filter add quiz page entries by: " + enums.Captions.AVAILABLE.value)
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 5: FAILED to filter add quiz page entries  by '" + enums.Captions.AVAILABLE.value + "'")
                    return

            writeToLog("INFO","Step 6: Going to verify add quiz page entries filter by: " + enums.Captions.AVAILABLE.value)
            if self.common.kea.verifyFiltersInEditor(self.filterByAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify add quiz page entries  by '" + enums.Captions.AVAILABLE.value + "'")
                return

            writeToLog("INFO", "STEP 7: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 7: Failed to clear the search menu")
                return

            writeToLog("INFO","Step 8: Going to filter add quiz page entries by: " + enums.Captions.NOT_AVAILABLE.value)
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.NOT_AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 8: FAILED to filter add quiz page entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                    return

            writeToLog("INFO","Step 9: Going to verify add quiz page entries filter by: " + enums.Captions.NOT_AVAILABLE.value)
            if self.common.kea.verifyFiltersInEditor(self.filterByNotAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify add quiz page entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in add new quiz page while using caption filters with no search term")
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
