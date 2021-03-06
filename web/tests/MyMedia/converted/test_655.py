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
    # Test Name: My Media - Add to existing playlist - multiple
    # The test's Flow: 
    # Login to KMS-> Upload entries -> Create Empty playlist -> add entries to existing playlist  from My Media > Go to my playlist -> Check that entries added to new playlist
    # test cleanup: deleting the uploaded files and playlist
    #================================================================================================================================
    testNum     = "655"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    playlistName  = None
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
            self.entryName1 = clsTestService.addGuidToString('addMultipleToPlaylist1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('addMultipleToPlaylist2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('addMultipleToPlaylist3', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            self.playlistName = clsTestService.addGuidToString('MultipleToExistingPlaylist', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################    
            writeToLog("INFO","Step 1: Going to upload 3 entries")
            if self.common.upload.uploadMultipleEntries(self.filePath, self.entriesList, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return
            
            writeToLog("INFO","Step 2: Going to navigate to last uploaded entry, entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                return           
              
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return       
             
            writeToLog("INFO","Step 4: Going to navigate to My media page")
            if self.common.myMedia.navigateToMyMedia(True) == False:
                writeToLog("INFO","Step 4: FAILED navigate to My media page")
                return 
                         
            writeToLog("INFO","Step 4: Going to create empty playlist")
            if self.common.myPlaylists.createEmptyPlaylist(self.entryName3, self.playlistName) == False:
                writeToLog("INFO","Step 4: FAILED to create empty playlist")
                return   
             
            writeToLog("INFO","Step 5: Going to navigate to My Media page")
            if self.common.myMedia.navigateToMyMedia(forceNavigate = True) == False:
                writeToLog("INFO","Step 5: FAILED to navigate to My Media")
                return                             
               
            writeToLog("INFO","Step 6: Going to add  entries to playlist")
            if self.common.myPlaylists.addEntriesToPlaylist(self.entriesList, self.playlistName, False) == False:
                writeToLog("INFO","Step 6: FAILED to add entries to playlist")
                return
               
            writeToLog("INFO","Step 7: Going to verify that all entries were added to playlist")
            if self.common.myPlaylists.verifyMultipleEntriesInPlaylist(self.playlistName, self.entriesList) == False:
                writeToLog("INFO","Step 7: FAILED to find all entries in playlist")
                return                            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Add multiple entries to existing playlist' was done successfully")
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