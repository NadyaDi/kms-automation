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
    expectedEntriesList_Comments = ["C - Automation Entry - Comments", "B - Automation Entry - Views", "A - Automation Entry - Alphabetical",  "D - Automation Entry - Most Recent"]
    expectedEntriesList_Likes = ["E - Automation Entry - Likes", "A - Automation Entry - Alphabetical", "B - Automation Entry - Views",  "D - Automation Entry - Most Recent"]
    expectedEntriesList_Views = ["B - Automation Entry - Views", "A - Automation Entry - Alphabetical", "C - Automation Entry - Comments",  "D - Automation Entry - Most Recent"]
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
            writeToLog("INFO","Step 1: Going to sort entries by Comments")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.COMMENTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to sort entries by Comments")
                return
            
            writeToLog("INFO","Step 2: Going to verify entries order - by comment")
            if self.common.myMedia.verifyEntriesOrder(self.expectedEntriesList_Comments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify entries order - by comment")
                return
            
            writeToLog("INFO","Step 3: Going to sort entries by Likes")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.LIKES) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to sort entries by Likes")
                return
            
            writeToLog("INFO","Step 4: Going to verify entries order - by Likes")
            if self.common.myMedia.verifyEntriesOrder(self.expectedEntriesList_Likes) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify entries order - by Likes")
                return
            
            writeToLog("INFO","Step 5: Going to sort entries by Views")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.VIEWS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to sort entries by Views")
                return
            
            writeToLog("INFO","Step 5: Going to verify entries order - by Views")
            if self.common.myMedia.verifyEntriesOrder(self.expectedEntriesList_Views) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify entries order - by Views")
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