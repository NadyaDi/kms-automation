import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','..','lib')))
from time import strftime
import pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from upload import UploadEntry
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test Name : Playlists - Change the entries order
    # Test description:
    # Playlist reorder
    #================================================================================================================================
    testNum     = "675"
    
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Playlist_entry1')
            self.entryName2 = clsTestService.addGuidToString('Playlist_entry2')
            self.entryName3 = clsTestService.addGuidToString('Playlist_entry3')
            self.entryName4 = clsTestService.addGuidToString('Playlist_entry4')
            self.entryName5 = clsTestService.addGuidToString('Playlist_entry5')
            self.entriesListToUpload = [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5]
            
            self.playlistName = clsTestService.addGuidToString('Playlist_reorder', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5]
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return             

            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.upload.uploadMultipleEntries(self.filePath, self.entriesList, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
                                      
            writeToLog("INFO","Step 3: Going to add entries to playlist")
            if self.common.myPlaylists.addEntriesToPlaylist(self.entriesList, playlistName=self.playlistName, toCreateNewPlaylist=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add entries to playlist")
                return
              
            entriesListBefore = [self.entryName5, self.entryName4, self.entryName3, self.entryName2, self.entryName1]
            writeToLog("INFO","Step 4: Going to verify entries order before reorder")
            if self.common.myMedia.verifyEntriesOrder(entriesListBefore, location = enums.Location.MY_PLAYLISTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify entries order before reorder")
                return
            
            writeToLog("INFO","Step 5: Going to Shuffle entries inside the playlist")
            if self.common.myPlaylists.shufflePlaylistEntries(self.playlistName, 5, 3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to Shuffle entries inside the playlist")
                return
            
            entriesListAfter = [self.entryName5, self.entryName4, self.entryName1, self.entryName3, self.entryName2]
            writeToLog("INFO","Step 6: Going to verify entries order before reorder")
            if self.common.myMedia.verifyEntriesOrder(entriesListAfter, location = enums.Location.MY_PLAYLISTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify entries order before reorder")
                return
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Playlists - Change the entries order' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)           
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