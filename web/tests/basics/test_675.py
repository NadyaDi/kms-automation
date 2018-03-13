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
    # Playlist reorder
    #================================================================================================================================
    testNum     = "675"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None        
    entriesList = None
    playlistName = None        
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
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
            self,capture,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Playlist_entry1')
            self.entryName2 = clsTestService.addGuidToString('Playlist_entry2')
            self.entryName3 = clsTestService.addGuidToString('Playlist_entry3')
            self.entryName4 = clsTestService.addGuidToString('Playlist_entry4')
            self.entryName5 = clsTestService.addGuidToString('Playlist_entry5')
            self.playlistName = clsTestService.addGuidToString('Playlist_reorder', self.testNum)
            self.entriesList = [self.entryName5, self.entryName4, self.entryName3, self.entryName2, self.entryName1]
#           TO-DO: move the below line to "crate evn test"
#           self.common.admin.adminDownloadMedia(True)
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return             
            
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath,
                self.entryName4: self.filePath,
                self.entryName5: self.filePath }
            
            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
            
            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.myPlaylists.addEntriesToPlaylist(self.entriesList, playlistName=self.playlistName, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
            
            entriesListBefore = [self.entryName5, self.entryName4, self.entryName3, self.entryName2, self.entryName1]
            writeToLog("INFO","Step 2: Going to verify entries order before reorder")
            if self.common.myMedia.verifyEntriesOrder(entriesListBefore, location = enums.Location.MY_PLAYLISTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify entries order before reorder")
                return
            
            writeToLog("INFO","Step 3: Going to Shuffle entries inside the playlist")
            if self.common.myPlaylists.shufflePlaylistEntries(self.playlistName, self.entriesList ,0 ,3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to Shuffle entries inside the playlist")
                return
            
            entriesListAfter = [self.entryName4, self.entryName3, self.entryName5, self.entryName2, self.entryName1]
            writeToLog("INFO","Step 2: Going to verify entries order before reorder")
            if self.common.myMedia.verifyEntriesOrder(entriesListAfter, location = enums.Location.MY_PLAYLISTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify entries order before reorder")
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
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')