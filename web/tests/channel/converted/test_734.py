import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Channel - Entries details
    # Test description:
    # As the channel's owner:
    # Choose one of your entries in the channel and check that all the entry details (views, likes, comments) are correct 
    #================================================================================================================================
    testNum = "734"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelName = None
    comments = ["Comment 1", "Comment 2"]

    
    
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
            self.entryName = clsTestService.addGuidToString("Channel Entry Details", self.testNum)
            self.channelName = clsTestService.addGuidToString("Channel Entry Details", self.testNum)
            self.channelName= [(self.channelName)]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 

            writeToLog("INFO","Step 1: Going to enable like module")            
            if self.common.admin.enablelike(True) == False:
                writeToLog("INFO","Step 1: FAILED to enable like module")
                return
             
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
                         
            writeToLog("INFO","Step 3: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
               
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName[0], self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, False) == False:
                writeToLog("INFO","Step 4: FAILED create new channel")
                return
               
            writeToLog("INFO","Step 5: Going navigate to entry page")            
            if self.common.entryPage.navigateToEntry(self.entryName, enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 5: FAILED navigate to entry: " + self.entryName)
                return 
                
            writeToLog("INFO","Step 6: Going to like the entry page")            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                writeToLog("INFO","Step 6: FAILED to like entry: " + self.entryName)
                return   
               
            writeToLog("INFO","Step 7: Going to add comments to entry")  
            for i in range(2):
                if self.common.entryPage.addComment(self.comments[i]) == False:
                    writeToLog("INFO","Step 7: FAILED to add comment '" + self.comments[i] + "' to entry: " + self.entryName)
                    return
                 
            writeToLog("INFO","Step 8: Going to publish entry to channel")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", self.channelName, publishFrom = enums.Location.ENTRY_PAGE, disclaimer=False) == False:
                writeToLog("INFO","Step 8: FAILED publish entry '" + self.entryName + "' to channel: " + self.channelName[0])
                return
              
            writeToLog("INFO","Step 9: Going navigate to my channels page")  
            if self.common.channel.navigateToChannel(self.channelName[0], navigateFrom=enums.Location.MY_CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 9: FAILED navigate to channel: " + self.channelName[0])
                return
             
            writeToLog("INFO","Step 10: Going to verify entry details in channel")
            if self.common.category.verifyEntryDetails(self.entryName, "1", "0", str(len(self.comments))) == False:
                writeToLog("INFO","Step 10: FAILED to verify entry details in channel page")
                return
             
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Channel Entry Details' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName[0])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')