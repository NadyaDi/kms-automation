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
    #  @Author: Michal Zomper
    # Test Name : Categories Type (Open / Restricted / Private)
    # Test description:
    # Create 3 categories : Open / Restricted / Private
    # For open category : Membership is open ans non-members can view content and participate.
    #                     Everyone can view and add content
    # For restricted category : Non-members can view content, but users must be invited to participate.
    #                           Everyone can view content, but only members (contributors and above) can add content.
    # For private category: Membership is by invitation only and only members can view content and participate.
    #                       Only members can view and add content.
    #                       Non-members cannot see and search for the category.
    #================================================================================================================================
    testNum = "716"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    description = "Description"
    tags = "Tags,"
    openCategoryName = None
    restrictedCategoryName = None
    privateCategoryName = None
    filePath= localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    userName = "Automation_User_1"
    userPass = "Kaltura1!"

    
    
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
            self.openCategoryName = clsTestService.addGuidToString("Categories Type - Open Category", self.testNum)
            self.restrictedCategoryName = clsTestService.addGuidToString("Categories Type - Restricted Category", self.testNum)
            self.privateCategoryName = clsTestService.addGuidToString("Categories Type - Private Category", self.testNum)
            self.entryName1 = clsTestService.addGuidToString("Categories Type - Open Category", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Categories Type - Restricted Category", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Categories Type - Private Category", self.testNum)
            self.entry1 = UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
            self.entry2 = UploadEntry(self.filePath, self.entryName2, self.description, self.tags, timeout=60, retries=3)
            self.entry3 = UploadEntry(self.filePath, self.entryName3, self.description, self.tags, timeout=60, retries=3)            
            uploadEntrieList = [self.entry1, self.entry2, self.entry3]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create open category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.openCategoryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create open category")
                return
             
            writeToLog("INFO","Step 2: Going to create restricted category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.restrictedCategoryName, self.description, self.tags, privacy=KalturaPrivacyType.AUTHENTICATED_USERS, addContentToCategory=KalturaContributionPolicyType.MEMBERS_WITH_CONTRIBUTION_PERMISSION) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create open category")
                return
             
            writeToLog("INFO","Step 3: Going to create private category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.privateCategoryName, self.description, self.tags, privacy=KalturaPrivacyType.MEMBERS_ONLY, addContentToCategory=KalturaContributionPolicyType.ALL, whoCanSeeTheCategory=KalturaAppearInListType.CATEGORY_MEMBERS_ONLY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create private category")
                return
            
            writeToLog("INFO","Step 4: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 5: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to home page")
                return
            
            sleep(2)
            writeToLog("INFO","Step 6: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to logout from main user")
                return  
                              
            writeToLog("INFO","Step 7: Going to login with user " + self.userName)
            if self.common.login.loginToKMS(self.userName, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to login with " + self.userName)
                return       
             
            writeToLog("INFO","Step 8: Going to add content to open category with non member user")
            if self.common.category.addNewContentToCategory(self.openCategoryName, uploadEntrieList[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to add media to open category")
                return
                          
            writeToLog("INFO","Step 9: Going to verify entry found in category")
            if self.common.category.searchEntryInCategory(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to find entry '" + self.entryName1 + "' in category: " + self.openCategoryName)
                return
             
            writeToLog("INFO","Step 10: Going to add content to restricted category with non member user")
            if self.common.category.addNewContentToCategory(self.restrictedCategoryName, uploadEntrieList[1]) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED, user is non member in restricted category and should NOT have permission to add content")
                return
            writeToLog("INFO","Step 10: preview step failed as expected: user is non member in restricted category and should NOT have permission to add content")
             
            writeToLog("INFO","Step 11: Going to add content to private category with non member user")
            if self.common.category.addNewContentToCategory(self.privateCategoryName, uploadEntrieList[2]) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED, user is non member in private category and should NOT have permission to add content")
                return
            writeToLog("INFO","Step 11: preview step failed as expected: user is non member in private category and can NOT enter to category")
             
            sleep(2)
            writeToLog("INFO","Step 12: Going to logout from '" + self.userName + "' user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to logout from '" + self.userName + "' user")
                return  
             
            writeToLog("INFO","Step 13: Going to login with main user")
            if self.common.loginAsUser()== False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to login with main user")
                return 
             
            writeToLog("INFO","Step 14: Going to add user as member in category: " + self.restrictedCategoryName)
            if self.common.category.addMembersToCategory(self.restrictedCategoryName, self.userName, permission=enums.CategoryMemberPermission.CONTRIBUTOR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to add user '"+ self.userName + "' as a member in category: " + self.restrictedCategoryName)
                return
            
            writeToLog("INFO","Step 15: Going to add user as member in category: " + self.privateCategoryName)
            if self.common.category.addMembersToCategory(self.privateCategoryName, self.userName, permission=enums.CategoryMemberPermission.CONTRIBUTOR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to add user '"+ self.userName + "' as a member in category: " + self.privateCategoryName)
                return
            
            sleep(2)
            writeToLog("INFO","Step 16: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to logout from main user")
                return  
                              
            writeToLog("INFO","Step 17: Going to login with user " + self.userName)
            if self.common.login.loginToKMS(self.userName, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to login with " + self.userName)
                return       
             
            writeToLog("INFO","Step 18: Going to add content to restricted category with non member user")
            if self.common.category.addNewContentToCategory(self.restrictedCategoryName, uploadEntrieList[1]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED, user is a member in restricted category and should have permission to add content")
                return
             
            writeToLog("INFO","Step 19: Going to verify entry found in category")
            if self.common.category.searchEntryInCategory(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to find entry '" + self.entryName2 + "' in category: " + self.restrictedCategoryName)
                return
             
            writeToLog("INFO","Step 20: Going to add content to private category with non member user")
            if self.common.category.addNewContentToCategory(self.privateCategoryName, uploadEntrieList[2]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED, user is a member in private category and should have permission to add content")
                return
            
            writeToLog("INFO","Step 21: Going to verify entry found in category")
            if self.common.category.searchEntryInCategory(self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to find entry '" + self.entryName2 + "' in category: " + self.privateCategoryName)
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Categories Type' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")        
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName, self.userPass)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)          
            self.common.apiClientSession.deleteCategory(self.openCategoryName)
            self.common.apiClientSession.deleteCategory(self.restrictedCategoryName)
            self.common.apiClientSession.deleteCategory(self.privateCategoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')