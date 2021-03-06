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
    # test Name: Entry page - Publish to channel from entry page
    # Test description: publish entry to channel from entry page
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions' -Publish -> choose channel to publish to -> Click save
    # -> Check that entry is displayed in channel
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "693"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    channelName = None
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
            self.entryName = clsTestService.addGuidToString('publishEntryToChannelFromEntryPage', self.testNum)
            self.channelName = clsTestService.addGuidToString("Entry page - Publish to channel from entry page", self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, False) == False:
                writeToLog("INFO","Step 1: FAILED create new channel")
                return
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return      
              
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
              
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
                  
            writeToLog("INFO","Step 5: Going to publish entry to channel from entry page")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", [self.channelName], publishFrom = enums.Location.ENTRY_PAGE) == False:
                writeToLog("INFO","Step 5: FAILED to publish entry to channel from entry page")
                return                           
                          
            writeToLog("INFO","Step 6: Going to search entry in channel")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED to find entry in channel")
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
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')