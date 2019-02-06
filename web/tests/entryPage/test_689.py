import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *
import collections

class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # test Name: Entry page - Add to playlist from entry page
    # Test description: Add entry to playlist from entry page, both for exists playlist and new playlist
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions' - Add to playlist -> choose playlist to add to -> Click save
    # -> Check that entry is added to the playlist
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "689"
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
    entryDescription = "description"
    entryTags = "tag1,"
    existPlaylist = None
    newPlaylistVideo = None
    newPlaylistImage = None
    newPlaylistAudio = None
    newPlaylist = None
    entriesToUpload = []
    playlistList= []
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
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
            self.entryName1 = clsTestService.addGuidToString('addVideoToPlaylistFromEntryPage', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('addImageToPlaylistFromEntryPage', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('addAudioToPlaylistFromEntryPage', self.testNum)
            self.existPlaylist = clsTestService.addGuidToString('existPlaylist', self.testNum)
            self.newPlaylistVideo = clsTestService.addGuidToString('newPlaylistVideo', self.testNum)
            self.newPlaylistImage = clsTestService.addGuidToString('newPlaylistImage', self.testNum)
            self.newPlaylistAudio = clsTestService.addGuidToString('newPlaylistAudio', self.testNum)
            self.playlistList = [self.existPlaylist, self.newPlaylistImage, self.newPlaylistAudio, self.newPlaylistVideo]
            self.entriesToUpload = {
                self.entryName1: self.filePathVideo, 
                self.entryName2: self.filePathImage,
                self.entryName3: self.filePathAudio}
            self.entriesToUpload = collections.OrderedDict(self.entriesToUpload)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            step = 1
            for entry in self.entriesToUpload:
                writeToLog("INFO","Step " + str(step) + " : Going to upload entry")
                if self.common.upload.uploadEntry(self.entriesToUpload.get(entry), entry, self.entryDescription, self.entryTags, disclaimer=False) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to upload entry - " + entry)
                    return    
                  
                step = step + 1  
                  
                writeToLog("INFO","Step " + str(step) + " : Going to navigate to uploaded entry page")
                if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to navigate to entry page")
                    return 
                            
                step = step + 1    
                   
                writeToLog("INFO","Step " + str(step) + " : Going to wait until media will finish processing")
                if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED - New entry is still processing")
                    return
                 
                # Refresh page
                self.common.base.refresh()
                  
                step = step + 1 
                  
                if step == 4:  
                    writeToLog("INFO","Step " + str(step) + " : Going to create empty playlist")
                    if self.common.myPlaylists.createEmptyPlaylist(entry, self.existPlaylist) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(step) + " : FAILED to create empty playlist")
                        return 
                      
                    step = step + 1           
                  
                    writeToLog("INFO","Step " + str(step) + " : Going to navigate to entry page")
                    if self.common.entryPage.navigateToEntry(entry) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(step) + " : FAILED to navigate to entry page")
                        return               
                          
                    step = step + 1 

                writeToLog("INFO","Step " + str(step) + " : Going to add to exist playlist from entry page")
                # Refresh page
                self.common.base.refresh() 
                if self.common.myPlaylists.addSingleEntryToPlaylist(entry, self.existPlaylist, toCreateNewPlaylist = False, currentLocation = enums.Location.ENTRY_PAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to add entry to exist playlist from entry page")
                    return   
                      
                step = step + 1 
                    
                writeToLog("INFO","Step " + str(step) + " : Going to check entry in exist playlist")
                if self.common.myPlaylists.verifySingleEntryInPlaylist(self.existPlaylist, entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to find entry in exist playlist")
                    return          
                    
                step = step + 1 
                     
                writeToLog("INFO","Step " + str(step) + " : Going to navigate to entry page")
                if self.common.entryPage.navigateToEntry(entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to navigate to entry page")
                    return                      
                      
                step = step + 1 
                  
                if "Audio" in entry:
                    self.newPlaylist =self.newPlaylistAudio
                elif "Video" in entry:
                    self.newPlaylist =self.newPlaylistVideo
                else:
                    self.newPlaylist =self.newPlaylistImage
                                      
                writeToLog("INFO","Step " + str(step) + " : Going to add to new playlist from entry page")
                if self.common.myPlaylists.addSingleEntryToPlaylist(entry, self.newPlaylist, toCreateNewPlaylist = True, currentLocation = enums.Location.ENTRY_PAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to add entry to new playlist from entry page")
                    return 
                                                                
                step = step + 1 
                      
                writeToLog("INFO","Step " + str(step) + " : Going to check entry in new  playlist")
                if self.common.myPlaylists.verifySingleEntryInPlaylist(self.newPlaylist, entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to find entry in new playlist")
                    return   
                      
                step = step + 1                                                                                              
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
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])
            self.common.myPlaylists.deleteMultiplePlaylists(self.playlistList)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')
