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
    # Replace entry media
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions'-->'Edit' -> Go to 'Attachment' tab -> Upload attachment
    # -> Check that file is uploaded
    # Go to entry page and continue play entry (not to the end) -> 
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
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathAttachment = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation1.jpeg'
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
            self.entryName = clsTestService.addGuidToString('replaceVideo', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
#             writeToLog("INFO","Step 1: Going to upload entry")
#             if self.common.upload.uploadEntry(self.filePathVideo1, self.entryName, self.entryDescription, self.entryTag, disclaimer=False) == None:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entry")
#                 return      
#                
#             writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
#             if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to navigate to entry page")
#                 return           
#                
#             writeToLog("INFO","Step 3: Going to wait until media will finish processing")
#             if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED - New entry is still processing")
#                 return                         
#                
#             writeToLog("INFO","Step 4: Going to navigate to edit entry page")
#             if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
#                 return               
            writeToLog("INFO","Step 5: Going to naviagte to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia('43D41A5A-692-sideBar4') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add attachment")
                return      
                
            writeToLog("INFO","Step 5: Going to add attachment")
            if self.common.editEntryPage.addAttachments(self.filePathAttachment,self.attachmentEntryName, self.attachmentTitle, self.attachmentDescripiton) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add attachment")
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