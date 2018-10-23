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
    #  @Author: Inbar Willman
    # Test Name : Setup test for eSearch
    # Test description:
    # Creating new channel for eSearch test in pending tab
    #================================================================================================================================
    testNum = "1"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    filePathForSortBy = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    channelDescription = "Description"
    channelTags = "Tags,"
    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"
    userName3 = "admin"
    userPass3 = "123456"
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)

            # Categories for eSearch test in pending tab channel/gallery
            self.categoryForModerator = 'category for eSearch moderator'
            self.channelForModerator = 'channel moderator for eSearch'
            ##################### TEST STEPS - MAIN FLOW ############################################################# 
            # Create moderated channel as admin user, inbar.willman@kaltura.com will be member in channel
            writeToLog("INFO","Step 1: Going to login with user " + self.userName3)
            if self.common.login.loginToKMS(self.userName3, self.userPass3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName3)
                return  
             
            writeToLog("INFO","Step 2 : Going to create new channel '" + self.channelForModerator)            
            if self.common.channel.createChannel(self.channelForModerator, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED create new channel: " + self.channelForModerator)
                return   
             
            writeToLog("INFO","Step 3 : Going to add member to channel:" + self.userName1)            
            if self.common.channel.addMembersToChannel(self.channelForModerator, self.userName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add member to channel:" + self.userName1)
                return  
             
            writeToLog("INFO","Moderated channel was created successfully")
            #################################################################################

        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 

            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')