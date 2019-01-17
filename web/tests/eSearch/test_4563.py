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
    # Test Name : Filter by Ownership - Dependency with other filters - My Media
    # Test description:
    # Verify that the Publish option is not enabled while using "Filter Media I can Edit" option
    # Verify that the Edit option is  enabled while using "Filter Media I can Edit" option
    # Verify that the Publish option is  enabled while using "Filter Media I can Publish" option
    # Verify that the Edit option is not enabled while using "Filter Media I can Publish" option
    #================================================================================================================================
    testNum = "4563"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    searchPage = "My Media"
    entryName = "Filter by ownership"
    filterMenuName = "Filter by Ownership"

    userEditor = "admin"
    pwEditor = "123456"

    userPublisher = "privateForEsearch"
    pwPublisher ="123456"

    publishID = "Publish"

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
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to navigate to " + self.searchPage)
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to " + self.searchPage)
                return

            writeToLog("INFO", "Step 2: Going to filter " + self.searchPage + " entries by: " + enums.Ownership.MEDIA_EDIT.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.OWNERSHIP, enums.Ownership.MEDIA_EDIT) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 2: FAILED to filter " + self.searchPage + " entries  by '" + enums.Ownership.MEDIA_EDIT.value + "'")
                return

            writeToLog("INFO", "Step 3: Going to verify that the Publish action option is disabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter")
            if self.common.myMedia.verifyActionOptionStatus(self.publishID, disabled=True) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 3: FAILED, the Publish action option is enabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter")
                return

            writeToLog("INFO", "Step 4: Going to verify that the Edit option is enabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter")
            if self.common.base.is_present(self.common.myMedia.EDIT_OPTION_PRESENT_ANY_ENTRY, timeout=5) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 4: FAILED, the Edit option is disabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter")
                return

            writeToLog("INFO", "Step 5: Going to log out from " + self.userEditor + " account")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 5: FAILED to log out from " + self.userEditor + " account")
                return

            writeToLog("INFO", "Step 6: Going to log in with " + self.userPublisher + " account")
            if self.common.login.loginToKMS(self.userPublisher, self.pwPublisher) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 6: FAILED to log in with " + self.userPublisher + " account")
                return

            writeToLog("INFO","Step 7: Going to navigate to " + self.searchPage)
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to " + self.searchPage)
                return

            writeToLog("INFO", "Step 8: Going to filter " + self.searchPage + " entries by: " + enums.Ownership.MEDIA_PUBLISH.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.OWNERSHIP, enums.Ownership.MEDIA_PUBLISH) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 8: FAILED to filter " + self.searchPage + " entries  by '" + enums.Ownership.MEDIA_PUBLISH.value + "'")
                return

            writeToLog("INFO", "Step 9: Going to verify that the Publish action option is disabled while using " + enums.Ownership.MEDIA_PUBLISH.value + " filter")
            if self.common.myMedia.verifyActionOptionStatus(self.publishID, disabled=False)== False:
                self.status = "Fail"
                writeToLog("INFO", "Step 9: FAILED the Publish action option is enabled while using " + enums.Ownership.MEDIA_PUBLISH.value + " filter")
                return

            writeToLog("INFO", "Step 10: Going to verify that the Edit option is disabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter with " + self.userPublisher + " user")
            if self.common.base.wait_element(self.common.myMedia.EDIT_OPTION_PRESENT_PUBLISH_ENTRY, 1, True) != False:
                self.status = "Fail"
                writeToLog("INFO", "Step 10: FAILED the Edit option is enabled while using " + enums.Ownership.MEDIA_EDIT.value + " filter")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the options are properly enabled or disabled while using " + self.filterMenuName + " filter")
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