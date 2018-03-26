from enum import *
import time, pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # TBD
    # @Author: Inbar Willman
    # Test description:
    # Entry that is published to channel and was played by member in channel, should be displayed in My History after channel's admin change entry privacy
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Publish entry to channel -> Go to My history and check that entry isn't displayed -> Go to entry page and play entry -> Go to
    # MY History page and make sure that entry exists in page -> Login with user that is member in channel -> Play entry  -> Check that entry displayed in MY History -> Login with channel's admin -> Change entry privacy
    # Login with channel member -> check that entry still displayed in My History
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2648"
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
    channelList = ['PrivateChannelMyHistory']
    entryPageURL = None
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
            self,capture,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistory', self.testNum)
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
              
            writeToLog("INFO","Step 3: Going to publish entry to unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate('', '', '', enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 3: FAILED failed to publish entry to unlisted")
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
             
            writeToLog("INFO","Step 6: Going to get entry page URL")
            self.entryPageURL = self.common.base.driver.current_url
              
            writeToLog("INFO","Step 7: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 6: Previous Step Failed as Expected - The entry should not be displayed")
             
            writeToLog("INFO","Step 8: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate and play entry")
                return  
             
            writeToLog("INFO","Step 9: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to switch to default content")
                return  
             
            writeToLog("INFO","Step 10: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED find entry in my history")
                return    
             
            writeToLog("INFO","Step 11: Going to logout as admin channel")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to logout from KMS")
                return        
             
            writeToLog("INFO","Step 12: Going to perform login to KMS site as user - Channel member")
            if self.common.login.loginToKMS(self.channelMemberUserId, self.channelMemberPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to login as user - Channel member")
                return  
             
            writeToLog("INFO","Step 13: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to navigate to entry page link")
                return
             
            writeToLog("INFO","Step 14: Going to play entry as channel member")
            if self.common.player.clickPlayAndPause('0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to navigate and play entry")
                return  
             
            writeToLog("INFO","Step 15: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to switch to default content")
                return  
             
            writeToLog("INFO","Step 16: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED find entry in my history")
                return   
             
            writeToLog("INFO","Step 17: Going to logout as member channel")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to logout from KMS")
                return                            
             
            writeToLog("INFO","Step 18: Going to perform login to KMS site as user - admin member")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to login as user")
                return              

            writeToLog("INFO","Step 19: Going to changed played entry privacy to unlisted")
            if self.common.myMedia.publishSingleEntry(self.entryName, [], self.channelList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to changed entry privacy")
                return   
            
            writeToLog("INFO","Step 20: Going to logout as admin channel")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to logout from KMS")
                return                            
            
            writeToLog("INFO","Step 21: Going to perform login to KMS site as user - channel member")
            if self.common.login.loginToKMS(self.channelMemberUserId, self.channelMemberPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to login as user - channel member")
                return   
            
            writeToLog("INFO","Step 22: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED find entry in my history")
                return  
            
            writeToLog("INFO","Step 23: Going to logout as member channel")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to logout from KMS")
                return                            
             
            writeToLog("INFO","Step 24: Going to perform login to KMS site as user - admin member")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to login as user")
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