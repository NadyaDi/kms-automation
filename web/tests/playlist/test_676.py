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
    # Test description:
    # Add entry to playlist when entry is already exist in playlist
    # The test's Flow: 
    # Login to KMS-> Upload entry -> add entry to playlist -> Go to my playlist -> Click on playlist -> Check that entry is added to playlist
    # -> Go to my media -> add same entry to same playlist -> go to playlist -> Check that entry displayed just once
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "676"
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
    playlistName = None
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
            self.entryName = clsTestService.addGuidToString('entryInPlaylist', self.testNum)
            self.playlistName = clsTestService.addGuidToString('testPlaylist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################        
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
              
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return                          
                 
            writeToLog("INFO","Step 4: Going to add  entry to playlist")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.playlistName, True, currentLocation = enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add entry to playlist")
                return
                 
            writeToLog("INFO","Step 5: Click on 'Go to my playlist")
            if self.common.base.click(self.common.myPlaylists.GO_TO_PLAYLIST_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to my playlist")
                return        
              
            writeToLog("INFO","Step 6: Go to verify that entry is displayed in playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to found entry in playlist")
                return                 
            
            writeToLog("INFO","Step 7: Going add again the entry to the same playlist")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.playlistName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add entry to playlist")
                return
             
            writeToLog("INFO","Step 8: Click on 'Go to my playlist")
            if self.common.base.click(self.common.myPlaylists.GO_TO_PLAYLIST_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to my playlist")
                return  
            
            writeToLog("INFO","Step 9: Check that entry display just once in playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.playlistName, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to to display entry just once in playlist")
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
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')