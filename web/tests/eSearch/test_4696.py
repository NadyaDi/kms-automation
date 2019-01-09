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
    # Test Name : Approve/Reject - with search - Category Page - Pending tab
    # Test description:
    # Going to upload four Video entries, approve and reject them using normal and bulk options
    #================================================================================================================================
    testNum = "4696"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    categoryName = "category for eSearch moderator"
    categoryNamePending = "category for eSearch moderator - Pending tab"
    methodName = "Approve and Reject"

    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    entryDescription = "approve and reject"
    entryTags = "approve,"
    searchTerm = "Approve and Reject"

    userName1 = "admin"
    userPass1 = "123456"

    userName2 = "inbar.willman@kaltura.com"
    userPass2 = "Kaltura1!"

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

            # Category tests in gallery/add to gallery tabs
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator'

            # Entries and dictionaries
            self.entryName1 = "Approve and Reject - video one"
            self.entryName2 = "Approve and Reject - video two"
            self.entryName3 = "Approve and Reject - video three"
            self.entryName4 = "Approve and Reject - video four"

            self.entriesToUpload = {self.entryName1: self.filePath, self.entryName2: self.filePath, self.entryName3: self.filePath, self.entryName4: self.filePath}
            self.entriesToDelete = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]
            self.entriesToPublish = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]

            self.pendingListAll     = {self.entryName1:True, self.entryName2: True, self.entryName3: True, self.entryName4: True}
            self.pendingListOne     = {self.entryName1:False, self.entryName2: True, self.entryName3: True, self.entryName4: True}
            self.pendingListTwo     = {self.entryName1:False, self.entryName2: False, self.entryName3: True, self.entryName4: True}
            self.pendingListThree   = {self.entryName1:False, self.entryName2: False, self.entryName3: False, self.entryName4: True}
            self.pendingListFour    = {self.entryName1:False, self.entryName2: False, self.entryName3: False, self.entryName4: False}

            self.mediaListOne       = {self.entryName1:True, self.entryName2: False, self.entryName3: False, self.entryName4: False}
            self.mediaListTwo       = {self.entryName1:True, self.entryName2: False, self.entryName3: False, self.entryName4: False}
            self.mediaListThree     = {self.entryName1:True, self.entryName2: False, self.entryName3: True, self.entryName4: False}
            self.mediaListFour      = {self.entryName1:True, self.entryName2: False, self.entryName3: True, self.entryName4: False}
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to upload multiple entries for " + self.userName2 + " user")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": Failed to upload multiple entries for " + self.userName2 + " user")
                return
            else:
                i = i + 1
            i = i
 
            for entry in self.entriesToPublish:
                i = i
                writeToLog("INFO","Step " + str(i) + ": Going to publish the " + entry +"  entry")
                if self.common.myMedia.publishSingleEntry(entry, [self.categoryForModerator, self.categoryForEsearch], '', publishFrom = enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to publish the " + entry +"  entry")
                    return
                else:
                    i = i + 1
                i = i

            writeToLog("INFO","Step " + str(i) + ": Going to logout from " + self.userName2)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout from " + self.userName2)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to log in with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log in with " + self.userName1)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryNamePending)
            if self.common.channel.navigateToPendingaTab(self.categoryName, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.channel.makeSearchInPending(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to approve " + self.entryName1 + " entry from " + self.categoryNamePending)
            if self.common.channel.approveEntriesInPandingTab(self.entryName1, enums.Location.PENDING_TAB) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to approve " + self.entryName1 + " entry from " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryNamePending + " entries")
            if self.common.channel.verifyFiltersInPendingTab(self.pendingListOne) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryNamePending + " entries")
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryName)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToMedia=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryName)
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.category.searchInCategoryWithoutVerifyResults(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryName + " entries")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.mediaListOne) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryName + " entries")
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryNamePending)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToPending=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.channel.makeSearchInPending(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to reject " + self.entryName2 + " entry from " + self.categoryNamePending)
            if self.common.channel.rejectEntriesInPandingTab(self.entryName2, enums.Location.PENDING_TAB) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to reject " + self.entryName2 + " entry from " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryNamePending + " entries")
            if self.common.channel.verifyFiltersInPendingTab(self.pendingListTwo) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryNamePending + " entries")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryName)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToMedia=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryName)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.category.searchInCategoryWithoutVerifyResults(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryName + " entries")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.mediaListTwo) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryName + " entries")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryNamePending)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToPending=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.channel.makeSearchInPending(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to bulk approve " + self.entryName3 + " entry from " + self.categoryNamePending)
            if self.common.channel.pendingBulkRejectAndApprove(self.entryName3, moderateAction=enums.PendingModerateAction.APPROVE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to bulk approve " + self.entryName3 + " entry from " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryNamePending + " entries")
            if self.common.channel.verifyFiltersInPendingTab(self.pendingListThree) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryNamePending + " entries")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryName)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToMedia=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryName)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.category.searchInCategoryWithoutVerifyResults(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryName + " entries")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.mediaListThree) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryName + " entries")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryNamePending)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToPending=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.channel.makeSearchInPending(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to bulk reject " + self.entryName4 + " entry from " + self.categoryNamePending)
            if self.common.channel.pendingBulkRejectAndApprove(self.entryName4, moderateAction=enums.PendingModerateAction.REJECT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to bulk approve " + self.entryName4 + " entry from " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryNamePending + " entries")
            if self.common.channel.verifyFiltersInPendingTab(self.pendingListFour, noEntriesExpected=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryNamePending + " entries")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.categoryName)
            if self.common.channel.switchBetweenMediaAndPendingWithRefresh(switchToMedia=True, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.categoryName)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going  to search by " + self.searchTerm + " in " + self.categoryNamePending)
            if self.common.category.searchInCategoryWithoutVerifyResults(self.searchTerm) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search by " + self.searchTerm + " in " + self.categoryNamePending)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to verify " + self.categoryName + " entries")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.mediaListFour) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify " + self.categoryName + " entries")
                return
            else:
                i = i + 1
            i = i
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries were properly displayed in " + self.categoryName + " and " + self.categoryNamePending + " while approving and rejecting them from  using normal and bulk options")
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)

    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName2, self.userPass2)
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesToDelete, showAllEntries=True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')