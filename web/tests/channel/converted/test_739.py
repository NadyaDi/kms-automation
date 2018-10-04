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
    # @Author: Inbar Willman
    # Test Name: Channel - Members tab
    # Test description:
    # Add members to channel
    # The test's Flow: 
    # Login to KMS -> Create channel -> Click on 'Actions' --> 'Edit' -> Go to 'Members' tab -> Add new member to the channel -> Edit the member's permission
    # -> Delete member -> Set as owner
    #================================================================================================================================
    testNum     = "739"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    channelName = None
    channelDescription = "Channel description"
    channelTags = "Channeltags1,Channeltags2,"  
    username = 'private'
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
            self.channelName = clsTestService.addGuidToString('Add member to channel', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ######################   
            writeToLog("INFO","Step 1: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create Channel")
                return
 
            writeToLog("INFO","Step 2: Going to add member to channel")
            if self.common.channel.addMembersToChannel(self.channelName, self.username) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add member to channel")
                return  
             
            writeToLog("INFO","Step 3: Going to change member permission")
            if self.common.channel.editChannelMemberPermission(self.username) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED change member permission")
                return  
             
            writeToLog("INFO","Step 4: Going to delete member")
            if self.common.channel.deleteChannelMember(self.username) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to delete member")
                return     
            
            writeToLog("INFO","Step 5: Going to add member to channel")
            if self.common.channel.addMembersToChannel(self.channelName, self.username) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add member to channel")
                return   
             
            writeToLog("INFO","Step 6: Going to set member as owner")
            if self.common.channel.setChannelMemberAsOwner(self.username) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to set member as owner")
                return                                                   
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Channel - Members tab' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.channel.deleteChannel(self.channelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')