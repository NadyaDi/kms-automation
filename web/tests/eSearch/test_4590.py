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
    # Test Name : Filter by Ownership - with search - co editor - Category Page - pending tab
    # Test description:
    # Verify that proper entries are displayed while filtering them by ownership
    #================================================================================================================================
    testNum = "4590"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    searchPage = "Category Page - pending tab - with search"
    filterMenuName = "Filter by Ownership"
    userType = "Co Editor"
    entryName = "Filter by ownership"
    categoryName = "category for eSearch moderator"

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
            self.entryNameOwner         = "Filter by Ownership - pending owner"
            self.entryNameEditor        = "Filter by Ownership - pending co-editor"
            self.entryNamePublisher     = "Filter by Ownership - pending co-publisher"
            self.entryNameBoth          = "Filter by Ownership - pending both"

            self.listAnyOwner    = {self.entryNameOwner:True, self.entryNameEditor:True, self.entryNamePublisher:True, self.entryNameBoth:True}
            self.listAllInvalid  = {self.entryNameOwner:False, self.entryNameEditor:False, self.entryNamePublisher:False, self.entryNameBoth:False}

            self.listOwner       = {self.entryNameOwner:True, self.entryNameEditor:True, self.entryNamePublisher:True, self.entryNameBoth:True}    
            self.listEditor      = {self.entryNameOwner:False, self.entryNameEditor:True, self.entryNamePublisher:False, self.entryNameBoth:False} 
            self.listPublisher   = {self.entryNameOwner:False, self.entryNameEditor:False, self.entryNamePublisher:True, self.entryNameBoth:False}
            self.listBoth        = {self.entryNameOwner:False, self.entryNameEditor:False, self.entryNamePublisher:False, self.entryNameBoth:True}
            
            self.enumAnyOwner      = enums.Ownership.ANY_OWNER
            self.enumMediaOwn      = enums.Ownership.MEDIA_OWN
            self.enumMediaEdit     = enums.Ownership.MEDIA_EDIT
            self.enumMediaPublish  = enums.Ownership.MEDIA_PUBLISH

            self.entriesMap = {self.enumAnyOwner:[self.listAnyOwner, enums.Ownership.ANY_OWNER.value, False], self.enumMediaOwn:[self.listAllInvalid, enums.Ownership.MEDIA_OWN.value, True], self.enumMediaEdit:[self.listEditor, enums.Ownership.MEDIA_EDIT.value, False], self.enumMediaPublish:[self.listAllInvalid, enums.Ownership.MEDIA_PUBLISH.value, True]}
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.searchPage)
            if self.common.channel.navigateToPendingaTab(self.categoryName, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.searchPage)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to search for " + self.entryName + " in " + self.searchPage)
            if self.common.channel.makeSearchInPending(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search for " + self.entryName + " in " + self.searchPage)
                return
            else:
                i = i + 1
            i = i

            for entry in self.entriesMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + self.entriesMap[entry][1] + "'")
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.OWNERSHIP, entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + self.entriesMap[entry][1] + "'")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + self.entriesMap[entry][1] + " while using a " + self.userType + " user")
                if self.common.channel.verifyFiltersInPendingTab(self.entriesMap[entry][0], self.entriesMap[entry][2]) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + self.entriesMap[entry][1] + " while using a " + self.userType + " user")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to clear the filter search menu")
                if self.common.myMedia.filterClearAllWhenOpened() == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": Failed to clear the search menu")
                    return
                else:
                    i = i + 1
            i = i
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in " + self.searchPage + " while using " + self.filterMenuName + " filter with " + self.userType + " user")
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