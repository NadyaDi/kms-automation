import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test description:
    # Main user add different user as a collaboration user on an entry.
    # The collaboration permission is co publish
    # The entry is published to category so the collaborator user can see the entry
    # Login with the collaborator user - go to entry page and try to delete the entry. collaborator user doesn't have permission to delete entry
    # Go to collaborator tab and add user as collaborator.collaborator user doesn't have permission to add collaborator user
    #================================================================================================================================
    testNum     = "3282"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    newUserId = "Automation_User_1"
    newUserId2 = "Automation_User_2"
    newUserPass = "Kaltura1!"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    categoryList = [("Apps Automation Category")]
    channelList = ""
    categoryName = None
    whereToPublishFrom = "Entry Page"
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Collaboration negative test", self.testNum)
            
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
               
            writeToLog("INFO","Step 7: Going to try and delete entry with added as Collaborator user")
            if self.common.entryPage.deleteEntryFromEntryPage(self.entryName, enums.Location.CATEGORY_PAGE, self.categoryList[0]) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED, the collaborator user succeed to delete entry although he don't have permission for it")
                return
            writeToLog("INFO","Step 7: Previous Step Failed as Expected - the collaborator user don't have permission to delete the entry")
            
            self.driver.refresh()
            sleep(3)
        
            writeToLog("INFO","Step 8: Going navigate to edit entry page from category page")
            if self.common.category.navigateToEditEntryPageFromCategoryPage(self.entryName, self.categoryList[0]) == False: 
                writeToLog("INFO","Step 8: FAILED to navigate to edit entry page")
                self.status = "Fail"
                return False 
            
            writeToLog("INFO","Step 9: Going to try to add user as collaborator with added as Collaborator user")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.newUserId2, True, False) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED, the collaborator user succeed to add user as a collaborator although he don't have permission for it")
                return      
            writeToLog("INFO","Step 9: Previous Step Failed as Expected - the collaborator user don't have permission to add collaborator user")     

            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Entry Collaboration co edit' was done successfully")
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