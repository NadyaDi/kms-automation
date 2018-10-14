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
    # Test Name: Categories - Enable / Disable Inherit permissions
    # Test description:
    # create 2 categories, 1 parent and 1 sub category 
    # Add member with different permissions to parent category  
    #    1. Go so sub category member tab and click on 'Inherit permissions from parent category' -> Click on 'Yes' in the pop-up message
    #     All the parent category's members are added to the sub category according to their permissions there.
    #     You should Not be able to edit the member's permissions or to remove them or to add new members as long as the inherit option is checked.
    # 
    #    2.  Go so sub category member tab and UnCheck the option : 'Inherit permissions from parent category' - > Click on 'Yes' in the pop-up message
    #     The parent category's members should be removed from the category.
    #     The members list should be as it was before the inheriting.
    #================================================================================================================================
    testNum = "719"
    
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
    userName4 = "Automation_User_4"

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
            self.parentCategoryName = clsTestService.addGuidToString('Category - Inherit permissions', self.testNum)
            self.subCategoryName = clsTestService.addGuidToString('Sub Category - Inherit permissions', self.testNum)
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
            
            writeToLog("INFO","Step 7: Going to inherit permissions from parent category")
            if self.common.category.inheritPermissionsFormCategory() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to  inherit permissions from parent category")
                return 
            sleep(3)
            
            writeToLog("INFO","Step 8: Going navigate to sub category edit page")
            if self.common.category.navigateToEditSubCategoryPage(self.parentCategoryName, self.subCategoryName, forcrNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to sub category edit page")
                return 
             
            writeToLog("INFO","Step 9: Going to verify that inherit members form parent category display in sub category member tab after inherit")
            if self.common.category.verifyMembersPermissionsInMemberTable(self.membersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify that add members form parent category display in sub category member tab after inherit permissions")
                return 
             
            writeToLog("INFO","Step 10: Going to try to delete member")
            if self.common.channel.deleteChannelMember(self.userName2) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED, user delete member although after inherit members permissions user can NOT delete member")
                return   
            writeToLog("INFO","Step 10: preview step failed as expected: user can NOT delete members after inherit members permissions")
            sleep(3)
            
            writeToLog("INFO","Step 11: Going to try and add member to sub category")
            if self.common.category.addMemberToCategory(self.subCategoryName, self.userName2, permission=enums.CategoryMemberPermission.MEMBER, forceNavigate=False) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED, user added member to sub category although after inherit members permissions user can NOT add member ")
                return   
            writeToLog("INFO","Step 11: preview step failed as expected: user can NOT add members after inherit members permissions")
            sleep(3)
            
            writeToLog("INFO","Step 12: Going to try and change member permission")
            if self.common.category.editCategoryMemberPermission(self.userName1, permission = enums.CategoryMemberPermission.MODERATOR) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED, user change member permission although after inherit members permissions user can NOT change member permission")
                return  
            writeToLog("INFO","Step 12: preview step failed as expected: user can NOT change member permission after inherit members permissions")
            sleep(3)
            
            writeToLog("INFO","Step 13: Going to try and set member as owner")
            if self.common.channel.setChannelMemberAsOwner(self.userName3) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED, user set member as owner although after inherit members permissions user can NOT set member as owner")
                return   
            writeToLog("INFO","Step 13: preview step failed as expected: user can NOT set member as owner after inherit members permissions")   
            sleep(3)       
            
            writeToLog("INFO","Step 14: Going navigate to sub category edit page")
            if self.common.category.navigateToEditSubCategoryPage(self.parentCategoryName, self.subCategoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED navigate to sub category edit page")
                return 
            
            writeToLog("INFO","Step 15: Going to disable inherit permissions from parent category")
            if self.common.category.inheritPermissionsFormCategory() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to disable inherit permissions from parent category")
                return
            
            writeToLog("INFO","Step 16: Going navigate to sub category edit page")
            if self.common.category.navigateToEditSubCategoryPage(self.parentCategoryName, self.subCategoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED navigate to sub category edit page")
                return 
            
            writeToLog("INFO","Step 17: Going navigate to sub category member tab")
            if self.common.category.navigateToCategoryMembersTab() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED navigate to sub category member tab")
                return 
                       
            writeToLog("INFO","Step 18: Going to verify that inherit member '" + self.userName1 + "' form parent category erased from sub category member tab after disable inherit permissions")
            if self.common.category.verifyMemberPermissionsInMemberTable(self.userName1,enums.CategoryMemberPermission.MEMBER)== True:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED, member '" + self.userName1 + "' still display in sub category member tab after disable inherit permissions")
                return     
            writeToLog("INFO","Step 18: preview step failed as expected: user doesn't need to a member in sub category after disable inherit members permissions")
            
            writeToLog("INFO","Step 19: Going to verify that inherit member '" + self.userName2 + "' form parent category erased from sub category member tab after disable inherit permissions")
            if self.common.category.verifyMemberPermissionsInMemberTable(self.userName2,enums.CategoryMemberPermission.MODERATOR)== True:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED, member '" + self.userName2 + "' still display in sub category member tab after disable inherit permissions")
                return     
            writeToLog("INFO","Step 19: preview step failed as expected: user doesn't need to a member in sub category after disable inherit members permissions")
            
            writeToLog("INFO","Step 20: Going to verify that inherit member '" + self.userName3 + "' form parent category erased from sub category member tab after disable inherit permissions")
            if self.common.category.verifyMemberPermissionsInMemberTable(self.userName3,enums.CategoryMemberPermission.CONTRIBUTOR)== True:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED, member '" + self.userName3 + "' still display in sub category member tab after disable inherit permissions")
                return     
            writeToLog("INFO","Step 20: preview step failed as expected: user doesn't need to a member in sub category after disable inherit members permissions")                        
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Categories - Enable / Disable Inherit permissions' was done successfully")
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