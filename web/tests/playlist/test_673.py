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
    # test Name: Playlists - Embed playlist
    # Test description:
    # Check embed playlist
    # The test's Flow: 
    # Login to KMS-> Upload entries -> add entries to playlist (create new one) > Go to my playlist -> Click on playlist -> Choose embed option
    # -> Choose layout and color -> copy embed code - > Use embed code
    # Go to entry page and continue play entry (not to the end) -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "673"
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
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    playerWidth = "740"
    playerHeight = "330"
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)        
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('EmbedPlaylist1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('EmbedPlaylist2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('EmbedPlaylist3', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            self.playlistName = clsTestService.addGuidToString('embedPlaylistTest', self.testNum)
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath }
              
            writeToLog("INFO","Step 1: Going to enable secureEmbed in admin")
            if self.common.admin.enableSecureEmbed(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to Enable secure embed")
                return                
            
            writeToLog("INFO","Step 2: Going to login to KMS")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to login to KMS")
                return              
                 
            writeToLog("INFO","Step 3: Going to upload 3 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to upload 3 entries")
                return
               
            writeToLog("INFO","Step 4: Going to add  entries to playlist")
            if self.common.myPlaylists.addEntriesToPlaylist(self.entriesList, self.playlistName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add entries to playlist")
                return
               
            writeToLog("INFO","Step 5: Click on 'Go to my playlist")
            if self.common.base.click(self.common.myPlaylists.GO_TO_PLAYLIST_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to my playlist")
                return        
            
            writeToLog("INFO","Step 6: Get playlist embed code")
            self.embedLink = self.common.myPlaylists.clickEmbedPlaylistAndGetEmbedCode(self.playlistName)
            if self.embedLink == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to get playlist embed code")
                return                 
            
            writeToLog("INFO","Step 7: Going to write embed code in file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to write embed code in file")
                return     
             
            writeToLog("INFO","Step 8: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to to embed entry page")
                return  
            
            writeToLog("INFO","Step 9: Going to check player layout")
            if self.common.myPlaylists.verifyEmbedPlayerSizes(self.playerWidth, self.playerHeight) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to get correct player layout")
                return              
            
            writeToLog("INFO","Step 10: navigate to My Media in order to come back to KMS")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to navigate to to my media")
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