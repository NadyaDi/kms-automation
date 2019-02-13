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
    # Test Name:
    # Test description:
    # Replace entry media
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions'-->'Edit' -> Go to 'Attachment' tab -> Upload attachment
    # -> Check that file is uploaded
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "702"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTag = "tag1,"
    attachmentEntryName = 'automation1.jpeg'
    attachmentTitle = 'attachmentTitle'
    attachmentDescripiton = 'attachmentDescripiton'
    newAttachmentTitle = 'newAttachmentTitle'
    newAttachmentDescripiton = 'newAttachmentDescripiton'    
    filePathMedia = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathDictionary = {}
    
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
            self.entryName = clsTestService.addGuidToString('attachmentsFromMedia', self.testNum)
            self.filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\TestingAutomation.png'
            self.filePathImageDownload = localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + '/TestingAutomation.png'
            self.filePathImageOriginalJenkinsNode = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/images/TestingAutomation.png'
            
            self.filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
            self.filePathAudioDownload = localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + '/audio.mp3'
            self.filePathAudioOriginalJenkinsNode = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/audios/audio.mp3'
            
            self.filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10secQrMidLeftSmall.mp4'
            self.filePathVideoDownload = localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + '/10secQrMidLeftSmall.mp4'
            self.filePathVideoOriginalJenkinsNode = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/videos/10secQrMidLeftSmall.mp4'
                                        
            self.filePathDictionary ={
                self.filePathImageOriginalJenkinsNode: [self.filePathImageDownload, self.filePathImage],
                self.filePathAudioOriginalJenkinsNode: [self.filePathAudioDownload, self.filePathAudio],
                self.filePathVideoOriginalJenkinsNode: [self.filePathVideoDownload, self.filePathVideo]
                }
            
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePathMedia, self.entryName, self.entryDescription, self.entryTag, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return      
                  
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
                  
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                                      
            writeToLog("INFO","Step 4: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
                return     
             
            writeToLog("INFO","Step 5: Going to create temp folder for download")
            if self.common.createFolder(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create temp folder on")
                return
                          
            step = 6
              
            for path in self.filePathDictionary:  
                fileName = self.filePathDictionary[path][1].split("\\")[len(self.filePathDictionary[path][1].split("\\"))-1]   
                writeToLog("INFO","Step " + str(step) + ": Going add attachment")
                if self.common.editEntryPage.addAttachments(self.filePathDictionary[path][1], fileName, self.attachmentTitle, self.attachmentDescripiton) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to add attachment")
                    return   
                   
                step = step + 1   
                    
                writeToLog("INFO","Step " + str(step) + ": Going to edit attachment")
                if self.common.editEntryPage.editAttachmentFields(fileName, self.newAttachmentTitle, self.newAttachmentDescripiton) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to edit attachment fields")
                    return  
  
                step = step + 1    
                
                writeToLog("INFO","Step " + str(step) + ": Going to download attachment file from edit entry page")
                if self.common.editEntryPage.downloadAttachmentFileFromEditPage(path, self.filePathDictionary[path][0]) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to download attachment file from edit entry page")
                    return
                
                step = step + 1 
                
                writeToLog("INFO","Step " + str(step) + ": Going to delete download file from folder")    
                if self.common.deleteFile(self.filePathDictionary[path][0]) == False:    
                    self.status = "Fail"    
                    writeToLog("INFO","Step " + str(step) + ": FAILED to delete download file from folder")    
                    return     
                  
                step = step + 1  
                   
                writeToLog("INFO","Step " + str(step) + ": Going to navigate to entry page")
                if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to navigate to edit entry page")
                    return   
                       
                step = step + 1               
                       
                writeToLog("INFO","Step " + str(step) + ": Going to download attachment file from entry page")
                if self.common.entryPage.downloadAttachmentFromEntryPage(path, self.filePathDictionary[path][0]) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to download attachment file from entry page")
                    return 
                      
                    step = step + 1                                                     
                       
                writeToLog("INFO","Step " + str(step) + ": Going to navigate to edit entry page")
                if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to add attachment")
                    return   
                      
                step = step + 1                                      
           
                writeToLog("INFO","Step " + str(step) + ": Going remove attachment file")
                if self.common.editEntryPage.removeAttachmentFile() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to remove attachment file")
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
            self.common.deleteFolder(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')