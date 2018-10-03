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
    # Test Name : My Channels - Create Channel 
    # Test description:
    # Go to my channels page :
    #    1. Click on 'Create Channel' button
    #    2. Fill out all the fields
    #    3. Choose privacy type 
    #    4. Define as moderated
    #    5. Enable comments
    #    6. Enable subscription (enable in admin)
    #    7. Choose categories
    #    8. Click on 'Save'
    #
    #    1. 'Create a New Channel' page should be opened' 
    #    2-7. Done successfully
    #    8. The channel should be created successfully according to what you have defined.
    #    The following message should be received: "The information was saved successfully"

    #================================================================================================================================
    testNum = "730"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    description = "Description"
    tags = "Tags,"
    channelName = None
    categoryName = None

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
            self.channelName = clsTestService.addGuidToString("My Channels - Create Channel", self.testNum)
            self.categoryName = clsTestService.addGuidToString("Create Channel", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create new category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create category")
                return
             
            writeToLog("INFO","Step 2: Going to clear cache in admin page")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache in admin page")
                return
             
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
             
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, True, True, True, linkToCategoriesList=[self.categoryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED create new channel: " + self.channelName)
                return
              
            writeToLog("INFO","Step 5: Going navigate to channel page")
            if self.common.channel.navigateToChannel(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to channel page: " + self.channelName)
                return
             
            managerName = self.common.login.getLoginUserName()
            writeToLog("INFO","Step 6: Going to verify channel details")
            if self.common.channel.verifyChannelInformation(str(enums.ChannelPrivacyType.OPEN), "0", "1", "0", managerName, appearsInCategoryName=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify channel details")
                return

            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Channels - Create Channel '  was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.channel.deleteChannel(self.channelName)
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')