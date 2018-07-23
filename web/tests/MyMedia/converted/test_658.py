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
    # Test Name: My Media - Add to a new playlist - Single
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Check entry in My Media > Click 'Actions' - 'Add to 'Playlist' -> Create new playlist
    # -> Add entry to the new playlist - > Check that entry is displayed in playlist
    # Go to entry page and continue play entry (not to the end) -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "658"
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
            self.entryName = clsTestService.addGuidToString('addSingleToNewPlaylist', self.testNum)
            self.playlistName = clsTestService.addGuidToString('NewPlaylist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
               
            writeToLog("INFO","Step 2: Going to add entry to new playlist from My Media")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.playlistName, toCreateNewPlaylist = True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add entry to new playlist from My Media")
                return    
            
            writeToLog("INFO","Step 3: Going to verify that entry is added to the new playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to find entry in new playlist")
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