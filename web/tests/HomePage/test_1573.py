import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test description:

    #================================================================================================================================
    testNum = "1573"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode middle (1).png'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode middle (2).png'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode middle (3).png'
    expectedQRCode1 = 1
    expectedQRCode2 = 2
    expectedQRCode3 = 3
    playlistName = None
    playlistID = None
    
    
    
    categoryList = [("Apps Automation Category")]
    channelList = ""
    categoryName = None
    whereToPublishFrom = "Entry Page"
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName1 = clsTestService.addGuidToString("Home Page Playlist 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Home Page Playlist 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Home Page Playlist 3", self.testNum)
            
            self.entriesList = [self.entryName3, self.entryName2, self.entryName1]
            
            self.playlistName = clsTestService.addGuidToString("Home Page Playlist", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            playlistID = self.common.myPlaylists.getPlaylistID("9CED306A-1573-Home Page Playlist")
            
            writeToLog("INFO","Step 1: Going to upload entry number 1")
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry number 1")
                return
            
            writeToLog("INFO","Step 2: Going to upload entry number 2")
            if self.common.upload.uploadEntry(self.filePath2, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry number 2")
                return
            
            writeToLog("INFO","Step 3: Going to upload entry number 3")
            if self.common.upload.uploadEntry(self.filePath3, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry number 3")
                return
                 
            writeToLog("INFO","Step 4: Going to create new playlist with entries")
            if self.common.myPlaylists.addEntriesToPlaylist(self.entriesList, self.playlistName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create new playlist '" + self.playlistName + "'")
                return
            
            writeToLog("INFO","Step 5: Going to navigate to home page")
            if self.common.home.navigateToHomePage() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 5: Going verify home page playlist name")
            tmp_playlist_name = (self.common.myPlaylists.PLAYLIST_CHECKBOX[0], self.common.myPlaylists.PLAYLIST_CHECKBOX[1].replace('PLAYLIST_NAME', self.playlistName)) 
            if self.base.is_visible(tmp_playlist_name) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to find and verify playlist name in home page: " + self.playlistName)
                return
                 
            writeToLog("INFO","Step 6: Going to verify the left entry in the playlist")
            if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName1, self.expectedQRCode1, 9.6, 1.81, 2.7, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify left entry '" + self.entryName1 + "' in playlist '" + self.playlistName + "'")
                return
                 
            writeToLog("INFO","Step 7: Going to verify the middle entry in the playlist")
            if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName2, self.expectedQRCode2, 2.7, 1.81, 1.57, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify middle entry '" + self.entryName2 + "' in playlist '" + self.playlistName + "'")
                return

            writeToLog("INFO","Step 8: Going to verify the right entry in the playlist")
            if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName3, self.expectedQRCode3, 1.58, 1.81, 1, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify right entry '" + self.entryName3 + "' in playlist '" + self.playlistName + "'")
                return                 
                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Home Page Playlist' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                            
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName2)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName3)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')