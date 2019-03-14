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
    # @Author: Michal Zomper
    # Test Name: Categories - Members tab
    # Test description:
    # Add members to channel
    # The test's Flow: 
    # Login to KMS -> Create channel -> Click on 'Actions' --> 'Edit' -> Go to 'Members' tab -> Add new member to the channel -> Edit the member's permission
    # -> Delete member -> Set as owner
    #================================================================================================================================
    testNum = "712"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    categoryName = None
    description = "description"
    tags = "tags,"  
    userName = "Automation_User_1"

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
            self.categoryName = clsTestService.addGuidToString('Categories - Members tab', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ######################   
            
            writeToLog("INFO","Step 1: Going to create open category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description) == False:
                writeToLog("INFO","Step 1: FAILED to create open category")
                return
             
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 4: Going to add member to category")
            if self.common.category.addMemberToCategory(self.categoryName, self.userName, permission=enums.CategoryMemberPermission.MEMBER) == False:
                writeToLog("INFO","Step 4: FAILED to add member to category")
                return  
             
            writeToLog("INFO","Step 5: Going to change member permission")
            if self.common.category.editCategoryMemberPermission(self.userName, permission = enums.ChannelMemberPermission.MODERATOR) == False:
                writeToLog("INFO","Step 5: FAILED change member permission")
                return  
             
            writeToLog("INFO","Step 6: Going to delete member")
            if self.common.channel.deleteChannelMember(self.userName) == False:
                writeToLog("INFO","Step 6: FAILED to delete member")
                return     
            
            writeToLog("INFO","Step 7: Going to add member to category")
            if self.common.category.addMemberToCategory(self.categoryName, self.userName, permission=enums.CategoryMemberPermission.MEMBER) == False:
                writeToLog("INFO","Step 7: FAILED to add member to category")
                return   
             
            writeToLog("INFO","Step 8: Going to set member as owner")
            if self.common.channel.setChannelMemberAsOwner(self.userName) == False:
                writeToLog("INFO","Step 8: FAILED to set member as owner")
                return      
            sleep(3)                                             
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Categories - Members tab' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')