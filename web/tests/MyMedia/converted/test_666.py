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
    # Test Name : My Media - Filter by status
    # Test description:
    # upload 5 entries from all types: image / audio / video
    # some of the entries live as private /publish /Unlisted /Pending / Rejected
    # In the Status filter:
    #    1. Filter by 'Private' -  Only Private entries should be displayed 
    #    2. Filter by 'Published' - Only Published entries should be displayed
    #    3. Filter by 'Pending' - Only Pending entries should be displayed
    #    4. Filter by 'Rejected' - Only Rejected entries should be displayed
    #    5. Filter by 'Unlisted' - Only Unlisted entries should be displayed
    #    6. Filter by 'All Media' - All the user's entries should be displayed - in any status..
    # *A compatible label should be displayed on top of the entry's thumbnail.
    #================================================================================================================================
    testNum = "666"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None
    entryName6 = None
    description = "Description" 
    tags = "Tags,"
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filterByImage = None
    filterByAudio = None
    filterByVideo = None
    filterByAllMedia = None
    
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
            self.entryName1 = clsTestService.addGuidToString("My Media - Image 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - Image 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Media - Audio 1", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("My Media - Audio 2", self.testNum)
            self.entryName5 = clsTestService.addGuidToString("My Media - Video 1", self.testNum)
            self.entryName6 = clsTestService.addGuidToString("My Media - Video 2", self.testNum)
            
            
            # each dictionary get a list of entries and bool parameter that indicate if the entry need to be display in the list filter or not
            self.filterByImage = [(self.entryName1, True), (self.entryName2, True), (self.entryName3, False), (self.entryName4, False), (self.entryName5, False), (self.entryName6, False)]
            self.filterByAudio = [(self.entryName1, False), (self.entryName2, False), (self.entryName3, True), (self.entryName4, True), (self.entryName5, False), (self.entryName6, False)]
            self.filterByVideo = [(self.entryName1, False), (self.entryName2, False), (self.entryName3, False), (self.entryName4, False), (self.entryName5, True), (self.entryName6, True)]
            self.filterByAllMedia = [(self.entryName1, True), (self.entryName2, True), (self.entryName3, True), (self.entryName4, True), (self.entryName5, True), (self.entryName6, True)]            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            for i in range(1,3):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new images entries")            
                if self.common.upload.uploadEntry(self.filePathImage, eval('self.entryName'+str(i)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i)))
                    return
                  
            for i in range(3,5):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new audio entries")            
                if self.common.upload.uploadEntry(self.filePathAudio, eval('self.entryName'+str(i)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i)))
                    return
                  
            for i in range(5,7):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new video entries")            
                if self.common.upload.uploadEntry(self.filePathVideo, eval('self.entryName'+str(i)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i)))
                    return 
             
            writeToLog("INFO","Step 8: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to my media")
                return  
             
            writeToLog("INFO","Step 9: Going to filter and verify my media entries by: " + enums.MediaType.IMAGE.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(enums.MediaType.IMAGE, self.filterByImage) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to filter and verify my media entries  by '" + enums.MediaType.IMAGE.value + "'")
                return 
            
            writeToLog("INFO","Step 10: Going to verify that only entries with " + enums.MediaType.IMAGE.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon((self.entryName1, self.entryName2), enums.MediaType.IMAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to filter and verify my media entries  by '" + enums.MediaType.IMAGE.value + "'")
                return 
            
            sleep(1)
            writeToLog("INFO","Step 11: Going to filter and verify my media entries by: " + enums.MediaType.AUDIO.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(enums.MediaType.AUDIO, self.filterByAudio) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to filter and verify my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                return 
            
            writeToLog("INFO","Step 12: Going to verify that only entries with " + enums.MediaType.AUDIO.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon((self.entryName3, self.entryName4), enums.MediaType.AUDIO) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to filter and verify my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                return 
            
            sleep(1)
            writeToLog("INFO","Step 13: Going to filter and verify my media entries by: " + enums.MediaType.VIDEO.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(enums.MediaType.VIDEO, self.filterByVideo) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to filter and verify my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                return 
            
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                writeToLog("INFO","Step 12: Going to verify that only entries with " + enums.MediaType.VIDEO.value + " icon display")  
                if self.common.myMedia.verifyEntryTypeIcon((self.entryName5, self.entryName6), enums.MediaType.VIDEO) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 12: FAILED to filter and verify my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                    return 
            
            sleep(1)
            writeToLog("INFO","Step 14: Going to filter and verify my media entries by: " + enums.MediaType.IMAGE.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(enums.MediaType.ALL_MEDIA, self.filterByAllMedia) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to filter and verify my media entries  by '" + enums.MediaType.ALL_MEDIA.value + "'")
                return 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Media - Filter by media Type' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5, self.entryName6])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')