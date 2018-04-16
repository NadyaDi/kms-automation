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
    # Test description:
    # Check that entry that viewed in embed link is displayed in My History
    # The test's Flow: 
    # Login to KMS with user1-> Upload entry -> Publish entry to public channel -> Go to My history and check that entry isn't displayed -> Go to entry page and play entry -> Go to
    # MY History page and make sure that entry displayed in page -> Go to edit entry page -> Create secured embed link -> open link with user 2 -> play entry -> verify entry displayed in user2 My History page
    # Go to entry page and continue play entry (not to the end) -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2673"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    channelMemberUserId = 'private'
    channelMemberPass = '123456'
    channelList = ['publicChannelMyHistory']
    embedLink = None
    watchedAt = 'embed'
    embedLinkFilePath = 'C:\\xampp\\htdocs\\EmbedTest2673.html'
    embedUrl = 'http://localhost:8080/EmbedTest2673.html'
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryEmbed', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user - Channel admin")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
              
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return
               
            writeToLog("INFO","Step 3: Going to publish entry to public channel")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], self.channelList, publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False: 
                self.status = "Fail"        
                writeToLog("INFO","Step 2: FAILED failed to publish entry")
                return       
              
            writeToLog("INFO","Step 4: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to entry page")
                return           
              
            writeToLog("INFO","Step 5: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED - New entry is still processing")
                return
               
            writeToLog("INFO","Step 6: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 6: Previous Step Failed as Expected - The entry should not be displayed")
              
            writeToLog("INFO","Step 7: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate and play entry")
                return  
              
            writeToLog("INFO","Step 8: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to switch to default content")
                return  
              
            writeToLog("INFO","Step 9: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED find entry in my history")
                return  
              
            writeToLog("INFO","Step 10: Going to navigate to entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.MY_HISTORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to navigate to entry page")
                return 
              
            writeToLog("INFO","Step 11: Going to get embed link")
            self.embedLink = self.common.entryPage.getEmbedLink()
            if self.embedLink == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to get embed link")
                return  
             
            writeToLog("INFO","Step 12: Going to write embed code in file")
            self.common.writeToFile(self.embedLinkFilePath, self.embedLink)
             
            writeToLog("INFO","Step 13: Going to logout as user 1")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to logout from KMS")
                return        
              
            writeToLog("INFO","Step 14: Going to perform login to KMS site as user 2")
            if self.common.login.loginToKMS(self.channelMemberUserId, self.channelMemberPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to login as user 2")
                return  
             
            writeToLog("INFO","Step 15: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to navigate to to embed entry page")
                return   
            
            writeToLog("INFO","Step 16: Going to play entry")
            if self.common.player.clickPlayAndPause('0:05', True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to play entry")
                return   
            
            writeToLog("INFO","Step 17: Going to navigate to My History page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_HISTORY_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to navigate to My History page")
                return 
            
            writeToLog("INFO","Step 18: Going to search entry in My History")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED find entry in my history")
                return   
            
            writeToLog("INFO","Step 19: Going to check that entry details displayed correctly")
            if self.common.myHistory.checkEntryDetailsInMyHistory(self.entryName, self.entryDescription, self.entryTags, self.watchedAt) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED find entry in my history")
                return              
            
            writeToLog("INFO","Step 20: Going to logout as user 2")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to logout from KMS")
                return        
              
            writeToLog("INFO","Step 21: Going to perform login to KMS as user 1")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to login as user 1")
                return                                                                              
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')