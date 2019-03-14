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
    # Create empty playlist
    # The test's Flow: 
    # Login to KMS-> Upload entries -> add entry to playlist (create new one- DO NOT SAVE) > Go to my playlist -> Click on playlist -> Verify list is Empty
    #================================================================================================================================
    testNum     = "683"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    playlistName  = 'emptyPlaylistTest'
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'  
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
            self.entryName = clsTestService.addGuidToString('EmptyPlaylist', self.testNum)
            self.entriesList = [self.entryName]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName: self.filePath, 
                 }                       
            
            writeToLog("INFO","Step 1: Going to upload 1 entry")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return
            
            writeToLog("INFO","Step 2: Going to create Empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName, self.playlistName) == False:
                writeToLog("INFO","Step 2: FAILED to create Empty playlist")
                return
            
            writeToLog("INFO","Step 3: Going to verify Empty Playlist in myPlaylists")
            if self.common.myPlaylists.verifyEmptyPlaylistInMyPlaylists(self.playlistName) == False:
                writeToLog("INFO","Step 3: FAILED to find Playlist")
                return                 
                                                                   
            #########################################################################
            self.status = "Pass"
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
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')