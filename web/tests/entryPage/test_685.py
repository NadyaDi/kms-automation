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
    # test Name: Entry page - Edit Metadata
    # Test description: edit entry metadata -name, description and tags
    # The test's Flow: 
    # Login to KMS-> Upload 3 entries (audio, image and video) -> Go to entry page > Click on 'Actions' - 'Edit'-> change entry name, description and tags
    # test cleanup: deleting the uploaded files
    #================================================================================================================================
    testNum     = "685"
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
    newEntryName1 = None
    newEntryName2 = None
    newEntryName3 = None
    entryDescription = "description"
    entryTags = "tag1,"
    newDescripiton = 'new description'
    newTags = 'New tag,'
    entriesListToDelete = []
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
            self.entryName1 = clsTestService.addGuidToString('video', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Image', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('Audio', self.testNum)
            self.newEntryName1 = clsTestService.addGuidToString('newVideoName', self.testNum)
            self.newEntryName2 = clsTestService.addGuidToString('newImageName', self.testNum)
            self.newEntryName3 = clsTestService.addGuidToString('newAudioName', self.testNum)
            self.entriesListToDelete = [self.newEntryName1, self.newEntryName2, self.newEntryName3]
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
                
                if "Audio" in entry:
                    newEntryName = self.newEntryName3
                elif "Video" in entry:
                    newEntryName = self.newEntryName1
                else:
                    newEntryName = self.newEntryName2 
                     
                writeToLog("INFO","Step " + str(step) + " : Going to change entry metadata fields")
                if self.common.editEntryPage.changeEntryMetadata (entry, newEntryName, self.newDescripiton, self.newTags)== False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + " : FAILED to change entry metadata fields")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesListToDelete)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')