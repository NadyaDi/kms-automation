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
    # Scheduling media – Add to playlist (anytime, Past, Future)
    #================================================================================================================================
    testNum     = "869"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    playlistName = None
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ########################################################################
            self.entryName = clsTestService.addGuidToString('SchedulingEntry', self.testNum)
            self.playlistName = clsTestService.addGuidToString('Scheduling_Playlist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                         
            writeToLog("INFO","Step 2: Going to add the entry to a playlist")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, toCreateNewPlaylist = True, playlistName = self.playlistName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add the entry from to a playlist")
                return 
            
            writeToLog("INFO","Step 3: Verify if the entry is presented inside the palylist from step #2 (Expected: should be presented)")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName, isExpected=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED, Entry is not presented although it should")
                return                                  

            writeToLog("INFO","Step 4: Going to set Future time-frame publishing to entry ")   
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime, entryName=self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to set Future time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 5: Verify if the entry is presented inside the palylist from step #2 (Expected: should NOT be presented)")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName, isExpected=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED, Entry is  presented although it shouldn't")
                return 
            
            writeToLog("INFO","Step 6: Going to set Past time-frame publishing to entry ")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, entryName=self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to set past time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 7: Verify if the entry is presented inside the palylist from step #2 (Expected: should be presented)")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName, isExpected=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED, Entry is not presented although it should")
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
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')