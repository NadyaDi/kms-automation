import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Hotspots - Create Hotspots while playing the video
    # Test description:
    # Enter in Hotspots tab, play the video and place a Hotspot while the video is still playing
    # Switch Between the KEA tabs, and resume back to the Hotspots
    # Verify that a new Hotspot is created at second zero after switching back to the Hotspots tab
    #================================================================================================================================
    testNum = "5115"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For Hotspot created while the video was playing and after switching between the KEA sections"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"
    instanceURL         = None

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotOne             = ['Hotspot Title One', '', '00:15', '', 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotOneVerification = ['Hotspot Title One', '', 15, 30, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotTwo             = ['Hotspot Title Two', enums.keaLocation.TOP_LEFT, 0, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    
    # This Dictionary is used in order to create and verify the hotspots
    hotspotOneDict               = {'1':hotspotOne}
    hotspotTwoDict               = {'1':hotspotTwo}
    hotspotVerificationDict      = {'1':hotspotTwo, '2':hotspotOneVerification}
         
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
            # Variables used in order to proper create the Entry
            self.entryName             = clsTestService.addGuidToString("Hotspots - Creation Types", self.testNum)
            self.instanceURL           = self.common.base.driver.current_url
            self.common.admin.allowHotspots(True)
            self.common.base.navigate(self.instanceURL)
            self.common.admin.allowEditor(True)
            self.common.base.navigate(self.instanceURL)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
                
            writeToLog("INFO","Step 2: Going to navigate to the KEA Hotspots tab for " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True, timeOut=40) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Hotspots tab for " + self.entryName + " entry")
                return
                 
            writeToLog("INFO","Step 3: Going to create a new hotspot while using Hotspot Creation Type " + enums.keaHotspotCreationType.VIDEO_PLAYING.value + " for the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotOneDict, False, enums.keaHotspotCreationType.VIDEO_PLAYING) == False:
                writeToLog("INFO","Step 3: FAILED to create a new hotspot while using Hotspot Creation Type " + enums.keaHotspotCreationType.VIDEO_PLAYING.value + " for the " + self.entryName)
                return
             
            writeToLog("INFO","Step 4: Going to navigate to the KEA Editor tab of " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.VIDEO_EDITOR, navigateToEntry=False, timeOut=0) == False:
                writeToLog("INFO","Step 4: FAILED to navigate to the KEA Editor tab of " + self.entryName + " entry")
                return
             
            writeToLog("INFO","Step 5: Going to navigate back to the KEA Hotspots tab of " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=False, timeOut=0) == False:
                writeToLog("INFO","Step 5: FAILED to navigate back to the KEA Hotspots tab of " + self.entryName + " entry")
                return
             
            writeToLog("INFO","Step 6: Going to create a new hotspot while using Hotspot Creation Type " + enums.keaHotspotCreationType.VIDEO_PAUSED.value + " for the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotTwoDict, False) == False:
                writeToLog("INFO","Step 6: FAILED to create a new hotspot while using Hotspot Creation Type " + enums.keaHotspotCreationType.VIDEO_PAUSED.value + " for the " + self.entryName)
                return
             
            writeToLog("INFO","Step 7: Going to verify the timeline section for " + self.entryName +" entry, after creating Hotspots While Video was Playing and Stopped")
            if self.common.kea.hotspotTimelineVerification(self.hotspotVerificationDict) == False:
                writeToLog("INFO","Step 7: FAILED to verify the timeline section for " + self.entryName +" entry, after creating Hotspots While Video was Playing and Stopped")
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Hotspots test case has been successfully verified " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')