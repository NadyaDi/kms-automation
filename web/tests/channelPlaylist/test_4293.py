import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from time import strftime
import pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Oded.berihon 
    # Test name: Embed Channel Playlist
    # Test description:
    # Upload entries - create Channel - publish the entries to channel and create channel playlist while adding the new entries to it.
    # Go back to edit channel playlist page grab the embed code and play it as stand alone page.
    #================================================================================================================================
    testNum     = "4293"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None 
    entryName2 = None
    entryName3 = None
    entryDescription = "description"
    entryTags = "tag,"
    entriesNames = None
    channelName = "F5383AE8-767-Channel playlist"
    channelDescription = "description"
    channelTags = "tag,"
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
    
    
    privacyType = ""
    playlisTitle = None
    playlistDescription = "playlist description"
    playlistTag = "playlisttag,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
   
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Video1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Video2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('Video3', self.testNum)
            self.channelName = clsTestService.addGuidToString('F5383AE8-4293-Embed Channel playlist', self.testNum)
            self.playlisTitle = clsTestService.addGuidToString('Embed Channel playlist', self.testNum)
            self.entriesNames = [self.entryName1, self.entryName2, self.entryName3]
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)            
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload Video type entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry Video")
                return
             
            writeToLog("INFO","Step 2: Going to upload audio type entry")
            if self.common.upload.uploadEntry(self.filePath2, self.entryName2, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 2: FAILED failed to upload entry audio")
                return 
             
            writeToLog("INFO","Step 3: Going to upload video type entry")            
            if self.common.upload.uploadEntry(self.filePath3, self.entryName3, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 3: FAILED failed to upload entry video")
                return             
            
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PUBLIC, False, True, True) == False:
                writeToLog("INFO","Step 4: FAILED to create Channel#1")
                return
            
            writeToLog("INFO","Step 5: Going to publish entries to channel")
            if self.common.myMedia.publishEntriesFromMyMedia([self.entryName1,self.entryName2,self.entryName3], "", [self.channelName]) == False:
                writeToLog("INFO","Step 5: FAILED to publish entries to channel")
                return
            
            writeToLog("INFO","Step 6: Going navigate to channel playlist tab") 
            if self.common.channel.navigateToChannelPlaylistTab(self.channelName) == False:  
                writeToLog("INFO","Step 6: FAILED navigate to channel playlist tab")
                return       
            
            writeToLog("INFO","Step 7: Going to create channel playlist")                                     
            if self.common.channel.createChannelPlaylist(self.channelName, self.playlisTitle, self.playlistDescription, self.playlistTag, self.entriesNames) == False:    
                writeToLog("INFO","Step 7: FAILED to create channel playlist")
                return 
            sleep(3)          
            
            writeToLog("INFO","Step 8: Going to get embed code")
            self.embedLink = self.common.channel.clickEmbedChannelPlaylistAndGetEmbedCode(self.playlisTitle, self.channelName)
            if self.embedLink == False:
                writeToLog("INFO","Step 8: FAILED to get embed code")
                return  
                 
            writeToLog("INFO","Step 9: Going to write embed code in file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                writeToLog("INFO","Step 9: FAILED to write embed code in file")
                return 
              
            writeToLog("INFO","Step 10: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                writeToLog("INFO","Step 10: FAILED navigate to embed entry page")
                return  
            
            writeToLog("INFO","Step 11: Going navigate to home page")              
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 11: FAILED navigate to home page")
                return  
            
            writeToLog("INFO","Step 12: Going to delete channel playlist")              
            if  self.common.channel.deleteChannelPlaylist(self.channelName, self.playlisTitle) == False:    
                writeToLog("INFO","Step 12: FAILED failed to delete channel playlist")
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
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])                 
            self.common.channel.deleteChannel(self.channelName) 
            writeToLog("INFO","**************** Ended: teardown_method *******************")
            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')