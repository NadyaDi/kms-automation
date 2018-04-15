import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test description:
    # Main user add different user as a collaboration user on an entry.
    # The collaboration permission is co edit
    # The entry is published to category so the collaborator user can see the entry
    # Login with the collaborator user - go to entry caption tab and added caption to the entry successfully.
    #================================================================================================================================
    testNum     = "3280"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    categoryName = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    entryDescription = "Description"
    entryTags = "Tags,"
    newUserId = "Automation_User_1"
    newUserPass = "Kaltura1!"
    categoryList = [("Apps Automation Category")]
    channelList = ""
    whereToPublishFrom = "Entry Page"
    captionFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\xml\app-caption-entry-page.xml'
    captionLanguage = "English (American)"
    captionLabel = None
    
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
            self.entryName = clsTestService.addGuidToString("Collaboration Co Edit - Caption tab", self.testNum)
            self.captionLabel = clsTestService.addGuidToString("English", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 
   
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                   
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                self.status = "Fail"
                return
            
                                 
            writeToLog("INFO","Step 3: Going to add Collaborator in edit Entry Page")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.newUserId, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to add user as a collaborator")
                return
                
            sleep(2)     
            writeToLog("INFO","Step 4: Going to publish the entry so the add user as a collaborator can see it")            
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entry '" + self.entryName + "'")
                return
                
            writeToLog("INFO","Step 5: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to logout from main user")
                return  
                                  
            writeToLog("INFO","Step 6: Going to login with the user that was added as Collaborator")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to login with the user that was added as Collaborator")
                return
                
            writeToLog("INFO","Step 7: Going to navigate to entry page from category page with the user that was added as Collaborator")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.categoryList[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to entry page with the user that was added as Collaborator")
                return                                  
                
            writeToLog("INFO","Step 8: Going to navigate to edit entry page from entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to edit entry page from entry page")
                return 
              
            writeToLog("INFO","Step 0: Going to add caption with added as Collaborator user")
            if self.common.editEntryPage.addCaptions(self.captionFilePath, self.captionLanguage, self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to add caption to entry '" + self.entryName + "' with Collaborator user")
                return

            writeToLog("INFO","Step 10: Going to remove added caption with added as Collaborator user")
            if self.common.editEntryPage.removeCaption(self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to remove added caption to entry '" + self.entryName + "' with Collaborator user")
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Entry Collaboration co editor - Caption tab' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                        
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')