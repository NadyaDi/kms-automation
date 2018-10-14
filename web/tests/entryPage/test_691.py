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
    # Test name: Entry page - Related Media
    # Test description:
    # Check Related media in entry page
    # The test's Flow: 
    # Login to KMS admin-> Enable side my media -> Login to KMS > Upload entry -> Go to entry page -> Click on related media
    # -> Choose 'My Media' -> Check that My media entries are displayed 
    # test cleanup: deleting the uploaded files and disabled sideMyMedia module
    #================================================================================================================================
    testNum     = "691"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    relatedLimit = 2
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    categoryName = 'Apps Automation Category'
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
            self.entryTags = clsTestService.addGuidToString('tags', self.testNum)
            self.entryTags = self.entryTags + ','
            
            self.entryName1 = clsTestService.addGuidToString('sideBar1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('sideBar2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('sideBar3', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('sideBar4', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]
            
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath, 
                self.entryName4: self.filePath}
            
            writeToLog("INFO","Setup: Going to enable related media (side my media)")
            if self.common.admin.enableRelatedMedia(True, self.relatedLimit) == False:
                self.status = "Fail"
                writeToLog("INFO","Setup: FAILED to enable related media (side my media)")
                return            
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return              
               
            writeToLog("INFO","Step 2: Going to upload 4 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 4 entries")
                return
            
            writeToLog("INFO","Step 2.1: Going to publish 4 entries")
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesList, [self.categoryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2.1: FAILED to publish 4 entries")
                return
              
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
              
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return                         
            
            writeToLog("INFO","Step 4: Going to verify count of entries in related section, expected:" + str(self.relatedLimit))
            if self.common.entryPage.verifyRelatedMediaCount(self.relatedLimit) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED displayed correct count of entries in related section")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')