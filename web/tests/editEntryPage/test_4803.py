import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name : Edit entry page - Change clipping permission
    # Test description:
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Publish entry to 'unlisted' > Click on 'Actions'-->'Edit' -> Go to 'Options' tab -> 
    # -> Check 'enable everyone to create clip'-> Click 'Save' -> Login with different user -> Navigate to entry page -> 
    # Click 'Actions' - 'Create clip' -> Create clip in KEA
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "4803"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.videoEntryName = clsTestService.addGuidToString("Enable clipping permission", self.testNum)
            expectedEntryDuration = "0:20"
            self.user2 = 'private'
            self.user2Pass = '123456'            
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('Add Captions', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry - to be trimmed")  
            if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
               
            writeToLog("INFO","Step 2: Going to publish entry to unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate('', '', '', enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 2: FAILED failed to publish entry to unlisted")
                return          
                
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
                
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
                
            writeToLog("INFO","Step 5: Going to get entry page URL")
            self.entryPageURL = self.common.base.driver.current_url  
               
            writeToLog("INFO","Step 6: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.videoEntryName) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to edit entry page")
                return     
               
            writeToLog("INFO","Step 7: Going to click on option tab and enable clip permission to everyone")
            if self.common.editEntryPage.changeEntryOptions(False, False, True) == False:
                writeToLog("INFO","Step 7: FAILED to click on option tab and enable clip permission to everyone")
                return  
              
            writeToLog("INFO","Step 8: Going to logout as admin")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 8: FAILED to logout from KMS")
                return        
              
            writeToLog("INFO","Step 9: Going to perform login to KMS as user 2")
            if self.common.login.loginToKMS(self.user2, self.user2Pass) == False:
                writeToLog("INFO","Step 9: FAILED to login as user 2")
                return  
              
            writeToLog("INFO","Step 10: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 10: FAILED to navigate to entry page link")
                return  
             
            writeToLog("INFO","Step 11: Going to clip the entry from 30sec to 20sec")  
            if self.common.kea.clipEntry(self.videoEntryName, "00:10", "00:20", expectedEntryDuration, enums.Location.ENTRY_PAGE, enums.Location.MY_MEDIA, isCreateClippingPermissionIsOn=True) == False:
                writeToLog("INFO","Step 11: FAILED to clip the entry from 30sec to 20sec")
                return    
             
            writeToLog("INFO","Step 12: Going to collect the new entry's QR codes")  
            self.QRlist = self.common.player.collectQrTimestampsFromPlayer("Clip of " + self.videoEntryName)
            if  self.QRlist == False:
                writeToLog("INFO","Step 12: FAILED to collect the new entry's QR codes")
                return
             
            self.isExist = ["5", "7", "22", "28"];
            self.isAbsent = ["12", "13", "15", "17"];
            writeToLog("INFO","Step 13: Going to verify the entry duration (using QR codes)")  
            if self.common.player.compareLists(self.QRlist, self.isExist, self.isAbsent, enums.PlayerObjects.QR) == False:
                writeToLog("INFO","Step 13: FAILED to verify the entry duration (using QR codes)")
                return   
            
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 14: Going to logout as user 2")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 14: FAILED to logout from KMS")
                return                            
             
            writeToLog("INFO","Step 15: Going to perform login to KMS site as user - admin")
            if self.common.loginAsUser() == False:
                writeToLog("INFO","Step 15: FAILED to login as user - admin")
                return   
            
            writeToLog("INFO","Step 16: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.videoEntryName) == False:
                writeToLog("INFO","Step 16: FAILED to navigate to edit entry page")
                return     
              
            writeToLog("INFO","Step 17: Going to click on option tab and disabled clip permission to everyone")
            if self.common.editEntryPage.changeEntryOptions(False, False, False) == False:
                writeToLog("INFO","Step 17: FAILED to click on option tab and disabled clip permission to everyone")
                return  
             
            writeToLog("INFO","Step 18: Going to logout as admin")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 18: FAILED to logout from KMS")
                return        
             
            writeToLog("INFO","Step 19: Going to perform login to KMS as user 2")
            if self.common.login.loginToKMS(self.user2, self.user2Pass) == False:
                writeToLog("INFO","Step 19: FAILED to login as user 2")
                return  
             
            writeToLog("INFO","Step 20: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 20: FAILED to navigate to entry page link")
                return   
            
            writeToLog("INFO","Step 21: Going to verify that create clip option isn't available")
            if self.common.entryPage.chooseCreateClipOption() == True:
                writeToLog("INFO","Step 21: FAILED to verify that create clip option isn't available")
                return                                                            
            writeToLog("INFO","Step 21: step above failed as expected")                                         
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Enable clipping permission was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia("Clip of " +self.videoEntryName)
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.videoEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')