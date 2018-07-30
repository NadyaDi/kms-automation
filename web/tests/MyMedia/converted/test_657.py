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
    #  @Author: Inbar Willman
    # Test Name: My Media - Add to an existing playlist - Single
    # The test's Flow: 
    # Login to KMS-> Upload entry -> -> Create empty playlist -> add entry to existing playlist from My Media > Go to my playlist -> Check that entries added to the playlist
    # test cleanup: deleting the uploaded and playlist
    #================================================================================================================================
    testNum     = "657"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    playlistName  = None
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
            self.entryName = clsTestService.addGuidToString('addToExistingPlaylist', self.testNum)
            self.playlistName = clsTestService.addGuidToString('existingPlaylist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################      
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to create empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName, self.playlistName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create empty playlist")
                return            
               
            writeToLog("INFO","Step 3: Going to add  entry to playlist")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.playlistName, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add entry to playlist")
                return
               
            writeToLog("INFO","Step 4: Going to verify that entry was added to playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to find entry in playlist")
                return                           
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Add single entry to existing playlist' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
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