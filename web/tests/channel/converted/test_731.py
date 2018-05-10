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
    # Test description:
    # Verify that the details that displayed on the channel's information are correct:
    #    1. Entries' number
    #    2. Member's number
    #    3. Subscribers' number
    #    4. Manager name
    #    5. 'Appears in:" 
    #    6. Channel's type
    #================================================================================================================================
    testNum = "731"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelName = None
    categoryName = "Apps Automation Category"

    
    
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
            self.entryName = clsTestService.addGuidToString("Channel page information", self.testNum)
            self.channelName = clsTestService.addGuidToString("Channel page information ", self.testNum)
            self.channelName= [(self.channelName)]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            #self.common.channel.createChannel(self.channelName[0], self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, False)
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
              
            writeToLog("INFO","Step 2: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName[0], self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, True, linkToCategoriesList=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED create new channel")
                return
                
            writeToLog("INFO","Step 3: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", self.channelName, publishFrom = enums.Location.ENTRY_PAGE, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED publish entry '" + self.entryName + "' to channel: " + self.channelName)
                return
             
            writeToLog("INFO","Step 7: Going navigate to my channels page")  
            if self.common.channel.navigateToChannel(self.channelName[0], navigateFrom=enums.Location.MY_CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 7: FAILED navigate to channel: " + self.channelName[0])
                return
            
            writeToLog("INFO","Step 8: Going to verify entry details in channel")
            if self.common.category.verifyEntryDetails(self.entryName, "1", "0", str(len(self.comments))) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify entry details in channel page")
                return
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Channel page information' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName[0])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')