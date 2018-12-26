import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Ori Flchtman
    # Test description:
    # Playlists - Delete entries from Playlist
    # The test's Flow: 
    # Login to KMS-> Upload entries -> Open My Media -> Select entries -> Action- Add to playlist -> Create New Playlist -> Save ->
    # -> Open Playlist screen -> Select playlist -> Delete several entries -> Verify delete confirmation -> Verify Entries not in Playlist
    #================================================================================================================================
    testNum     = "4542"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    filePathImage1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation.jpg'  
    filePathVideo1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\BlackFriday.mp4'
    filePathAudio1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\waves.mp3'
    filePathImage2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation1.jpeg'  
    filePathVideo2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'
    filePathAudio2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\AudioU2_6.wma'
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
            self.entryName1 = clsTestService.addGuidToString('Image1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Video1', self.testNum) 
            self.entryName3 = clsTestService.addGuidToString('Audio1', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('Image2', self.testNum)
            self.entryName5 = clsTestService.addGuidToString('Video2', self.testNum) 
            self.entryName6 = clsTestService.addGuidToString('Audio2', self.testNum)           
            self.playlistName1  = clsTestService.addGuidToString('newPlaylist', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5, self.entryName6]
            self.entriesListToDelete = [self.entryName1, self.entryName2, self.entryName3]
            self.remainingEntriesInPlaylist = [self.entryName4, self.entryName5, self.entryName6]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePathImage1, 
                self.entryName2: self.filePathVideo1,
                self.entryName3: self.filePathAudio1,
                self.entryName4: self.filePathImage2, 
                self.entryName5: self.filePathVideo2,
                self.entryName6: self.filePathAudio2
                }                      
            
            writeToLog("INFO","Step 1: Going to upload 6 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 6 entries")
                return

            writeToLog("INFO","Step 2: Going to create playlist with 6 entries")
            if self.common.myPlaylists.addEntriesToMultiplePlaylists(self.entriesList, newPlaylistsName=self.playlistName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create playlist with 6 entries")
                return
            
            writeToLog("INFO","Step 3: Going to delete entries from playlist")
            if self.common.myPlaylists.deleteEntriesFromPlalists(self.entriesListToDelete, self.playlistName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete entries from playlist")
                return
            
            writeToLog("INFO","Step 4: Going to verify remaining Entries in Playlists")
            if self.common.myPlaylists.verifyMultipleEntriesInPlaylist(self.playlistName1, self.remainingEntriesInPlaylist, isExpected=True, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify remaining  Entries in Playlists")
                return
            sleep(4)                                                       
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
            self.common.myPlaylists.deletePlaylist(self.playlistName1)  
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)         
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    
 
    pytest.main('test_' + testNum  + '.py --tb=line')