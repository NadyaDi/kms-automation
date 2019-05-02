import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
from KalturaClient.Plugins.Core import KalturaPrivacyType, KalturaContributionPolicyType, KalturaAppearInListType
import enums
from upload import UploadEntry


class Test:
    
    #================================================================================================================================
    #  @Author: Ori Flchtman
    # Test Name : Create New Groups on Admin Manage Groups
    # Test description:
    # Create users
    # Create Groups
    # Add Users to Groups
    #================================================================================================================================
    testNum = "5158"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    userName1 = "user_admin_5"
    firstName1= "user admin"
    lastName1 = "5"
    userPass1 = "123456"
    groupName1= "Group #5"
    groupId1= "Group_#5"

    
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
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to Add Users") 
            if self.common.admin.addUsers(self.userName1, self.firstName1, self.lastName1, self.userPass1, enums.UserRoles.PRIVATE_ONLY_ROLE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add user")
                return
            
            writeToLog("INFO","Step 2: Going to Add Group with User") 
            if self.common.admin.addGroups(self.groupName1, self.groupId1, self.userName1, enums.AdminTabs.MANAGE_GROUPS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add Group with User")
                return            
              
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Add User' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")        
            self.common.admin.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4], showAllEntries=True)       
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')