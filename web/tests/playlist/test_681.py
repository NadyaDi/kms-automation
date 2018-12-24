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
    # Playlists - Add several entries to new and existing playlists
    # The test's Flow: 
    # Login to KMS-> Upload entries -> add entry to playlist (create new one- DO NOT SAVE)
    # Upload additional Entries-> add to Playlists (create new one and check previous created)
    # Go to my playlist -> Click on playlist -> Verify both lists contain the 2nd and 3rd Entries
    #================================================================================================================================
    testNum     = "681"
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
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation.jpg'  
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\BlackFriday.mp4'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\waves.mp3'
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
            self.entryName1 = clsTestService.addGuidToString('Image', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Video', self.testNum) 
            self.entryName3 = clsTestService.addGuidToString('Audio', self.testNum)         
            self.playlistName1  = clsTestService.addGuidToString('emptyPlaylist', self.testNum)
            self.playlistName2  = clsTestService.addGuidToString('Playlist#1', self.testNum)
            self.playlistName3  = clsTestService.addGuidToString('Playlist#2', self.testNum)    
            self.entriesList = [self.entryName1, self.entryName3]
            self.listOfPlaylists = [self.playlistName1, self.playlistName2]
            self.verifylistOfPlaylists = [self.playlistName1, self.playlistName2, self.playlistName3]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePathImage, 
                self.entryName2: self.filePathVideo,
                self.entryName3: self.filePathAudio
                }                      
            
            writeToLog("INFO","Step 1: Going to upload 3 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return
            
            writeToLog("INFO","Step 2: Going to create Empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName1, self.playlistName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Empty playlist")
                return

            writeToLog("INFO","Step 3: Going to create playlist with 1 Entry")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName2, self.playlistName2, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create playlist with 1 Entry ")
                return
            
            writeToLog("INFO","Step 4: Going to add 2 Entries to Multiple Playlists") 
            if self.common.myPlaylists.addEntriesToMultiplePlaylists(self.entriesList, self.listOfPlaylists, self.playlistName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add Entry to Multiple Playlists")
                return
            
            writeToLog("INFO","Step 5: Going to verify Entries in Playlists")
            if self.common.myPlaylists.verifyMultipleEntriesInMultiplePlaylists(self.entriesList, self.verifylistOfPlaylists, isExpected=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify Entries in Playlists")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName1)
            self.common.myPlaylists.deletePlaylist(self.playlistName1)
            self.common.myPlaylists.deletePlaylist(self.playlistName2)
            self.common.myPlaylists.deletePlaylist(self.playlistName3)            
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')