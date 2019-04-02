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
    # Test Name : Collaboration - edit metadata
    # Test description:
    # Main user add different user as a collaboration user on an entry.
    # The collaboration permission is co edit
    # The entry is published to category so the collaborator user can see the entry
    # Login with the collaborator user and change the entry metadata (entry name / description / tags) successfully. 
    #================================================================================================================================
    testNum     = "3277"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    newEntryName = None
    channelList = None
    entryDescription = "Description"
    entryTags = "Tags,"
    newUserId = "AutomationUser7"
    newUserPass = "Kaltura1!"
    newDescription = "Edit description"
    newTags = "Edit Tags,"
    categoryList = [("Apps Automation Category")]
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Collaboration - edit metadata", self.testNum)
            self.newEntryName = clsTestService.addGuidToString('Edit Collaboration', self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
        
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                writeToLog("INFO","Step 1: FAILED to login as user")
                return         

            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 3: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to edit entry page")
                return
            
            writeToLog("INFO","Step 4: Going to add Collaborator in edit Entry Page")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.newUserId, True, False) == False:
                writeToLog("INFO","Step 4: FAILED failed to add user as a collaborator")
                return
            
            sleep(2)     
            writeToLog("INFO","Step 5: Going to publish the entry so the add user as a collaborator can see it")            
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "") == False:
                writeToLog("INFO","Step 5: FAILED to publish entry '" + self.entryName + "'")
                return
            
            writeToLog("INFO","Step 6: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 6: FAILED failed to logout from main user")
                return  
                              
            writeToLog("INFO","Step 7: Going to login with the user that was added as Collaborator")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                writeToLog("INFO","Step 7: FAILED to login with the user that was added as Collaborator")
                return
            
            writeToLog("INFO","Step 8: Going to navigate to entry page from category page with the user that was added as Collaborator")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName, self.categoryList[0]) == False:
                writeToLog("INFO","Step 8: FAILED to navigate to entry page with the user that was added as Collaborator")
                return                                  
            
            writeToLog("INFO","Step 9: Going to navigate to edit entry page from entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 9: FAILED to navigate to edit entry page from entry page")
                return 
             
            writeToLog("INFO","Step 10: Going to change entry metadata  (entry name, description, tags) with the user that  added as Collaborator")
            if self.common.editEntryPage.changeEntryMetadata(self.entryName, self.newEntryName, self.newDescription, self.newTags) == False:
                writeToLog("INFO","Step 10: FAILED to edit entry metadata with the user that was added as Collaborator")
                return  
            
            writeToLog("INFO","Step 11: Going to navigate to entry page from category page")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.newEntryName, self.categoryList[0]) == False:
                writeToLog("INFO","Step 11: FAILED to navigate to entry page with the user that was added as Collaborator")
                return                 
                
            writeToLog("INFO","Step 12: Going to verify entry new  metadata  (entry name, description, tags) with the user that  added as Collaborator")
            # We add the word 'tags' since we don't delete the tags that was insert when the entry was uploaded
            if self.common.entryPage.verifyEntryMetadata(self.newEntryName, self.newDescription, self.entryTags.lower()[:-1] + self.newTags.lower()[:-1]) == False:
                writeToLog("INFO","Step 12: FAILED to verify entry new  metadata with the user that was added as Collaborator")
                return  
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Test 'Entry Collaboration co editor - Details Tab' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                       
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.newEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')