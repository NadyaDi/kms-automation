from enum import *
import time, pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #================================================================================================================================
    #  @Author: Tzachi Guetta
    # Test description:
    # In case disclaimer module is turned on and set to "before Publish" 
    # The following test will check that publish is prevented before disclaimer's check-box was checked.
    #================================================================================================================================
    testNum     = "1556"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    channelName = None
    entryDescription = "Tzachi Entry description"
    entryTags = "entrytags1,entrytags2,"
    channelDescription = "Tzachi Channel description"
    channelTags = "Channeltags1,Channeltags2,"
    filePath = "C:\\Users\\tzachi.guetta\\Downloads\\1.JPG"
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ################################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,captur,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString('Tzachi Entry name')
            self.channelName = clsTestService.addGuidToString('Tzachi Channel name') 
               
            ########################### KMS ADMIN SETUP ###########################
            
            self.common.admin.navigateToAdminPage()
            self.common.admin.adminDisclaimer(True, enums.DisclaimerDisplayArea.BEFORE_PUBLISH, True)
            
            ##################### TEST STEPS - MAIN FLOW ##########################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
             
            writeToLog("INFO","Step 2: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PRIVATE, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create Channel")
                return   
               
            writeToLog("INFO","Step 3: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 4: Going to publish the entry while Disclaimer before published turned ON")
            if self.common.myMedia.publishSingleEntryInMyMedia(self.entryName, "", [self.channelName], True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
            ##################################################################
            print("DONE")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName)
            self.common.admin.adminDisclaimer(False)
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')