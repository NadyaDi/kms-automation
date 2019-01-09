import time, pytest,sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Tzachi Guetta
    # Test Name : Channel page - Add New Media to channel 
    # Test description:
    # 1. Click on 'Add Media' --> Add New' 
    # Add the following media types:
    # 1 Media Upload - Audio, Video, Image
    #     
    #     Expected:
    # 1. All media types should be uploaded successfully.
    # 2. Metadata should be saved successfully
    # 3. Entry page should be opened successfully
    # 4. All the uploaded media should be displayed in the channel
    #================================================================================================================================
    testNum = "732"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None
    newUserId = None
    newUserPass = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3' 
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4' 
    
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
            self.entryName1 = clsTestService.addGuidToString('entryName1')
            self.entryName2 = clsTestService.addGuidToString('entryName2')
            self.entryName3 = clsTestService.addGuidToString('entryName3')
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as End-user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as End-user")
                return
              
            self.entriesToUpload = {
                self.entryName1: self.filePathImage, 
                self.entryName2: self.filePathAudio,
                self.entryName3: self.filePathVideo }            
              
            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
                 
            writeToLog("INFO","Step 7: Going to publish entries 1-3 to Moderated channel")
            if self.common.channel.addExistingContentToChannel("KMS-Automation_Moderate_Channel", [self.entryName1, self.entryName2, self.entryName3], isChannelModerate=False, publishFrom = enums.Location.MY_CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entries 1-3 to Moderated channel")
                return
                             
            writeToLog("INFO","Step 7: Going to ")
            if self.common.channel.searchEntriesInChannel([self.entryName1, self.entryName2, self.entryName3], enums.Location.CHANNELS_PAGE, "KMS-Automation_Moderate_Channel") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to ")
                return
               
            
            ##################################################################
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            if self.status == "Fail" : 
                self.common.login.logOutOfKMS()
                self.common.loginAsUser()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')