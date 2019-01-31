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
    # Add comments to entry
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Add comments -> Add replay to the comment -> publish entry
    # -> Login with user with permission to see the entry -> GO to the same entry page -> Add new comment -> Replay to existing comment
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "697"
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
    comment1User1 = 'comment 1'
    commentReply1User1 = 'Comment 1 replay 1'
    comment2User2 = 'Second comment'
    commenReply2User2 = 'Comment 1 replay 2'
    channelList = ['Add comments']
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
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
            ########################################################################
            self.entryName = clsTestService.addGuidToString('replyComments', self.testNum)
            self.channelMemberUserId = localSettings.LOCAL_SETTINGS_ADMIN_USERNAME
            self.channelMemberPass = localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD
            self.user1 = localSettings.LOCAL_SETTINGS_LOGIN_USERNAME
            self.user1Pass = localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD
            ########################## TEST STEPS - MAIN FLOW ####################### 
            
            writeToLog("INFO","Step 1: Going to create new channel")            
            if self.common.channel.createChannel(self.channelList[0], self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED create new channel: " + self.channelList[0])
                return
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return          
                
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
                
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
                         
            writeToLog("INFO","Step 5: Going to add new comment to entry as user 1")
            if self.common.entryPage.addComment(self.comment1User1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add new comment as user 1")
                return  
              
            writeToLog("INFO","Step 6: Going to replay the added comment")
            if self.common.entryPage.replyComment(self.commentReply1User1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to replay the added comment")
                return    
            
            writeToLog("INFO","Step 7: Going to publish entry")
            if self.common.myMedia.publishSingleEntry(self.entryName, '', self.channelList, publishFrom = enums.Location.ENTRY_PAGE)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entry")
                return  
            
            writeToLog("INFO","Step 8: Going to get entry page url")
            self.entryPageURL = self.common.base.driver.current_url
 
            
            writeToLog("INFO","Step 9: Going to logout as user 1")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to logout from KMS")
                return        
              
            writeToLog("INFO","Step 10: Going to perform login to KMS site as user 2")
            if self.common.login.loginToKMS(self.channelMemberUserId, self.channelMemberPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to login as user 2")
                return   
            
            writeToLog("INFO","Step 11: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to navigate to entry page link")
                return     
            
            writeToLog("INFO","Step 12: Going to reply user 1 comment")
            if self.common.entryPage.replyComment(self.commenReply2User2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to replay user 1 comment")
                return    
            
            writeToLog("INFO","Step 13: Going to add new comment to entry as user 2")
            if  self.common.entryPage.addComment(self.comment2User2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to add new comment as user 2")
                return  
            
            writeToLog("INFO","Step 14: Going to logout as user 2")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to logout from KMS")
                return        
              
            writeToLog("INFO","Step 15: Going to perform login to KMS site as user 1 in order to delete entry")
            if self.common.login.loginToKMS(self.user1, self.user1Pass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to login as user 1")
                return                                                                                                                                                                 
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelList[0])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')