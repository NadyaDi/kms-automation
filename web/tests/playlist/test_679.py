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
    # !!!!!!!!!!!!!!!!!!!!    TODO - Implement method addRemoveExistingPlaylistswhen bus ### and ### are fixed 
    #================================================================================================================================
    #  @Author: Ori Flchtman
    # Test description:
    # Add Video/ Audio/ Image Remove Entry from one of playlist during to add same Entry to new 
    # The test's Flow: 
    # Login to KMS-> Upload entries (Video/ Audio/ Image) 
    # add entries to playlist-> enter each entry-> Actions-> Add to Playlist-> Create new Playlist and uncheck current playlist-> Save->  
    # Verify messages of Create new Playlist, Add to Playlit and remove from playlist
    #================================================================================================================================
    testNum     = "679"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "description"
    entryTags = "tag1,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3' 
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
            self.entryName1 = clsTestService.addGuidToString('Entry1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Entry2', self.testNum)            
            self.playlistName1 = clsTestService.addGuidToString('ExistPlaylist1', self.testNum)
            self.playlistName2 = clsTestService.addGuidToString('ExistPlaylist2', self.testNum)
            self.playlistName3 = clsTestService.addGuidToString('NewPlaylist1', self.testNum)
            self.playlistName4 = clsTestService.addGuidToString('NewPlaylist2', self.testNum)
            self.listOfPlaylists = [self.playlistName1, self.playlistName2]
            self.listOfNewPlaylists = [self.playlistName3, self.playlistName4]                        
            self.entriesList = [self.entryName1, self.entryName2]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
            self.entryName1: self.filePathVideo,
            self.entryName2: self.filePathAudio
            }
            
            
            writeToLog("INFO","Step 1: Going to upload 2 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 2 entries")
                return        
            
            self.common.myMedia.navigateToMyMedia(forceNavigate=True)
            writeToLog("INFO","Step 2: Going to add Video Entry to Playlist1")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName1, self.playlistName1, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add Video Entry to Playlist1")
                return
            
            writeToLog("INFO","Step 3: Going to add Audio Entry to Playlist2")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName2, self.playlistName2, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add Audio Entry to Playlist2")
                return    
            
            writeToLog("INFO","Step 4: select entries and create new playlists")
            if self.common.myPlaylists.removeAddEntriesToPlaylistsAtSameTime(self.entryName1, self.listOfNewPlaylists) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to select entries and create new playlists")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            self.common.myPlaylists.deleteMultiplePlaylists(self.listOfPlaylists)
            self.common.myPlaylists.deleteMultiplePlaylists(self.listOfNewPlaylists)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')