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
    # Test Name : Filter by Ownership - no search - co editor - Add to Gallery - My media tab
    # Test description:
    # Verify that proper entries are displayed while filtering them by ownership
    #================================================================================================================================
    testNum = "4618"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    searchPage = "Add to Gallery - My Media tab - no search"
    filterMenuName = "Filter by Ownership"
    userType = "Co Editor"
    gallery = "category for eSearch moderator"

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
            self.firstypeVideo      = "Filter by Ownership - firstype Video"
            self.firstypeQuiz       = "Filter by Ownership - firstype Quiz - Quiz"
            self.firstypeAudio      = "Filter by Ownership - firstype Audio"
            self.firstypeImage      = "Filter by Ownership - firstype Image"
            self.firstypeYoutube    = "Filter by Ownership - firstype Youtube"
            self.firstypeWebcast    = "Filter by Ownership - firstype Webcast"


            self.secondtypeVideo    = "Filter by Ownership - secondtype Video"
            self.secondtypeQuiz     = "Filter by Ownership - secondtype Quiz - Quiz"
            self.secondtypeAudio    = "Filter by Ownership - secondtype Audio"
            self.secondtypeImage    = "Filter by Ownership - secondtype Image"
            self.secondtypeYoutube  = "Filter by Ownership - secondtype Youtube"
            self.secondtypeWebcast  = "Filter by Ownership - secondtype Webcast"

            self.thirdtypeVideo     = "Filter by Ownership - thirdtype Video"
            self.thirdtypeQuiz      = "Filter by Ownership - thirdtype Quiz - Quiz"
            self.thirdtypeAudio     = "Filter by Ownership - thirdtype Audio"
            self.thirdtypeImage     = "Filter by Ownership - thirdtype Image"
            self.thirdtypeYoutube   = "Filter by Ownership - thirdtype Youtube"
            self.thirdtypeWebcast   = "Filter by Ownership - thirdtype Webcast"

            self.fourthtypeVideo    = "Filter by Ownership - fourthtype Video"
            self.fourthtypeQuiz     = "Filter by Ownership - fourthtype Quiz - Quiz"
            self.fourthtypeAudio    = "Filter by Ownership - fourthtype Audio"
            self.fourthtypeImage    = "Filter by Ownership - fourthtype Image"
            self.fourthtypeYoutube  = "Filter by Ownership - fourthtype Youtube"
            self.fourthtypeWebcast  = "Filter by Ownership - fourthtype Webcast"

            self.listAnyOwner    = {self.firstypeVideo: True, self.firstypeQuiz: True, self.firstypeAudio: True, self.firstypeImage: True, self.firstypeYoutube: True, self.firstypeWebcast: True, self.secondtypeVideo: True, self.secondtypeQuiz: True, self.secondtypeAudio: True, self.secondtypeImage: True, self.secondtypeYoutube: True, self.secondtypeWebcast: True, self.thirdtypeVideo: True, self.thirdtypeQuiz: True, self.thirdtypeAudio: True, self.thirdtypeImage: True, self.thirdtypeYoutube: True, self.thirdtypeWebcast: True, self.fourthtypeVideo: True, self.fourthtypeQuiz: True, self.fourthtypeAudio: True, self.fourthtypeImage: True, self.fourthtypeYoutube: True, self.fourthtypeWebcast: True}
            self.listAllInvalid  = {self.firstypeVideo: False, self.firstypeQuiz: False, self.firstypeAudio: False, self.firstypeImage: False, self.firstypeYoutube: False, self.firstypeWebcast: False, self.secondtypeVideo: False, self.secondtypeQuiz: False, self.secondtypeAudio: False, self.secondtypeImage: False, self.secondtypeYoutube: False, self.secondtypeWebcast: False, self.thirdtypeVideo: False, self.thirdtypeQuiz: False, self.thirdtypeAudio: False, self.thirdtypeImage: False, self.thirdtypeYoutube: False, self.thirdtypeWebcast: False, self.fourthtypeVideo: False, self.fourthtypeQuiz: False, self.fourthtypeAudio: False, self.fourthtypeImage: False, self.fourthtypeYoutube: False, self.fourthtypeWebcast: False}

            self.firstype        = {self.firstypeVideo: True, self.firstypeQuiz: True, self.firstypeAudio: True, self.firstypeImage: True, self.firstypeYoutube: True, self.firstypeWebcast: True, self.secondtypeVideo: False, self.secondtypeQuiz: False, self.secondtypeAudio: False, self.secondtypeImage: False, self.secondtypeYoutube: False, self.secondtypeWebcast: False, self.thirdtypeVideo: False, self.thirdtypeQuiz: False, self.thirdtypeAudio: False, self.thirdtypeImage: False, self.thirdtypeYoutube: False, self.thirdtypeWebcast: False, self.fourthtypeVideo: False, self.fourthtypeQuiz: False, self.fourthtypeAudio: False, self.fourthtypeImage: False, self.fourthtypeYoutube: False, self.fourthtypeWebcast: False}
            self.secondtype      = {self.firstypeVideo: False, self.firstypeQuiz: False, self.firstypeAudio: False, self.firstypeImage: False, self.firstypeYoutube: False, self.firstypeWebcast: False, self.secondtypeVideo: True, self.secondtypeQuiz: True, self.secondtypeAudio: True, self.secondtypeImage: True, self.secondtypeYoutube: True, self.secondtypeWebcast: True, self.thirdtypeVideo: False, self.thirdtypeQuiz: False, self.thirdtypeAudio: False, self.thirdtypeImage: False, self.thirdtypeYoutube: False, self.thirdtypeWebcast: False, self.fourthtypeVideo: False, self.fourthtypeQuiz: False, self.fourthtypeAudio: False, self.fourthtypeImage: False, self.fourthtypeYoutube: False, self.fourthtypeWebcast: False}
            self.thirdtype       = {self.firstypeVideo: False, self.firstypeQuiz: False, self.firstypeAudio: False, self.firstypeImage: False, self.firstypeYoutube: False, self.firstypeWebcast: False, self.secondtypeVideo: False, self.secondtypeQuiz: False, self.secondtypeAudio: False, self.secondtypeImage: False, self.secondtypeYoutube: False, self.secondtypeWebcast: False, self.thirdtypeVideo: True, self.thirdtypeQuiz: True, self.thirdtypeAudio: True, self.thirdtypeImage: True, self.thirdtypeYoutube: True, self.thirdtypeWebcast: True, self.fourthtypeVideo: False, self.fourthtypeQuiz: False, self.fourthtypeAudio: False, self.fourthtypeImage: False, self.fourthtypeYoutube: False, self.fourthtypeWebcast: False}
            self.fourthtype      = {self.firstypeVideo: False, self.firstypeQuiz: False, self.firstypeAudio: False, self.firstypeImage: False, self.firstypeYoutube: False, self.firstypeWebcast: False, self.secondtypeVideo: False, self.secondtypeQuiz: False, self.secondtypeAudio: False, self.secondtypeImage: False, self.secondtypeYoutube: False, self.secondtypeWebcast: False, self.thirdtypeVideo: False, self.thirdtypeQuiz: False, self.thirdtypeAudio: False, self.thirdtypeImage: False, self.thirdtypeYoutube: False, self.thirdtypeWebcast: False, self.fourthtypeVideo: True, self.fourthtypeQuiz: True, self.fourthtypeAudio: True, self.fourthtypeImage: True, self.fourthtypeYoutube: True, self.fourthtypeWebcast: True}

            self.enumAnyOwner      = enums.Ownership.ANY_OWNER
            self.enumMediaOwn      = enums.Ownership.MEDIA_OWN
            self.enumMediaEdit     = enums.Ownership.MEDIA_EDIT
            self.enumMediaPublish  = enums.Ownership.MEDIA_PUBLISH

            self.entriesMap = {self.enumMediaOwn:[self.listAllInvalid, enums.Ownership.MEDIA_OWN.value, enums.Location.ADD_TO_CHANNEL_MY_MEDIA, True], self.enumMediaPublish:[self.listAllInvalid, enums.Ownership.MEDIA_PUBLISH.value, enums.Location.ADD_TO_CHANNEL_MY_MEDIA, True], self.enumAnyOwner:[self.secondtype, enums.Ownership.ANY_OWNER.value, enums.Location.ADD_TO_CHANNEL_MY_MEDIA, False]}
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.searchPage)
            if self.common.category.navigateToAddToCategory(self.gallery) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.searchPage)
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
                if self.common.channel.verifyFiltersInAddToChannel(self.entriesMap[entry][0], self.entriesMap[entry][2], self.entriesMap[entry][3]) == False:
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