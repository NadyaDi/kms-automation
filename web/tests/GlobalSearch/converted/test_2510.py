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
    # Test Name : Global Search for Category
    # Test description:
    # Create category new category  
    # In the header - global search enter the category name to the text box and click on search: 
    #     Search results page should be opened successfully.
    #     The title should be "Search for: "
    #     the searched word- 
    #     move to categories tab 
    #     search category should be display

    #================================================================================================================================
    testNum = "2510"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
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
            self.categoryName = clsTestService.addGuidToString("Categories - Global Search for Category", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 

            writeToLog("INFO","Step 1: Going to create new category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create category")
                return
            
            writeToLog("INFO","Step 2: Going to clear cache")
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache in admin page")
                return 
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 4: Going to search and verify category in global search")
            if self.common.globalSearch.serchAndVerifyCategoryInGlobalSearch(self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to search category'" + self.categoryName + "' in global search")
                return 
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Global search - Global Search for Category' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.apiClientSession.deleteCategory(self.categoryName)  
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')