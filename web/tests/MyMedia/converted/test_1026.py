import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Publish from upload page
    # Test description:
    # 1. Click on 'Add New' and add new media
    # 2. Add entry metadata
    # 3. Publish to channel/category
    # 4. verify that the entry display in channel/ category page
    #================================================================================================================================
    testNum = "1026"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    description = "Description"
    tags = "tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryName = [("Apps Automation Category")]
    channelName = None
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName1 = clsTestService.addGuidToString("Publish from upload page", self.testNum)
            self.channelName = clsTestService.addGuidToString("Channel Publish from upload page", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to create new channel")  
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create new channel")
                return 
               
            writeToLog("INFO","Step 2: Going to upload entry")  
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.description, self.tags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry' " + self.entryName1)
                return 
                                 
            writeToLog("INFO","Step 3: Going to publish entry from upload page")  
            if self.common.myMedia.publishSingleEntry(self.entryName1, self.categoryName, [self.channelName], publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to publish entry' " + self.entryName1 + " to category and channel from upload page")
                return 
            sleep(3)
            writeToLog("INFO","Step 4: Going navigate to category page")
            if self.common.category.navigateToCategory(self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to category: " + self.categoryName[0])
                return
                
            writeToLog("INFO","Step 5: Going to verify entry published to category ")
            if self.common.category.searchEntryInCategory(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to find entry ' " + self.entryName1 + "' in category: " + self.categoryName)
                return 
            
            sleep(3)
            writeToLog("INFO","Step 6: Going navigate to channel page")
            if self.common.channel.navigateToChannel(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to channel: " + self.channelName)
                return
                
            writeToLog("INFO","Step 7: Going to verify entry published to channel")
            if self.common.channel.searchEntryInChannel(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to find entry ' " + self.entryName1 + "' in channel: " + self.channelName)
                return 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Publish from upload page' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            self.common.channel.deleteChannel(self.channelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')