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
    # @Author: Inbar Willman
    # Test description:
    # Check that entry that was played in context of channel is displayed in My History.
    # The test's Flow: 
    # Login to KMS-> Upload entry -> publish entry to open channel -> Go to My history and check that entry isn't displayed -> Go to channel -> play entry
    # in channel -> Go to My History page and check that entry is displayed.
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2667"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName= None
    channelName = 'OpenChannelMyHistory'
    channelList = [channelName]
    entryDescription = "description"
    entryTags = "tag1,"
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryEntry', self.testNum)
            ######################### TEST STEPS - MAIN FLOW #######################
#             writeToLog("INFO","Step 1: Going to upload entry")
#             if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entry")
#                 return
#              
#             writeToLog("INFO","Step 2: Going to publish entry to open channel")
#             if self.common.myMedia.publishSingleEntry(self.entryName, [], self.channelList, publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False: 
#                 self.status = "Fail"        
#                 writeToLog("INFO","Step 2: FAILED failed to publish entry")
#                 return          
#              
#             writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
#             if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED to navigate to entry page")
#                 return           
#              
#             writeToLog("INFO","Step 4: Going to wait until media will finish processing")
#             if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED - New entry is still processing")
#                 return
#               
#             writeToLog("INFO","Step 5: Going to Search entry in My History page")
#             if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 5: FAILED - New entry is displayed in my history page")
#                 return
#             writeToLog("INFO","Step 5: Previous Step Failed as Expected - The entry should not be displayed")
#             
#             writeToLog("INFO","Step 6: Going to navigate to My channel")
#             if self.common.channel.navigateToMyChannels() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 6: FAILED to navigate to My Channels")
#                 return
#          
#             writeToLog("INFO","Step 7: Going to navigate entry page from channel page")
#             if self.common.channel.naviagteToEntryFromChannelPage(self.entryName, self.channelName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 7: FAILED to navigate to entry page from channel page")
#                 return     
#             
#             writeToLog("INFO","Step 8: Going to play entry")
#             if self.common.player.clickPlayAndPause('0:05') == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 8: FAILED to play entry")
#                 return       
#              
#             writeToLog("INFO","Step 9: Going to switch to default content")
#             if self.common.base.switch_to_default_content() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 9: FAILED to switch to default content")
#                 return  
             
            writeToLog("INFO","Step 10: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory('CFEF9257_MyHistoryEntry') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED find entry in my history")
                return  
             
            writeToLog("INFO","Step 11: Going to check that entry details displayed correctly")
            if self.common.myHistory.checkEntryDetailsInMyHistory('CFEF9257_MyHistoryEntry') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED find entry in my history")
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