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
    # Add 3 images and create playlist
    # Add that playlist to be in the home page carousel from Admin page
    # under carouselInterval set the Interval
    # in home page move between the entries and verify that the entries order are correct 
    #================================================================================================================================
    testNum = "643"
    
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
    playlistID = None
    playlistType = "Custom Playlist"
    carouselInterval = 5
    defaultcarouselInterval = 5
    
    
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
            self.entryName1 = clsTestService.addGuidToString("Playlist 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Playlist 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Playlist 3", self.testNum)
            
            self.entriesList = [self.entryName3, self.entryName2, self.entryName1]
            
            self.playlistName = clsTestService.addGuidToString("Home Page carousel playlist", self.testNum)
            
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
             
            writeToLog("INFO","Step 6: Going to set carousel playlist in admin")  
            if self.common.admin.setCarouselForHomePage(self.playlistType, self.playlistID) == False:
                writeToLog("INFO","Step 6: FAILED set playlist as carousel playlist in admin")
                return
             
            writeToLog("INFO","Step 7: Going to set carousel interval in admin")  
            if self.common.admin.setCarouselInterval(self.carouselInterval) == False:
                writeToLog("INFO","Step 7: FAILED set carousel interval in admin")
                return
            writeToLog("INFO","Step 8: Going to navigate to home page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to home page")
                return
             
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                writeToLog("INFO","Step 9: Going to verify that the entries in the home page carousel are correct")
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName3, self.expectedQRCode3, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName3 + "' display in home page carousel")
                    return
                 
                sleep(self.carouselInterval + 1)
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName2, self.expectedQRCode2, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName2 + "' display in home page carousel")
                    return
                 
                sleep(self.carouselInterval - 1)
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName1, self.expectedQRCode1, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName1 + "' display in home page carousel")
                    return
             
            elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                writeToLog("INFO","Step 9: Going to verify that the entries in the home page carousel are correct")
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName3, self.expectedQRCode3, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName3 + "' display in home page carousel")
                    return
                 
                sleep(self.carouselInterval + 1) 
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName2, self.expectedQRCode2, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName2 + "' display in home page carousel")
                    return
                 
                sleep(self.carouselInterval - 1)
                if self.common.home.verifyEntryInHomePageCarousel(self.entryName1, self.expectedQRCode1, 1.8, 5.56, 1.23, 1.39)  == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED verify entry '" + self.entryName1 + "' display in home page carousel")
                    return
                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Home Page carousel playlist' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            sleep(4)                         
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName2)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName3)
            self.common.myPlaylists.deletePlaylist(self.playlistName)
            self.common.admin.setCarouselForHomePage("Most Recent - All published videos in channel or categories by creation date")
            self.common.admin.setCarouselInterval(self.defaultcarouselInterval)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')