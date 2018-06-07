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
    # @Author: Oded
    # Test description:
    # 
    #================================================================================================================================
    testNum     = "769"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    driver = None
    common = None
    # Test variables
    entryName1 = "F5383AE8-767-Video2"  
    entryName2 = "F5383AE8-767-Audio"
    entryName3 = "F5383AE8-767-Video"
    entryDescription = "description"
    entryTags = "tag,"
    entriesNames = None
    channelName = "F5383AE8-767-Channel playlist"
    channelDescription = "description"
    channelTags = "tag,"
    embedLink = None
    embedLinkFilePath = 'C:\\xampp\\htdocs\\testEmbed769.html'
    embedUrl = 'http://localhost/testEmbed769.html'
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
#             self.entryName1 = clsTestService.addGuidToString('Video1', self.testNum)
#             self.entryName2 = clsTestService.addGuidToString('Video2', self.testNum)
#             self.entryName3 = clsTestService.addGuidToString('Video3', self.testNum)
#              self.channelName = clsTestService.addGuidToString('F5383AE8-767-Channel playlist', self.testNum)
            self.playlisTitle = clsTestService.addGuidToString('Channel playlist', self.testNum)
            self.entriesNames = [self.entryName1, self.entryName2, self.entryName3]
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return    
             
            
            writeToLog("INFO","Step 9: Going to create channel playlist")                                     
            if self.common.channel.createChannelPlaylist(self.channelName, self.playlisTitle, self.playlistDescription, self.playlistTag, self.entriesNames) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED failed to create channel playlist")
                return 
            sleep(3)
            
            if self.common.channel.navigateToChannelPlaylistTab(self.channelName) == False:   
                writeToLog("INFO","Step 7: FAILED - to navigate to channel playlist tab")
                return                 
            
            self.embedLink = self.common.channel.clickEmbedChannelPlaylistAndGetEmbedCode(self.playlisTitle)
            writeToLog("INFO","FAILED to get playlist id")
            if self.embedLink == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to get embed code")
                return  
                 
            writeToLog("INFO","Step 5: Going to write embed code in file")
            self.common.writeToFile(self.embedLinkFilePath, self.embedLink)
               
              
            writeToLog("INFO","Step 6: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to to embed entry page")
                return  
              
#             writeToLog("INFO","Step 2: Going to upload Video type entry")            
#             if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED failed to upload entry Video")
#                 return
#             
#             writeToLog("INFO","Step 3: Going to upload audio type entry")
#             if self.common.upload.uploadEntry(self.filePath2, self.entryName2, self.entryDescription, self.entryTags) == None:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED failed to upload entry audio")
#                 return 
#             
#             writeToLog("INFO","Step 4: Going to upload video type entry")            
#             if self.common.upload.uploadEntry(self.filePath3, self.entryName3, self.entryDescription, self.entryTags) == None:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED failed to upload entry video")
#                 return                         
#             
#             writeToLog("INFO","Step 5: Going to create new channel")            
#             if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 5: FAILED to create Channel#1")
#                 return
#              
#             writeToLog("INFO","Step 6: Going to publish entry1")
#             if self.common.myMedia.publishSingleEntry(self.entryName1, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
#                 writeToLog("INFO","Step 6: FAILED - could not publish Video to channel")
#                 return
#                 
#             writeToLog("INFO","Step 7: Going to publish entry2")
#             if self.common.myMedia.publishSingleEntry(self.entryName2, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
#                 writeToLog("INFO","Step 7: FAILED - could not publish audio to channel")
#                 return
#             
#             writeToLog("INFO","Step 8: Going to publish entry3")
#             if self.common.myMedia.publishSingleEntry(self.entryName3, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
#                 writeToLog("INFO","Step 8: FAILED - could not publish video to channel")
#                 return
#           
#             expectedEntriesList = [self.entryName1, self.entryName2, self.entryName3]
#            
#             writeToLog("INFO","Step 9: Going to create channel playlist")                                     
#             if self.common.channel.sortAndFilterInChannelPlaylist(self.channelName, self.playlisTitle, self.playlistDescription, self.playlistTag, enums.SortBy.ALPHABETICAL, enums.MediaType.VIDEO) == False:    
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 9: FAILED failed to create channel playlist")
#                 return 
#             sleep(3)     
#             
#             writeToLog("INFO","Step 10: Going to verify entries order - by Alphabetical & video type")
#             if self.common.myMedia.verifyEntriesOrder(expectedEntriesList, enums.Location.CHANNEL_PLAYLIST) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 10: FAILED to verify entries order - by Alphabetical & video type")
#                 return
#            
#             writeToLog("INFO","Step 11: Going to delete channel playlist")              
#             if  self.common.channel.deleteChannelPlaylist(self.channelName, self.playlisTitle) == False:    
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 11: FAILED failed to delete channel playlist")
#                 return      
            #########################################################################
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