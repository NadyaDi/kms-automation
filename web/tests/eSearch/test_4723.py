import time, pytest
import sys,os
from _ast import Num
from _pytest.compat import enum
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
    # Test Name : Filters Section - with search - My Media
    # Test description:
    # Verify that the filters section has proper functionality while using:
    # Filter by media type and custom single list, arrows, remove option and incrementing or decrementing multiple Filter options
    #================================================================================================================================
    testNum = "4723"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    searchPage  = "Filters Section - with search - My Media"
    searchTerm  = "Filter"

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
            #Variables for media type

            self.mediaTypeVideo     = enums.MediaType.VIDEO
            self.mediaTypeQuiz      = enums.MediaType.QUIZ
            self.mediaTypeAudio     = enums.MediaType.AUDIO
            self.mediaTypeImage     = enums.MediaType.IMAGE
            self.mediaTypeWebcast   = enums.MediaType.WEBCAST_EVENTS

            self.singleListOne      = enums.SingleList.LIST_ONE
            self.singleListTwo      = enums.SingleList.LIST_TWO
            self.singleListThree    = enums.SingleList.LIST_THREE
            self.singleListFour     = enums.SingleList.LIST_FOUR
            self.singleListFive     = enums.SingleList.LIST_FIVE
            self.singleListSix      = enums.SingleList.LIST_SIX


            self.sortMediaType          = enums.SortAndFilter.MEDIA_TYPE
            self.sortSingleListType     = enums.SortAndFilter.SINGLE_LIST

            self.sortMultipleMediaOptions    = [self.mediaTypeVideo, self.mediaTypeQuiz, self.mediaTypeAudio, self.mediaTypeImage]
            self.sortAllMediaOptions         = [self.mediaTypeVideo, self.mediaTypeQuiz, self.mediaTypeAudio, self.mediaTypeImage, self.mediaTypeWebcast]
            self.sortAllSingleList           = [self.singleListOne, self.singleListTwo, self.singleListThree, self.singleListFour, self.singleListFive, self.singleListSix]

            self.enableMultipleOption        = [self.sortMultipleMediaOptions, self.sortAllMediaOptions]
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.searchPage)
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.searchPage)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to search for " + self.searchTerm)
            if self.common.myMedia.searchEntryMyMedia(self.searchTerm, forceNavigate=False, exactSearch=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to search for " + self.searchTerm)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that the filter options can increment and decrement")
            if self.common.myMedia.verifyFilterSection(self.sortMediaType, self.sortMultipleMediaOptions, enable=True, disable=True, clearFilterMenu=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step: " + str(i + 1) + " FAILED,the Filter Section cannot be incremented or decrement properly")
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that after all the sort options were selected, the filter will change to 'ALL'")
            if self.common.myMedia.verifyFilterSection(self.sortMediaType, self.sortAllMediaOptions, enable=True, disable=False, clearFilterMenu=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step: " + str(i + 1) + " FAILED,the filter section doesn't properly change to 'ALL' after all the filter option were selected")
                return
            else:
                i = i + 1
            i = i

            for entry in self.sortMultipleMediaOptions:
                i = i + 1
                writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that the " + entry.value + " can be properly enabled and disabled")
                if self.common.myMedia.verifyFilterSection(self.sortMediaType, entry, enable=True, disable=True, clearFilterMenu=False) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step: " + str(i + 1) + " FAILED, the " + entry.value + " cannot be properly enabled and disabled")
                    return
                i = i

            for entry in self.sortAllSingleList:
                i = i + 1
                writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that the " + entry.value + " can be properly enabled and disabled")
                if self.common.myMedia.verifyFilterSection(self.sortSingleListType, entry, enable=True, disable=True, clearFilterMenu=False) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step: " + str(i + 1) + " FAILED, the " + entry.value + " cannot be properly enabled and disabled")
                    return
                i = i
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the Filter section options were properly displayed in the  " + self.searchPage + " page")
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