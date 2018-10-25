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
    #  @Author: Oded berihon
    # Test Name : add custom metadata in order to publish
    # Test description:
    # Upload entry -> Search medie in My Media -> Check entry's checkbox -> Click on 'Action' -> Choose 'publish' -> click on edit page
    # add all required fields click publish via my media page 
    #================================================================================================================================
    testNum = "1592"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    channelName = 'custon data'
    channelDescription = "description"
    channelTags = "tag,"
    privacyType = ""
    channelList = [(channelName)]
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    customfield1 = "customfield1"
 

    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('add custom data', self.testNum)
            self.channelName = clsTestService.addGuidToString('custom data', self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################  
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Channel#1")
                return
                         
            writeToLog("INFO","Step 3: Going to try and publish entry and then add custom data fields")
            if self.common.myMedia.addCustomDataAndPublish(self.entryName, self.customfield1, customFieldDropdwon=enums.DepartmentDivision.ENGINEERING) == False: 
                self.status = "Fail"        
                writeToLog("INFO","Step 3: FAILED to add custom data fields")
                return    
            
            writeToLog("INFO","Step 4: Going to publish entry")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 4: FAILED - could not publish Video to channel")
                return
            
            writeToLog("INFO","Step 5: Going to search entry in channel page")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 5: FAILED to find entry in channel")
                return                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Search in my media' was done successfully")
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