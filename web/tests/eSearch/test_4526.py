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
    # Test Name : Filter by custom-data - no search - Add to channel - My Media tab - negative and positive
    # Test description:
    # Verify that proper entries are displayed based on the custom data by: single date, single text, single list and unlimited text
    #================================================================================================================================
    testNum = "4526"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    searchPage = "Add to channel - My Media tab - no search"
    channelName = "Channel for eSearch"

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
            self.entryName1 = "Filter by custom-data - Video"
            self.entryName2 = "Filter by custom-data - Image"
            self.entryName3 = "Filter by custom-data - Quiz - Quiz"
            self.entryName4 = "Filter by custom-data - Audio"

            self.year = 2018
            self.month = 5
            self.dayEntry1 = "1"
            self.dayEntry2 = "2"
            self.dayEntry3 = "3"
            self.dayEntry4 = "4"
            self.dayInvalid = "22"

            self.textEntry1 = "Video"
            self.textEntry2 = "Image"
            self.textEntry3 = "Quiz"
            self.textEntry4 = "Audio"
            self.textInvalid = "horiacus"

            self.listOne        = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: False}
            self.listTwo        = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False}
            self.listThree      = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False}
            self.listFour       = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: True}
            self.listInvalid    = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: False}

            self.enumListOne = enums.SingleList.LIST_ONE
            self.enumListTwo = enums.SingleList.LIST_TWO
            self.enumListThree = enums.SingleList.LIST_THREE
            self.enumListFour = enums.SingleList.LIST_FOUR
            self.enumListInvalid = enums.SingleList.LIST_SIX

            self.singleDateMap = {self.dayEntry1:self.listOne, self.dayEntry2:self.listTwo, self.dayEntry3:self.listThree, self.dayEntry4:self.listFour}
            self.singleTextMap = {self.textEntry1:self.listOne, self.textEntry2:self.listTwo, self.textEntry3:self.listThree, self.textEntry4:self.listFour}
            self.singleListMap = {self.enumListOne:[self.listOne, enums.SingleList.LIST_ONE.value], self.enumListTwo:[self.listTwo, enums.SingleList.LIST_TWO.value], self.enumListThree:[self.listThree, enums.SingleList.LIST_THREE.value], self.enumListFour:[self.listFour, enums.SingleList.LIST_FOUR.value]}
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.searchPage)
            if self.common.channel.navigateToAddToChannel(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.searchPage)
                return
            else:
                i = i + 1
            i = i
# SINGLE LIST NEGATIVE
            writeToLog("INFO", "STEP " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + enums.SingleList.LIST_SIX.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SINGLE_LIST, enums.SingleList.LIST_SIX) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + enums.SingleList.LIST_SIX.value + "'")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + enums.SingleList.LIST_SIX.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.listInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + enums.SingleList.LIST_SIX.value + "'")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": Failed to clear the search menu")
                return
            else:
                i = i + 1
            i = i
# SINGLE LIST POSITIVE
            for entry in self.singleListMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + self.singleListMap[entry][1] + "'")
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SINGLE_LIST, entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + self.singleListMap[entry][1] + "'")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + self.singleListMap[entry][1] + "'")
                if self.common.channel.verifyFiltersInAddToChannel(self.singleListMap[entry][0]) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + self.singleListMap[entry][1] + "'")
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
# SINGLE TEXT NEGATIVE
            writeToLog("INFO", "STEP " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + enums.FreeText.SINGLE_TEXT.value + " and " + self.textInvalid + " text")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.FREE_TEXT, enums.FreeText.SINGLE_TEXT, text=self.textInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + enums.FreeText.SINGLE_TEXT.value + " and " + self.textInvalid + " text")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + enums.FreeText.SINGLE_TEXT.value + " and " + self.textInvalid + " text")
            if self.common.channel.verifyFiltersInAddToChannel(self.listInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + enums.FreeText.SINGLE_TEXT.value + " and " + self.textInvalid + " text")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": Failed to clear the search menu")
                return
            i = i
