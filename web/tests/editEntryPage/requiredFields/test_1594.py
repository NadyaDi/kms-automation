import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','..','lib')))
from enum import *
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
    #Test Name: Entry required fields
    # Test description:
    # In case required fields are set to an entry, need to check that those entry must be filled before publishing.
    # The following test will check that there is no option to publish entry if required fields aren't filled,
    # And if the required fields are filled entry can be published.
    # The test's Flow: 
    # Login to KMS admin -> Set required fields -> Login to KMS -> Try to publish entry without filling required fields -> Make sure 
    # that entry can't be published -> Edit entry and fill required fields -> Publish entry again -> Make sure that entry was published. 
    # test cleanup: deleting the uploaded file, disable required fields in metadata module.
    #================================================================================================================================
    testNum     = "1594"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryEmptyDescription = ""
    entryEmptyTags = "   ,"
    entryDescription = "description"
    entryTags = "tag1,"
    channelName = None
    channelDescription = "test"
    channelTags = "test,"
    
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4' 
    
    
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
            self.entryName = clsTestService.addGuidToString('Requiredfields', self.testNum)
            self.common.admin.enableRequiredField(True, True, True, True)
            self.channelName = clsTestService.addGuidToString('"test required field"', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
            
            writeToLog("INFO","Step 2: Going to Create channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PRIVATE, False, False, False, linkToCategoriesList='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create channel")
                return
             
            writeToLog("INFO","Step 3: Going to upload entry while required fields turned ON")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryEmptyDescription, self.entryEmptyTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
           
            writeToLog("INFO","Step 4: Going to publish without filling required field")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], [], publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - publish shouldn't be enabled")
                return
      
            writeToLog("INFO","Expected result is failed - publish shouldn't be enabled")
            
            writeToLog("INFO","Step 5: Going to fill required fields")
            if self.common.upload.fillFileUploadEntryDetails(self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to fill tags and description")
                return 
            
            writeToLog("INFO","Step 6: Going to save changes in required fields")
            if self.common.upload.click(self.common.upload.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to save changes")
                return 
            sleep(2)

            self.common.general.waitForLoaderToDisappear()
            sleep(6)
        
            writeToLog("INFO","Step 7: Going to publish entry after filling required fields")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], [self.channelName], publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entry")
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
            self.common.channel.navigateToMyChannels()
            self.common.channel.deleteChannel(self.channelName)
            self.common.admin.enableRequiredField(False, False, True, True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')