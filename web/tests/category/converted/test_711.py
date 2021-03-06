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
    # Test Name : Categories - Edit metadata
    # Test description:
    # create new category
    # Enter category as the category manager Click on 'Actions' --> 'Edit'
    # Change the category's name / description / tags - The information saved and changed successfully
    #================================================================================================================================
    testNum = "711"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description"
    NewDescription = "New Description"
    tags = "Tags,"
    NewTags = "New Tags,"
    categoryName = None
    newCategoryName = None

    
    
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
            self.categoryName = clsTestService.addGuidToString("Categories - Edit metadata", self.testNum)
            self.newCategoryName = clsTestService.addGuidToString("New Category Name", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create new category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 1: FAILED to create category")
                return
            
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return

            writeToLog("INFO","Step 4: Going  navigate to edit category page")
            if self.common.category.navigateToEditCategoryPage(self.categoryName) == False:
                writeToLog("INFO","Step 4: FAILED navigate to category edit page")
                return
            
            writeToLog("INFO","Step 5: Going to edit category metadata")
            if self.common.category.editCategoryMatedate(self.newCategoryName, self.NewDescription, self.NewTags) == False:
                writeToLog("INFO","Step 5: FAILED to change category metadata")
                return
            
            writeToLog("INFO","Step 6: Going navigate to category page")
            if self.common.category.navigateToCategoryPageFronEditCategoryPage(self.newCategoryName) == False:
                writeToLog("INFO","Step 6: FAILED navigate to category page")
                return
                
            writeToLog("INFO","Step 7: Going to verify metadata change in category page")
            if self.common.category.varifyCategoryMatedate(self.newCategoryName, self.NewDescription, self.NewTags) == False:
                writeToLog("INFO","Step 7: FAILED to change category metadata")
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Categories - Edit metadata' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.apiClientSession.deleteCategory(self.newCategoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')