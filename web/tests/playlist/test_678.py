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
    # Add Video/ Audio/ Image Entries to Several Playlists from Entry Page
    # The test's Flow: 
    # Login to KMS-> Upload entries (Video/ Audio/ Image) -> add entry to playlist (create new one- DO NOT SAVE) > Upload additional Entry-> add to Play lists (create new one and check previous created)-> Open Entry Page--> Actions--> Add To Playlist--> Check 2 Playlists--> Go to my playlist -> Click on playlist -> Verify both lists contain the 2nd Entry
    #================================================================================================================================
    testNum     = "678"
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
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    playlistName1  = 'emptyPlaylistTest#1'
    playlistName2  = 'PlaylistTest#2'
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'   
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
            self.entryName2 = clsTestService.addGuidToString('EntryVideo', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('EntryAudio', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('EntryImage', self.testNum)             
            self.entriesList = [self.entryName2, self.entryName3, self.entryName4]
            self.listOfPlaylists = [self.playlistName1, self.playlistName2]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePath1, 
                self.entryName2: self.filePathVideo,
                self.entryName3: self.filePathAudio,
                self.entryName4: self.filePathImage}                      
            
            writeToLog("INFO","Step 1: Going to upload 4 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 4 entries")
                return
            
            writeToLog("INFO","Step 2: Going to create Empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName1, self.playlistName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Empty playlist")
                return

            writeToLog("INFO","Step 3: Going to create playlist with 1 Entry")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName1, self.playlistName2, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create playlist with 1 Entry ")
                return
            
            writeToLog("INFO","Step 4: Going to navigate to MyMedia")
            if self.common.myMedia.navigateToMyMedia(self, forceNavigate = False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED going to navigate to MyMedia ")
                return            
            
#             writeToLog("INFO","Step 4: Going to Video Entry Page from MyMedia") 
#             if self.common.myPlaylists.addSingleEntryToMultiplePlaylists(self.entriesList, self.listOfPlaylists, currentLocation = enums.Location.ENTRY_PAGE) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED to add Entry to Multiple Playlists via Entry Page")
#                 return
#             
#             writeToLog("INFO","Step 5: Going to verify Entry in Playlist1")
#             if self.common.myPlaylists.verifySingleEntryInMultiplePlaylists(self.entryName1, self.listOfPlaylists) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 5: FAILED to verify Entry in Playlist1")
#                 return
                                                                      
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
            self.common.myPlaylists.deletePlaylist(self.playlistName1)
            self.common.myPlaylists.deletePlaylist(self.playlistName2)            
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')