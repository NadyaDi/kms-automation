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
    # The function create playlist in kms.
    # in admin page the playlist is added to the playlist list of home page.
    # then in kms admin page we check that the playlist name and entries are correct  
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
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_2.png'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_3.png'
    expectedQRCode1 = 4
    expectedQRCode2 = 2
    expectedQRCode3 = 3
    playlistName = None
    playlistID = None
    playlistType = "Custom Playlist"
    
    
    
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
            
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                self.entryName1 = clsTestService.addGuidToString("Home Page Playlist 1", self.testNum)
                self.entryName2 = clsTestService.addGuidToString("Home Page Playlist 2", self.testNum)
                self.entryName3 = clsTestService.addGuidToString("Home Page Playlist 3", self.testNum)
            elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                self.entryName1 = clsTestService.addGuidToString("1", self.testNum)
                self.entryName2 = clsTestService.addGuidToString("2", self.testNum)
                self.entryName3 = clsTestService.addGuidToString("3", self.testNum)
            
            self.entriesList = [self.entryName3, self.entryName2, self.entryName1]
            
            self.playlistName = clsTestService.addGuidToString("Home Page Playlist", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
    
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
              
            writeToLog("INFO","Step 5: Going to get playlist id")            
            self.playlistID = self.common.myPlaylists.getPlaylistID(self.playlistName)
            if self.playlistID == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to get playlist '" + self.playlistName + "' id")
                return   
              
            writeToLog("INFO","Step 6: Going to set playlist in admin")  
            if self.common.admin.setPlaylistToHomePage(self.playlistName, self.playlistID , self.playlistType) == False:
                writeToLog("INFO","Step 6: FAILED add playlist in admin")
                return
              
            writeToLog("INFO","Step 7: Going to navigate to home page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to home page")
                return
  
            writeToLog("INFO","Step 8: Going verify home page playlist name")
            tmp_playlist_name = (self.common.home.HOME_PLAYLIST[0], self.common.home.HOME_PLAYLIST[1].replace('PLAYLIST', self.playlistName)) 
            if self.common.base.is_visible(tmp_playlist_name) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to find and verify playlist name in home page: " + self.playlistName)
                return
                   
            writeToLog("INFO","Step 9: Going to verify the left entry in the playlist")
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName3, self.expectedQRCode3, 5.81, 1.5, 3.6, 1.15) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED to verify left entry '" + self.entryName3 + "' in playlist '" + self.playlistName + "'")
                    return
                  
                writeToLog("INFO","Step 10: Going to verify the middle entry in the playlist")
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName2, self.expectedQRCode2, 2.7, 1.5, 1.79, 1.15) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 10: FAILED to verify middle entry '" + self.entryName2 + "' in playlist '" + self.playlistName + "'")
                    return
     
                writeToLog("INFO","Step 11: Going to verify the right entry in the playlist")
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName1, self.expectedQRCode1, 1.45, 1.5, 1.23, 1.15) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 11: FAILED to verify right entry '" + self.entryName1 + "' in playlist '" + self.playlistName + "'")
                    return  
                 
            elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                sleep(3)  
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName3, self.expectedQRCode3, 4.17, 1.80, 3.04, 1.39) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED to verify left entry '" + self.entryName3 + "' in playlist '" + self.playlistName + "'")
                    return
                sleep(2)
                writeToLog("INFO","Step 10: Going to verify the middle entry in the playlist")
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName2, self.expectedQRCode2, 2.4, 1.85, 2.14, 1.60) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 10: FAILED to verify middle entry '" + self.entryName2 + "' in playlist '" + self.playlistName + "'")
                    return
                sleep(2)
                writeToLog("INFO","Step 11: Going to verify the right entry in the playlist")
                if self.common.home.verifyEntyNameAndThumbnailInHomePagePlaylist(self.entryName1, self.expectedQRCode1, 1.9, 1.85, 1.73, 1.60) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 11: FAILED to verify right entry '" + self.entryName1 + "' in playlist '" + self.playlistName + "'")
                    return           
                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Home Page Playlist' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            sleep(2)                         
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName2)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName3)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            self.common.admin.deletePlaylistFromHomePage(self.playlistName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')