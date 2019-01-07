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
    # Test Name : Channel page - Edit metadata
    # Test description:
    # 1. Create channel
    # 2. Change the Channel's name / description / tags
    # 3. Choose different categories and check their check boxes
    # 4. Click on Save
    # The information should be saved successfully
    #================================================================================================================================
    testNum = "738"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    description = "Description"
    newDescription = "Edit Description"
    tags = "Tags,"
    newTags = "New Tags,"
    channelName = None
    newChannelName = None
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
            self.channelName = clsTestService.addGuidToString("Channel page - Edit metadata", self.testNum)
            self.newChannelName = clsTestService.addGuidToString("New Channel Name - Edit metadata", self.testNum)
            self.categoryName = clsTestService.addGuidToString("Category-Edit metadata", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
             
            writeToLog("INFO","Step 1: Going to create new category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName) == False:
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
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED create new channel: " + self.channelName)
                return

            writeToLog("INFO","Step 5: Going navigate to edit channel page")
            if self.common.channel.navigateToEditChannelPage(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to edit channel page")
                return
              
            writeToLog("INFO","Step 6: Going to edit channel matedata")
            if self.common.channel.editChannelMatedate(self.newChannelName, self.newDescription, self.newTags,  enums.ChannelPrivacyType.PRIVATE, [self.categoryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to edit channel matedata")
                return
              
            writeToLog("INFO","Step 7: Going navigate to channel page")
            if self.common.channel.navigateToChannelPageFromEditChannelPage(self.newChannelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to channel page: " + self.channelName)
                return
              
            writeToLog("INFO","Step 8: Going to verify channel details")
            if self.common.channel.varifyChannelyMatedate(self.newChannelName, self.newDescription, self.newTags, enums.ChannelPrivacyType.PRIVATE, appearsInCategoryName=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify channel details")
                return    
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Channel page - Edit metadata'  was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            if self.common.channel.deleteChannel(self.newChannelName) == False:
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