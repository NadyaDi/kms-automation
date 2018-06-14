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
    # Test Name : My Media - Expand media details 
    # Test description:
    # upload entry and publish it to channel / category
    # in my media go to the published entry and click on its '+' button:
    #    Published in 'section should be displayed and under it a list of channels / categories that the entry is published i
    #================================================================================================================================
    
    testNum = "670"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryName = [("Apps Automation Category")]
    channelName =  "Expand media details Channel"

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
            self.entryName = clsTestService.addGuidToString(" My Media - Expand media details", self.testNum)
            self.channelName = clsTestService.addGuidToString(self.channelName, self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload new entry")            
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload new entry " + self.entryName)
                return
                
            writeToLog("INFO","Step 2: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to my media")
                return  
 
            writeToLog("INFO","Step 3: Going to publish the entry")  
            if self.common.myMedia.publishEntriesFromMyMedia(self.entryName, self.categoryName, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to publish entry '" + self.entryName + "'")
                return 
               
            writeToLog("INFO","Step 4: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create Channel")
                return
               
            sleep(2)       
            writeToLog("INFO","Step 5: Going to publish entry to channel")  
            if self.common.channel.addContentToChannel(self.channelName, self.entryName, isChannelModerate=False, publishFrom = enums.Location.MY_CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry '" + self.entryName + "' to: " + self.channelName)
                return 
            
            writeToLog("INFO","Step 6: Going navigate to my media")  
            if self.common.myMedia.searchEntryMyMedia(self.entryName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate search entry in my media")
                return
            
            writeToLog("INFO","Step 7: Going to verify entry details after expend entry")  
            if self.common.myMedia.expendAndVerifyPublishedEntriesDetails(self.entryName, self.categoryName, [(self.channelName)]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify all entry details after expend")
                return
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Media - Expand media details' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")     
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