# SINGLE TEXT POSITIVE
            for entry in self.singleTextMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by '" + enums.FreeText.SINGLE_TEXT.value + " and " + entry + " text")
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.FREE_TEXT, enums.FreeText.SINGLE_TEXT, text=entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + self.FreeText.SINGLE_TEXT.value + " and " + entry + " text")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to verify filter " + self.searchPage + " entries by '" + enums.FreeText.SINGLE_TEXT.value + " and " + entry + " text")
                if self.common.channel.verifyFiltersInAddToChannel(self.singleTextMap[entry]) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to verify filter " + self.searchPage + " entries by '" + enums.FreeText.SINGLE_TEXT.value + " and " + entry + " text")
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
# SINGLE UNLIMITED NEGATIVE
            writeToLog("INFO", "STEP " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + enums.FreeText.UNLIMITED_TEXT.value + " and " + self.textInvalid + " text")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.FREE_TEXT, enums.FreeText.UNLIMITED_TEXT, text=self.textInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + enums.FreeText.UNLIMITED_TEXT.value + " and " + self.textInvalid + " text")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + enums.FreeText.UNLIMITED_TEXT.value + " and " + self.textInvalid + " text")
            if self.common.channel.verifyFiltersInAddToChannel(self.listInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + enums.FreeText.UNLIMITED_TEXT.value + " and " + self.textInvalid + " text")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": Failed to clear the search menu")
                return
            i = i
# SINGLE UNLIMITED POSITIVE
            for entry in self.singleTextMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by '" + enums.FreeText.UNLIMITED_TEXT.value + " and " + entry + " text")
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.FREE_TEXT, enums.FreeText.UNLIMITED_TEXT, text=entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + self.FreeText.UNLIMITED_TEXT.value + " and " + entry + " text")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to verify filter " + self.searchPage + " entries by '" + enums.FreeText.UNLIMITED_TEXT.value + " and " + entry + " text")
                if self.common.channel.verifyFiltersInAddToChannel(self.singleTextMap[entry]) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to verify filter " + self.searchPage + " entries by '" + enums.FreeText.UNLIMITED_TEXT.value + " and " + entry + " text")
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
# SINGLE DATE NEGATIVE
            writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + enums.SingleDate.DATE.value + "'")
            if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SINGLE_DATE, enums.SingleDate.DATE, year=self.year, month=self.month, day=self.dayInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step " + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + enums.SingleDate.DATE.value + "'")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + enums.SingleDate.DATE.value + "'")
            if self.common.channel.verifyFiltersInAddToChannel(self.listInvalid) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + enums.SingleDate.DATE.value + "'")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO", "STEP " + str(i) + ": Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP " + str(i) + ": Failed to clear the search menu")
                return
            else:
                i = i + 1
            i = i
# SINGLE DATE POSITIVE
#             for entry in self.singleDateMap:
#                 i = i
#                 writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + enums.SortAndFilter.SINGLE_DATE.value + "'")
#                 if self.common.myMedia.SortAndFilter(enums.SortAndFilter.SINGLE_DATE, enums.SingleDate.DATE, year=self.year, month=self.month, day=entry) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + enums.SortAndFilter.SINGLE_DATE.value + "'")
#                     return
#                 else:
#                     i = i + 1
#
#                 writeToLog("INFO", "Step " + str(i) + ": Going to verify filter " + self.searchPage + " entries by: " + enums.SortAndFilter.SINGLE_DATE.value + "'")
#                 if self.common.channel.verifyFiltersInAddToChannel(self.singleDateMap[entry]) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO", "Step" + str(i) + ": FAILED to verify filter " + self.searchPage + " entries  by '" + enums.SortAndFilter.SINGLE_DATE.value + "'")
#                     return
#                 else:
#                     i = i + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in " + self.searchPage + "  while using custom data filters")
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