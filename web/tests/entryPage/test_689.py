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
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    existPlaylist = None
    newPlaylist = None
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
            self.entryName = clsTestService.addGuidToString('addToPlaylistFromEntryPage', self.testNum)
            self.existPlaylist = clsTestService.addGuidToString('existPlaylist', self.testNum)
            self.newPlaylist = clsTestService.addGuidToString('newPlaylist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
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
            
            writeToLog("INFO","Step 4: Going to create empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName, self.playlistName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create empty playlist")
                return   
            
            writeToLog("INFO","Step 5: Going to add entry to exist playlist from entry page")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.existPlaylist, toCreateNewPlaylist = False, currentLocation = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add entry to exist playlist from entry page")
                return                                  
                  
            writeToLog("INFO","Step 6: Going to add entry to new playlist from entry page")
            if self.common.myPlaylists.addSingleEntryToPlaylist(self.entryName, self.newPlaylist, toCreateNewPlaylist = True, currentLocation = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add entry to new playlist from entry page")
                return     
            
            writeToLog("INFO","Step 7: Going to check entry in exist playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.existPlaylist, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to find entry in exist playlist")
                return 
            
            writeToLog("INFO","Step 8: Going to check entry in new  playlist")
            if self.common.myPlaylists.verifySingleEntryInPlaylist(self.newPlaylist, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to find entry in new playlist")
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
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')