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
    # Test Name : Hotspots - General layout UI (without Hotspots)
    # Test description:
    # Verify that all the specific elements for the Hotspots Tab are displayed while having no Hotspots created
    # Verify that all the remaining KEA Tabs can be opened and properly presented after switching from Hotsptos Tab to them
    # Verify that the Hotspots tab is properly resumed after switching between different tabs of KEA
    #================================================================================================================================
    testNum = "5121"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "In all the KEA Tabs while having no Hotspots created and resuming back to the Hotspots Tab"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
        
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - General Layout without Hotspots created", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
                
            writeToLog("INFO","Step 2: Going to navigate to the KEA Editor for " + self.entryName + " entry")
            if self.common.kea.launchKEA(self.entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Editor for " + self.entryName + " entry")
                return
                                       
            writeToLog("INFO","Step 3: Going to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA Tab are presented properly")
            if self.common.kea.keaTabVerification(self.entryName, enums.keaTab.HOTSPOTS, True, False, False) == False:
                writeToLog("INFO","Step 3: FAILED to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA Tab are presented properly")
                return
            
            writeToLog("INFO","Step 4: Going to verify that all the expected elements for " + enums.keaTab.VIDEO_EDITOR.value + " KEA Tab are presented properly")
            if self.common.kea.keaTabVerification(self.entryName, enums.keaTab.VIDEO_EDITOR, False, False, False) == False:
                writeToLog("INFO","Step 4: FAILED to verify that all the expected elements for " + enums.keaTab.VIDEO_EDITOR.value + " KEA Tab are presented properly")
                return
            
            writeToLog("INFO","Step 5: Going to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA Tab are presented properly after resuming it from " + enums.keaTab.VIDEO_EDITOR.value )
            if self.common.kea.keaTabVerification(self.entryName, enums.keaTab.HOTSPOTS, True, False, False) == False:
                writeToLog("INFO","Step 5: FAILED to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA are presented properly after resuming it from " + enums.keaTab.VIDEO_EDITOR.value )
                return
            
            writeToLog("INFO","Step 6: Going to verify that all the expected elements for " + enums.keaTab.QUIZ.value + " KEA Tab are presented properly")
            if self.common.kea.keaTabVerification(self.entryName, enums.keaTab.QUIZ, False, False, False) == False:
                writeToLog("INFO","Step 6: FAILED to verify that all the expected elements for " + enums.keaTab.QUIZ.value + " KEA Tab are presented properly")
                return
            
            writeToLog("INFO","Step 7: Going to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA Tab are presented properly after resuming it from " + enums.keaTab.QUIZ.value )
            if self.common.kea.keaTabVerification(self.entryName, enums.keaTab.HOTSPOTS, True, False, False) == False:
                writeToLog("INFO","Step 7: FAILED to verify that all the expected elements for " + enums.keaTab.HOTSPOTS.value + " KEA are presented properly after resuming it from " + enums.keaTab.QUIZ.value )
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