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
    entryDescription = "description"
    entryTags = "tag1,"
    embedLink = None
    embedLinkFilePath = 'C:\\xampp\\htdocs\\testPlaylistEmbed673.html'
    embedUrl = 'http://localhost:8080/testPlaylistEmbed673.html'
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
            self.entryName1 = clsTestService.addGuidToString('EmbedPlaylist1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('EmbedPlaylist2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('EmbedPlaylist3', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath }            
              
            writeToLog("INFO","Step 1: Going to upload 3 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return
            
#             writeToLog("INFO","Step 2: Going to add  entries to playlist")
#             if self.common.myPlaylists.addEntriesToPlaylist(self, self.entriesToUpload, playlistName, toCreateNewPlaylist): == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to add entries to playlist")
#                 return
            
            
                                                                  
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')