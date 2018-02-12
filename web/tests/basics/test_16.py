from time import strftime

import pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test description:
    # 
    #================================================================================================================================
    testNum     = "16"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    flavorsList = ["Source", "Mobile (3GP)", "Basic/Small - WEB/MBL (H264/400)","Basic/Small - WEB/MBL (H264/600)", "SD/Small - WEB/MBL (H264/900)", "SD/Large - WEB/MBL (H264/1500)","HD/720 - WEB (H264/2500)","HD/1080 - WEB (H264/4000)","WebM"] 
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,captur,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName = clsTestService.addGuidToString('entryName')
            self.filePathDownloaded = localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS + self.entryName + "_" + '(' + self.flavorsList[0] + ')'  + ".mp4"
#           TO-DO: move the below line to "crate evn test"
#           self.common.admin.adminDownloadMedia(True)
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return             
             
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
              
            writeToLog("INFO","Step 3: Going to add flavors to the entry")
            if self.common.editEntryPage.addFlavorsToEntry(self.entryName, [self.flavorsList[0]]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED add flavors to the entry")
                return           
              
            writeToLog("INFO","Step 4: Going to Download the flavor")
            if self.common.entryPage.downloadAFlavor(self.entryName, self.flavorsList[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to Download the flavor")
                return                  
              
            writeToLog("INFO","Step 2: Going to upload the downloaded  Flavor")
            if self.common.upload.uploadEntry(self.filePathDownloaded, self.entryName + '_Downloaded', "downloaded description", "downloadedtags1,downloadedtags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload the downloaded  Flavor")
                return
              
            writeToLog("INFO","Step 2: Going to verify uploaded entry")
            if self.common.player.navigateToEntryClickPlayPauseAndVerify(self.entryName + '_Downloaded', "0:05") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify uploaded entry")
                return

            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteSingleEnthryFromMyMedia(self.entryName)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName + '_Downloaded')
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')