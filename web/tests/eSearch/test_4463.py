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
    # Test Name : Filter by Duration - Dependency with other filters - My Media 
    # Test description:
    # Verify that the Duration filter can be used only when specific media types are selected
    #================================================================================================================================
    testNum = "4463"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
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

            self.search = "Filter by caption"
            self.sRChannel = "SR-Channel for eSearch"
            self.gallery = "category for eSearch moderator"

            # Entries and dictionaries            
            entryName1 = enums.MediaType.QUIZ
            entryName2 = enums.MediaType.AUDIO
            entryName3 = enums.MediaType.VIDEO
            entryName4 = enums.MediaType.IMAGE
            entryName5 = enums.MediaType.WEBCAST_EVENTS
                 
            entryListWithFilters = [entryName1, entryName2, entryName3, entryName5]
            entryListWithoutFilters = [entryName4]
            checkBoxLabelValue = "00:00-10:00 min undefined"

            ##################### TEST STEPS - MAIN FLOW #####################            
            writeToLog("INFO","Step 1: Going to navigate to my media page")
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to my media page")
                return
            
            i = 0
            for entry in entryListWithFilters:
                i = i + 1
                writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that specific media types have filter option enabled") 
                if self.common.myMedia.verifyFilterCheckBox(entry, checkBoxLabelValue, status=True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step: " + str(i + 1) + " FAILED, the specific media type has filter option disabled")
                    return
                i = i
                
            i = 0 
            for entry in entryListWithoutFilters:
                i = i + 1
                writeToLog("INFO","Step: " + str(i + 1) + ": Going to verify that filter option for the specific media type is disabled") 
                if self.common.myMedia.verifyFilterCheckBox(entry, checkBoxLabelValue, status=False) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step: " + str(i + 1) + " FAILED, the specific media type has filter enabled")
                    return        
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the media types have proper filters when selected")
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
