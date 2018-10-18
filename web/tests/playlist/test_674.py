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
    # test Name: Playlists - Delete playlist
    # Test description:
    # Check playlist deleted
    # The test's Flow: 
    # Login to KMS-> Upload entries -> add entries to playlist (create new one) > Go to my playlist -> Click on playlist -> click on delete
    # -> Cancel -> click on delete - > delete
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "674"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    playlistName1  = None
    playlistName2  = None
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
            self.entryName1 = clsTestService.addGuidToString('EntryVideo', self.testNum)            
            self.entriesList = [self.entryName1]
            self.playlistName1 = clsTestService.addGuidToString('deleteEmptyPlaylistTest#1', self.testNum)
            self.playlistName2 = clsTestService.addGuidToString('deletePlaylistTest#2', self.testNum)
            self.listOfPlaylists = [self.playlistName1, self.playlistName2]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePathVideo}          
                 
            writeToLog("INFO","Step 1: Going to upload 1 entry")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 1 entry")
                return
            
            writeToLog("INFO","Step 2: Going to create Empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName1, self.playlistName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Empty playlist")
                return 
            
            self.common.myMedia.navigateToMyMedia(forceNavigate=True)
            writeToLog("INFO","Step 3: Going to create playlist with 1 Entry")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName1, self.playlistName2, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create playlist with 1 Entry ")
                return    
            
            self.common.myPlaylists.navigateToMyPlaylists(forceNavigate=True)           
            writeToLog("INFO","Step 4: Going to delete multiple playlists")
            if self.common.myPlaylists.deleteMultiplePlaylists(self.listOfPlaylists) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to delete multiple playlists")
                return              
                                                                   
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Playlists - Embed playlist' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            self.common.deleteFile(self.embedLinkFilePath)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')