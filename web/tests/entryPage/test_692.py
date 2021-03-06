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
    # Check 'Side My Media'
    # The test's Flow: 
    # Login to KMS admin-> Enable side my media -> Login to KMS > Upload entry -> Go to entry page -> Click on related media
    # -> Choose 'My Media' -> Check that My media entries are displayed 
    # test cleanup: deleting the uploaded files and disabled sideMyMedia module
    #================================================================================================================================
    testNum     = "692"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entriesList = None
    entriesToDelete = None
    entriesToUpload = []
    entryDescription = "description"
    entryTags = "tag1,"
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('sideBar1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('sideBar2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('sideBar3', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('sideBar4', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            self.entriesToDelete = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]
            self.common.admin.enableSideMyMedia(True)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
                  
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath, 
                self.entryName4: self.filePath}            
               
            writeToLog("INFO","Step 2: Going to upload 4 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 2: FAILED to upload 4 entries")
                return 
              
            writeToLog("INFO","Step 3: Going to navigate to the last uploaded entry page")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName4) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to " + self.entryName4 + " entry page")
                return           
                             
            writeToLog("INFO","Step 4: Going to to click on My media option in Related media")
            if self.common.entryPage.selectRelatedMediaOption() == False:
                writeToLog("INFO","Step 4: FAILED click on 'My media' option")
                return  
            
            writeToLog("INFO","Step 5: Going to to check uploaded entries in My Media side bar")
            if self.common.entryPage.checkMyMediaSideBarEntries(self.entriesList) == False:
                writeToLog("INFO","Step 5: FAILED displayed My Media entries in side bar")
                return                                                                                                  
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesToDelete)
            self.common.admin.enableSideMyMedia(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')