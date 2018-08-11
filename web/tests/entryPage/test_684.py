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
    # test Name: Entry page - Navigate to Edit Entry Page from Entry Page
    # Test description: Navigate to edit entry page of media from entry page
    # The test's Flow: 
    # Login to KMS-> Upload 3 entries (audio, image and video) -> Go to entry page > Click on 'Actions' - 'Edit'
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "684"
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
    entriesList= []
    entriesToUpload = []
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
            self.entryName1 = clsTestService.addGuidToString('goToVideoEditPageFromEntryPage', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('goToImageEditPageFromEntryPage', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('goToAudioEditPageFromEntryPage', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            self.entriesToUpload = {
                self.entryName1: self.filePathVideo, 
                self.entryName2: self.filePathImage,
                self.entryName3: self.filePathAudio}
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
                 
                step = step + 1 
                 
                writeToLog("INFO","Step " + str(step) + " : Going to navigate to edit entry page")
                if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(entry)== False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to navigate to edit entry page")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')