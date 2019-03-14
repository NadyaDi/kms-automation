import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
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
    #  @Author: Tzachi Guetta
    # Test description:
    # In case disclaimer module is turned on and set to "before Publish" (and agreeRequired = Yes)
    # The following test will check that publish is prevented before disclaimer's check-box was checked.
    #================================================================================================================================
    testNum     = "1556"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    channelName = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    channelDescription = "Channel description"
    channelTags = "Channeltags1,Channeltags2,"
    categoryList = ['Galleries - Admin', 'Open Gallery - admin owner']
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('Disclaimer', self.testNum)
            self.channelName = clsTestService.addGuidToString('Channel name', self.testNum)
            
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
             
            writeToLog("INFO","Step 2: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PRIVATE, True, True, True) == False:
                writeToLog("INFO","Step 1: FAILED to create Channel")
                return   
            
            writeToLog("INFO","Step 3: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
            
            self.common.admin.adminDisclaimer(True, enums.DisclaimerDisplayArea.BEFORE_PUBLISH, True)
            self.common.home.navigateToHomePage()
            
            writeToLog("INFO","Step 4: Going to publish the entry while Disclaimer before published turned ON")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", [self.channelName], disclaimer=True) == False:
                writeToLog("INFO","Step 4: FAILED publish entry (Disclaimer is on)")
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
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName)
            self.common.admin.adminDisclaimer(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')