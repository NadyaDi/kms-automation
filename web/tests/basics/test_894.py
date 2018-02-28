from time import strftime

import pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test description:
    # 
    #================================================================================================================================
    testNum     = "894"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
    entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
    entryFutureStartDate = (datetime.datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")

    entryFutureStartTime = time.time() + (60*60)
    entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(entryFutureStartTime))
     
    entryPastStartTime = time.time() - (60*60)
    entryPastStartTime= time.strftime("%I:%M %p",time.localtime(entryPastStartTime))
    
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,captur,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ########################################################################
            self.entryName = clsTestService.addGuidToString('DisclaimerEntry', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.myMedia.SortAndFilterInMyMedia(enums.SortBy.VIEWS, enums.EntryPrivacyType.PUBLISHED, enums.MediaType.VIDEO, enums.Collaboration.CO_PUBLISH, enums.Scheduling.FUTURE_SCHEDULING) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return

            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
#             self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')