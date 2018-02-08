import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "346"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = None
    entryTags = None 
    newUserId = None
    newUserPass = None
    EnableComments = None
    CloseDiscussion = None
    EveryoneToCreateClip = None
    categoryList = None
    channelList = ""
    categoryName = None
    whereToPublishFrom = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    
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
            self,capture,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Collaboration entry Co Edit - Options tab")
            self.entryDescription = "Description"
            self.entryTags = "Tags,"
            self.newUserId = "Automation_User_1"
            self.newUserPass = "Kaltura1!"
            self.EnableComments = True
            self.CloseDiscussion = True
            self.EveryoneToCreateClip = True
            self.categoryList = [("Apps Automation Category")]
            self.whereToPublishFrom = "Entry Page"
            
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return         
 
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
                             
            writeToLog("INFO","Step 3: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to edit entry page")
                return False
            
            writeToLog("INFO","Step 4: Going to add Collaborator in edit Entry Page")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.newUserId, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to add user as a collaborator")
                return
            
            sleep(2)     
            writeToLog("INFO","Step 5: Going to publish the entry so the add user as a collaborator can see it")            
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry '" + self.entryName + "'")
                return
            
            writeToLog("INFO","Step 6: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED failed to logout from main user")
                return  
                              
            writeToLog("INFO","Step 7: Going to login with the user that was added as Collaborator")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to login with the user that was added as Collaborator")
                return
            
            writeToLog("INFO","Step 8: Going to navigate to entry page from category page with the user that was added as Collaborator")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.categoryList[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to entry page with the user that was added as Collaborator")
                return                                  
            
            writeToLog("INFO","Step 9: Going to navigate to edit entry page from entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to navigate to edit entry page from entry page")
                return 
            
            writeToLog("INFO","Step 10: Going to change entry options with the user that was added as Collaborator")
            if self.common.editEntryPage.changeEntryOptions(self.EnableComments, self.CloseDiscussion, self.EveryoneToCreateClip) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to change entry options with the user that was added as Collaborator")
                return 
            
            ##################################################################
            print("Test 'Entry Collaboration co editor - Options tab' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')