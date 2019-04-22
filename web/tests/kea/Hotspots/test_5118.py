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
    # Test Name : Hotspots - Cancel hotspot creation and saving 
    # Test description:
    # Verify Hotpot Creation Interrupts when:
    # Clicking on the Cancel Button
    # Clicking on the Player Screen
    # Switching between tabs
    # Exiting the KEA Editor page
    #================================================================================================================================
    testNum = "5118"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For Hotspot Creation where we performed four types of hotspot creation interrupts"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"
    instanceURL         = None

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list is used in order to trigger the specific hotspot creation interrupt
    interruptCancelButton         = [enums.keaHotspotCreationInterrupt.CANCEL_BUTTON, enums.keaLocation.BOTTOM_RIGHT]
    interruptCancelOutside        = [enums.keaHotspotCreationInterrupt.CANCEL_OUTSIDE, enums.keaLocation.BOTTOM_LEFT]
    interruptCancelSwitchTab      = [enums.keaHotspotCreationInterrupt.TAB_SWITCHING, enums.keaLocation.CENTER]
    interruptCancelExitKea        = [enums.keaHotspotCreationInterrupt.EXIT_KEA, enums.keaLocation.TOP_LEFT]
    
    # This Dictionary is used in order to call the interrupts within the for loop from the test case
    interruptDict                 = {'1':interruptCancelButton, '2':interruptCancelOutside, '3':interruptCancelSwitchTab, '4':interruptCancelExitKea}
         
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Interrupt Types", self.testNum)
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
            
            i = 3
            for x in range(0, len(self.interruptDict)):
                currentInterruptDetails = self.interruptDict[str(x+1)]
                writeToLog("INFO","Step " + str(i) + ": Going to perform  " + currentInterruptDetails[0].value + " interrupt on " + self.entryName)
                if self.common.kea.hotspotCreationInterrupts(currentInterruptDetails[0], currentInterruptDetails[1], self.entryName) == False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to perform  " + currentInterruptDetails[0].value + " interrupt on " + self.entryName)
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