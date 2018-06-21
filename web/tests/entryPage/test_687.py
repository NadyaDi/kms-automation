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
    # Check embed entry 
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Go to edit entry page -> click on share -> Choose embed option
    # -> Choose player size -> copy embed code - > Use embed code
    # Go to entry page and continue play entry (not to the end) -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "687"
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
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
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
            self.entryName = clsTestService.addGuidToString('Embed', self.testNum)
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)
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
              
            writeToLog("INFO","Step 4: Going to get embed link")
            self.embedLink = self.common.entryPage.getEmbedLink()
            if self.embedLink == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to get embed link")
                return  
             
            writeToLog("INFO","Step 5: Going to write embed code in file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to write embed code in file")
                return                 
             
            writeToLog("INFO","Step 6: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to to embed entry page")
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
            self.common.deleteFile(self.embedLinkFilePath)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')