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
            
            writeToLog("INFO","Step 1: Going navigate to admin page") 
            if self.common.admin.enableCustomMetadata(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED navigate to admin page")
                return
           
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 3: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create Channel#1")
                return
           
            writeToLog("INFO","Step 5: Going to check entry in my media")          
            if self.common.myMedia.serachAndCheckSingleEntryInMyMedia(self.entryName) == False:
                writeToLog("INFO","FAILED to Check for Entry: '" + self.entryName + "' something went wrong")
                return False
            
            writeToLog("INFO","Step 6: Going to publish entry") 
            if self.common.myMedia.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on Action button, Entry: '" + self.entryName + "' something went wrong")
                return False
            
            writeToLog("INFO","Step 7: Going to wait for massage to display") 
            if self.common.base.wait_visible(self.common.myMedia.MY_MEDIA_DISCLAIMER_MSG) == False:
                writeToLog("INFO","FAILED, Disclaimer alert (before publish) wasn't presented although Disclaimer module is turned on")
                return False                         
                         
            writeToLog("INFO","Step 8: Going to add customdata and publish")
            if self.common.myMedia.addCustomDataAndPublish(self.customfield1, customFieldDropdwon=enums.DepartmentDivision.ENGINEERING) == False: 
                self.status = "Fail"        
                writeToLog("INFO","Step 8: FAILED to add custom data fields")
                return    
            
            writeToLog("INFO","Step 9: Going to publish entry")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 9: FAILED - could not publish Video to channel")
                return
            
            writeToLog("INFO","Step 10: Going to search entry in channel page")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 10: FAILED to find entry in channel")
                return                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Add custom metadata' was done successfully")
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
            self.common.admin.enableCustomMetadata(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')