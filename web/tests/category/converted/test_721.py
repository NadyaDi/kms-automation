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
    # Test Name: Categories - Import Mermbers
    # Test description:
    # create 2 categories, 1 parent and 1 sub category 
    # Add member with different permissions to parent category  
    # Go so sub category member tab and click on the 'Import Members from Parent Category' button
    # All the parent category's members are added to the sub category according to their permissions there.
    # Edit the members' permissions and remove them / adding new members
    #================================================================================================================================
    testNum = "721"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    parentCategoryName = None
    subCategoryName = None
    description = "description"
    tags = "tags,"  
    userName1 = "Automation_User_1"
    userName2 = "Automation_User_2"
    userName3 = "Automation_User_3"

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
            self.parentCategoryName = clsTestService.addGuidToString('Category - Import Mermbers', self.testNum)
            self.subCategoryName = clsTestService.addGuidToString('Sub Category - Import Mermbers', self.testNum)
            self.membersList =[(self.userName1,enums.CategoryMemberPermission.MEMBER), 
                                (self.userName2,enums.CategoryMemberPermission.MODERATOR), 
                                (self.userName3,enums.CategoryMemberPermission.CONTRIBUTOR)]
            ########################## TEST STEPS - MAIN FLOW ######################   
            
            writeToLog("INFO","Step 1: Going to create parent category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.parentCategoryName, self.description) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create parent category")
                return
            
            writeToLog("INFO","Step 2: Going to create sub category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getCategoryByName(self.parentCategoryName)
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.subCategoryName, self.description) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create sub category")
                return
             
            writeToLog("INFO","Step 3: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 4: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 5: Going to add members to parent category")
            if self.common.category.addMembersToCategory(self.parentCategoryName, self.membersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add members to parent category")
                return  
            
            writeToLog("INFO","Step 6: Going navigate to sub category edit page")
            if self.common.category.navigateToEditSubCategoryPage(self.parentCategoryName, self.subCategoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to sub category edit page")
                return 
            
            writeToLog("INFO","Step 7: Going to import Members from parent category")
            if self.common.category.importMemberFormCategory() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to import Members from parent category")
                return 
             
            writeToLog("INFO","Step 8: Going navigate to sub category edit page")
            if self.common.category.navigateToEditSubCategoryPage(self.parentCategoryName, self.subCategoryName, forcrNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to sub category edit page")
                return 
             
            writeToLog("INFO","Step 9: Going to verify that import members form parent category display in sub category member tab after import")
            if self.common.category.verifyMembersPermissionsInMemberTable(self.membersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: to verify that add members form parent category display in sub category member tab after import")
                return 
             
            writeToLog("INFO","Step 10: Going to delete member")
            if self.common.channel.deleteChannelMember(self.userName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to delete member")
                return   
            sleep(3)
            
            writeToLog("INFO","Step 11: Going to add member to sub category")
            if self.common.category.addMemberToCategory(self.subCategoryName, self.userName2, permission=enums.CategoryMemberPermission.MEMBER, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to add member to sub category")
                return   
            sleep(3)
            
            writeToLog("INFO","Step 12: Going to change member permission")
            if self.common.category.editCategoryMemberPermission(self.userName1, permission = enums.CategoryMemberPermission.MODERATOR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED change member permission")
                return  
            sleep(3)
            
            writeToLog("INFO","Step 13: Going to set member as owner")
            if self.common.channel.setChannelMemberAsOwner(self.userName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to set member as owner")
                return      
            sleep(3)                                             
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Categories - Import Mermbers' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.apiClientSession.deleteCategory(self.subCategoryName)
            self.common.apiClientSession.deleteCategory(self.parentCategoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')