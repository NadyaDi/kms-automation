import time, pytest,sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Elad Binyamin
    # Test description:
    # Import channel to another channel 
    # 1. Login
    # 2. upload entry
    # 3. create channel #1
    # 4. create channel #2
    # 5. publish the entry from step#2 to channel #1
    # 6. import channel #1 to channel #2
    # 7. verify entry from step#2 presented in channel #2
    #
    #================================================================================================================================
    testNum     = "1557"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    channelName1 = None
    channelName2 = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    channelDescription = "Channel description"
    channelTags = "Channeltags1,Channeltags2,"
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.channelName1 = clsTestService.addGuidToString('Channel name1', self.testNum)
            self.channelName2 = clsTestService.addGuidToString('Channel name2', self.testNum)
            self.entryName1 = clsTestService.addGuidToString('ImportChannel1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('ImportChannel2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('ImportChannel3', self.testNum)
            
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")
            
            self.entriesList = [self.entryName1 ,self.entryName2 ,self.entryName3]
            for entry in self.entriesList:
                if self.common.upload.uploadEntry(self.filePath, entry, self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 1: FAILED failed to upload entry")
                    return
             
            writeToLog("INFO","Step 2: Going to create Channel#1")
            if self.common.channel.createChannel(self.channelName1, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Channel#1")
                return
             
            writeToLog("INFO","Step 3: Going to create Channel#2")
            if self.common.channel.createChannel(self.channelName2, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create Channel#2")
                return
             
            writeToLog("INFO","Step 4: Going to publish single entry")
            if self.common.channel.addContentToChannel(self.channelName1, self.entriesList, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entry to Channel#1")
                return
             
            writeToLog("INFO","Step 5: Going to import channel")
            if self.common.channel.importChannel(self.channelName1, self.channelName2, self.entriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to import channel 1 to Channel#2")
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
            self.common.channel.deleteChannel(self.channelName1)
            self.common.channel.deleteChannel(self.channelName2)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')