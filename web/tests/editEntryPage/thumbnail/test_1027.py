import time, pytest

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
    # Login to KMS, and upload a media
    # Navigate Edit Entry Page
    # under thumbnail tab change thumnbnail in 3 different ways : Upload, Capture, Auto-Generate
    #================================================================================================================================
    testNum     = "1027"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    uploadThumbnailExpectedResult = 5
    timeToStopPlayer = "0:03"
    captureThumbnailExpectedResult = 3
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10secQrMidLeftSmall.mp4'
    uploadThumbnailFliePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode (5).png'
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Edit entry - thumbnail tab", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            self.common.editEntryPage.captureThumbnail(self.timeToStopPlayer, self.captureThumbnailExpectedResult)
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                     
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                self.status = "Fail"
                return
            
            writeToLog("INFO","Step 3: Going to upload thumbnail in edit Entry Page")
            if self.common.editEntryPage.uploadThumbnail(self.uploadThumbnailFliePath, self.uploadThumbnailExpectedResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to upload thumbnail")
                return
               
            sleep(2)     
            writeToLog("INFO","Step 4: Going to navigate to entry page")            
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry page '" + self.entryName + "'")
                return
               
            writeToLog("INFO","Step 5: Going to check the entry thumbnail in the player")
            if self.common.player.verifyThumbnailInPlayer(self.uploadThumbnailExpectedResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to logout from main user")
                return  
                                 
                                 
                                 
                                 
                                 
                                 
                                 
                                 
            writeToLog("INFO","Step 6: Going to login with the user that was added as Collaborator")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to login with the user that was added as Collaborator")
                return
               
            writeToLog("INFO","Step 7: Going to navigate to entry page from category page with the user that was added as Collaborator")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.categoryList[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to entry page with the user that was added as Collaborator")
                return                                  
             
            writeToLog("INFO","Step 8: Going to publish entry with added as Collaborator user")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", self.channelList, enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to publish entry '" + self.entryName + "' with Collaborator user")
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Entry Collaboration co publish' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                    
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')