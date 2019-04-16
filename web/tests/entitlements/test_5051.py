import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Entitlements - Private Category
    # Test description:
    # 1. Verify that an entry can be published inside a Private Access Category
    # 2. Verify that Contributor Members are able to navigate to the category, entry published inside the category and add content to the category
    # 3. Verify that Category Members are able to access the category and navigate to the entry, but unable to add content
    # 4. Verify that KMS Users and Anonymous users are unable to access the Private Category
    #================================================================================================================================
    testNum = "5051"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    typeTest             = "Private Category with KMS User, Anonymous User, Contributor Member and Category Member"
    categoryName         = "Private Category"
    anonymousUser        = "Anonymous User"
    categoryMember       = "python_member"
    contributorMember    = "python_contributor"
    normalMember         = "python_normal"
    userPass             = "Kaltura1!"
    
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'    
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
            # Variables used in order to proper create the Entry
            self.entryName             = clsTestService.addGuidToString("Entitlements - Private Category", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
            
            writeToLog("INFO","Step 2: Going to publish the " + self.entryName + " to the " + self.categoryName)
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryName, '') == False:
                writeToLog("INFO","Step 2: FAILED to publish the " + self.entryName + " to the " + self.categoryName)
                return
            
            writeToLog("INFO","Step 3: Going to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " and authenticate with KMS User" + self.normalMember)
            if self.common.login.logOutThenLogInToKMS(self.normalMember, self.userPass)  == False:
                writeToLog("INFO","Step 3: FAILED to log out from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " and authenticate with KMS User " + self.normalMember)
                return
     
            writeToLog("INFO","Step 4: Going to verify that the " + self.categoryName + " can not be accessed by KMS User " + self.normalMember)
            if self.common.category.navigateToCategory(self.categoryName) != False:
                writeToLog("INFO","Step 4: FAILED, the " + self.categoryName + " was able to be accessed by KMS User " + self.normalMember + " although it shouldn't be available")
                return
            
            writeToLog("INFO","Step 5: Going to log out from " + self.normalMember + " and authenticate with Category Member " + self.categoryMember)
            if self.common.login.logOutThenLogInToKMS(self.categoryMember, self.userPass)  == False:
                writeToLog("INFO","Step 5: FAILED to log out from " + self.normalMember + " and authenticate with Category Member " + self.categoryMember)
                return
            
            writeToLog("INFO","Step 6: Going to verify that the " + self.categoryName + " can be accessed by Category Member " + self.categoryMember)
            if self.common.category.navigateToCategory(self.categoryName) == False:
                writeToLog("INFO","Step 6: FAILED, the " + self.categoryName + " couldn't be accessed by Category Member " + self.categoryMember)
                return
            
            writeToLog("INFO","Step 7: Going to verify that the " + self.entryName + " can be found by Category Member " + self.categoryMember + " inside the " + self.categoryName)
            if self.common.category.searchEntryInCategory(self.entryName) == False:
                writeToLog("INFO","Step 7: FAILED, the " + self.entryName + " couldn't be found by Category Member " + self.categoryMember + " inside the " + self.categoryName)
                return
            
            writeToLog("INFO","Step 8: Going to verify that the Category Member " + self.categoryMember + " its unable to add content to " + self.categoryName)
            if self.common.category.navigateToAddToCategory(self.categoryName) != False:
                writeToLog("INFO","Step 8: FAILED the Category Member " + self.categoryMember + " was able to add content to " + self.categoryName + " while it shouldn't have the permission")
                return
            
            writeToLog("INFO","Step 9: Going to log out from " + self.categoryMember + " and authenticate with Contributor Member " + self.contributorMember)
            if self.common.login.logOutThenLogInToKMS(self.contributorMember, self.userPass)  == False:
                writeToLog("INFO","Step 9: FAILED to log out from " + self.categoryMember + " and authenticate with Contributor Member " + self.contributorMember)
                return
            
            writeToLog("INFO","Step 10: Going to verify that the " + self.categoryName + " can be accessed by Contributor Member " + self.contributorMember)
            if self.common.category.navigateToCategory(self.categoryName) == False:
                writeToLog("INFO","Step 10: FAILED, the " + self.categoryName + " couldn't be accessed by Contributor Member " + self.contributorMember)
                return
            
            writeToLog("INFO","Step 11: Going to verify that the " + self.entryName + " can be found by Contributor Member " + self.contributorMember + " inside the " + self.categoryName)
            if self.common.category.searchEntryInCategory(self.entryName) == False:
                writeToLog("INFO","Step 11: FAILED, the " + self.entryName + " couldn't be found by Contributor Member " + self.contributorMember + " inside the " + self.categoryName)
                return
            
            writeToLog("INFO","Step 12: Going to verify that the Contributor Member " + self.contributorMember + " its able to add content to " + self.categoryName)
            if self.common.category.navigateToAddToCategory(self.categoryName) == False:
                writeToLog("INFO","Step 12: FAILED the Contributor Member " + self.contributorMember + " its unable to add content to " + self.categoryName)
                return
            
            writeToLog("INFO","Step 13: Going to log out from " + self.contributorMember + " and remain as " + self.anonymousUser)
            if self.common.login.logOutOfKMS()  == False:
                writeToLog("INFO","Step 13: FAILED to log out from " + self.contributorMember + " and remain as " + self.anonymousUser)
                return
            
            writeToLog("INFO","Step 14: Going to verify that the " + self.categoryName + " can not be accessed by" + self.anonymousUser)
            if self.common.category.navigateToCategory(self.categoryName) != False:
                writeToLog("INFO","Step 14: FAILED, the " + self.categoryName + " was able to be accessed by " + self.anonymousUser + " although it shouldn't be available")
                return          
            ##################################################################
            self.status="Pass"
            writeToLog("INFO","TEST PASSED: KMS has been successfully verified for a " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')