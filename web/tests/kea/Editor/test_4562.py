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
    #  @Author: Tzachi Guetta
    # Test Name : Trimming a video entry with caption
    # Test description:
    # 
    #================================================================================================================================
    testNum = "4562"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    captionLanguage = 'Afar'
    captionLabel = 'abc'
    captionText = '- Caption search 2'
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"    
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Trim-Caption.srt'    
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
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
            self.entryName = clsTestService.addGuidToString("Upload media - Video", self.testNum)
            expectedEntryDuration = "00:20"
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
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
              
            writeToLog("INFO","Step 4: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
                return    
            
            writeToLog("INFO","Step 5: Going to click on caption tab")
            if self.common.editEntryPage.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to click on caption tab")
                return            
            
            writeToLog("INFO","Step 6: Going to add caption")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to upload caption")
                return   

            writeToLog("INFO","Step 3: Going to collect all the presented captions on the player")  
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.entryName)
            if  self.captionList == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to collect all the presented captions on the player")
                return
            
            self.isExist = ["Caption5search", "Caption7search", "Caption12search", "Caption13search"];
            self.isAbsent = ["Caption100search", "Caption32search"];
            writeToLog("INFO","Step 4: Going to verify the captions that were collected")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify the captions that were collected")
                return               
             
            writeToLog("INFO","Step 2: Going to trim the entry from 30sec to 20sec")  
            if self.common.kea.trimEntry(self.entryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to trim the entry from 30sec to 20sec")
                return
 
            writeToLog("INFO","Step 3: Going to collect all the presented captions on the player (after the entry was trimmed)")  
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.entryName)
            if  self.captionList == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to collect all the presented captions on the player (after the entry was trimmed)")
                return
             
            self.isExist = ["Caption5search", "Caption7search", "Caption22search", "Caption28search"];
            self.isAbsent = ["Caption12search", "Caption13search", "Caption15search", "Caption17search"];
            writeToLog("INFO","Step 4: Going to verify the captions that were collected")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify the captions that were collected")
                return
                
            writeToLog("INFO","TEST PASSED")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')