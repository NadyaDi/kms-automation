import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name: Watch History - Filter by watch status
    # The test's Flow: 
    # Login to KMS-> Upload 3 entries -> Go to entry 1 page and play entry until the end -> Go to entry 2 page and play entry not until the end
    # Go My History page and filter entries by watch status
    # test cleanup: deleting the uploaded files
    #================================================================================================================================
    testNum     = "2702"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "description"
    entryTags = "tag1,"
    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']
    questionNumber = 1
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryStartWatching = clsTestService.addGuidToString('startWatching', self.testNum)
            self.entryCompleteWatching = clsTestService.addGuidToString('completeWatching', self.testNum)
            self.entriesToDelete = [self.entryStartWatching, self.entryCompleteWatching]
            self.entriesToUpload = {
                self.entryStartWatching: self.filePathVideo,
                self.entryCompleteWatching: self.filePathVideo,
                }
            self.filterByAllHistory = {self.entryStartWatching: True, self.entryCompleteWatching: True}
            self.filterByStartWatching = {self.entryStartWatching: True, self.entryCompleteWatching: False}
            self.filterByCompletedWatching = {self.entryStartWatching: False, self.entryCompleteWatching: True}

#             self.filterByAllHistory = {'201D6BED-2702-completeWatching': True, 'DE57CC14-2702-startWatching': True}
#             self.filterByStartWatching = {'201D6BED-2702-completeWatching': False, 'DE57CC14-2702-startWatching': True}
#             self.filterByCompletedWatching = {'201D6BED-2702-completeWatching': True, 'DE57CC14-2702-startWatching': False}
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page - start watching")
            if self.common.entryPage.navigateToEntry(self.entryStartWatching) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page " + self.entryStartWatching)
                return  
                      
            writeToLog("INFO","Step 3: Going to play entry - not until the end")
            if self.common.player.navigateToEntryClickPlayPause(self.entryStartWatching, '0:02') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate and play entry not until the end")
                return 
              
            writeToLog("INFO","Step 4: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to switch to default content")
                return  
              
            writeToLog("INFO","Step 5: Going to navigate to uploaded entry page - complete watching")
            if self.common.entryPage.navigateToEntry(self.entryCompleteWatching) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to entry page " + self.entryCompleteWatching)
                return  
                      
            writeToLog("INFO","Step 6: Going to play entry - not until the end")
            if self.common.player.navigateToEntryClickPlayPause(self.entryCompleteWatching, '0:23', timeout=50) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate and play entry not until the end")
                return 
              
            writeToLog("INFO","Step 7: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to switch to default content")
                return                                               
            
            writeToLog("INFO","Step 8: Going to navigate to history page")
            if self.common.myHistory.navigateToMyHistory(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to history page")
                return
            
            writeToLog("INFO","Step 9: Going to filter entries by watch status - start watching")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.WATCH_STATUS_MENU, dropDownListItem = enums.MyHistoryWatcheStatusItems.STARTED_WATCHING) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to filter entries by watch status - start watching")
                return   
            
            self.common.base.refresh()
            
            writeToLog("INFO","Step 10: Going to filter entries by watch status - start watching - again")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.WATCH_STATUS_MENU, dropDownListItem = enums.MyHistoryWatcheStatusItems.STARTED_WATCHING) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to filter entries by watch status - start watching - again")
                return             
            
            writeToLog("INFO","Step 11: Going to check that correct entries for start watching filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByStartWatching) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to displayed correct entries for start watching")
                return
            
            writeToLog("INFO","Step 12: Going to verify that only entries with " + enums.MyHistoryWatcheStatusItems.STARTED_WATCHING.value + " status are displayed")
            if self.common.myHistory.verifyFilterWatchStatus(enums.MyHistoryWatcheStatusItems.STARTED_WATCHING) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to displayed only entries with " + enums.MyHistoryWatcheStatusItems.STARTED_WATCHING.value + " status")
                return  
            
            writeToLog("INFO","Step 13: Going to filter entries by watch status - complete watching")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.WATCH_STATUS_MENU, dropDownListItem = enums.MyHistoryWatcheStatusItems.COMPLETED_WATCHING) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to filter entries by watch status - complete watching")
                return   
            
            writeToLog("INFO","Step 14: Going to check that correct entries for complete watching filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByCompletedWatching) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to displayed correct entries for complete watching")
                return
            
            writeToLog("INFO","Step 15: Going to verify that only entries with " + enums.MyHistoryWatcheStatusItems.COMPLETED_WATCHING.value + " status are displayed")
            if self.common.myHistory.verifyFilterWatchStatus(enums.MyHistoryWatcheStatusItems.COMPLETED_WATCHING) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to displayed only entries with " + enums.MyHistoryWatcheStatusItems.COMPLETED_WATCHING.value + " status")
                return  
            
            writeToLog("INFO","Step 16: Going to filter entries by watch status - All History")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.WATCH_STATUS_MENU, dropDownListItem = enums.MyHistoryWatcheStatusItems.ALL_HISTORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to filter entries by watch status - All history")
                return   
            
            writeToLog("INFO","Step 17: Going to check that correct entries for complete watching filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByAllHistory) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to displayed correct entries for complete watching")
                return                                                             
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)             
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesToDelete)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')