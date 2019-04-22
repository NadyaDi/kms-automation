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
    # Test Name : Hotspots - Enable and Disable Hotspots Module
    # Test description:
    # Verify that the Hotspots module can be enabled and then accessed from the Editor
    # Verify that the Hotspots module can disabled and unable to access it from Editor
    # Verify that the existing Hotspots are kept while Editor module is disabled
    #================================================================================================================================
    testNum = "5114"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For Hotspots Module when enabled, disabled, re-enabled and then disabled with active hotspots to an entry"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"
    instanceURL         = None

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotOne            = ['Hotspot Title One', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    
    # This Dictionary is used in order to create and verify the hotspots
    hotspotOneDict               = {'1':hotspotOne}
         
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Hotspot Module State", self.testNum)
            self.instanceURL           = self.common.base.driver.current_url
            self.common.admin.allowHotspots(True)
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
             
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 3: Going to disable the Hotspots Module from admin panel")              
            if self.common.admin.allowHotspots(False)== False:
                writeToLog("INFO","Step 3: FAILED to disable the Hotspots Module from admin panel")   
                return
             
            writeToLog("INFO","Step 4: Going to navigate to the KMS page" + self.instanceURL)              
            if self.common.base.navigate(self.instanceURL)== False:
                writeToLog("INFO","Step 4: FAILED to navigate to the KMS page" + self.instanceURL)             
                return
             
            writeToLog("INFO","Step 5: Going to verify that the Hotspots module cannot be accessed from the entry Editor Page")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True) != False:
                writeToLog("INFO","Step 5: FAILED, the Hotspots module could be accessed from the entry Editor Page")
                return
             
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 6: Going to enable the Hotspots Module from admin panel")              
            if self.common.admin.allowHotspots(True)== False:
                writeToLog("INFO","Step 6: FAILED to enable the Hotspots Module from admin panel")   
                return
             
            writeToLog("INFO","Step 7: Going to navigate to the KMS page" + self.instanceURL)              
            if self.common.base.navigate(self.instanceURL)== False:
                writeToLog("INFO","Step 7: FAILED to navigate to the KMS page" + self.instanceURL)             
                return
             
            writeToLog("INFO","Step 8: Going to verify that the Hotspots module can be accessed from the entry Editor Page")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True) == False:
                writeToLog("INFO","Step 8: FAILED, the Hotspots module couldn't be accessed from the entry Editor Page")
                return
             
            writeToLog("INFO","Step 9: Going to create hotspots for the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotOneDict) == False:
                writeToLog("INFO","Step 9: FAILED to create hotspots for the " + self.entryName)
                return
             
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 10: Going to disable the Editor Module from admin panel")              
            if self.common.admin.allowEditor(False)== False:
                writeToLog("INFO","Step 10: FAILED to disable the Editor Module from admin panel")   
                return
             
            writeToLog("INFO","Step 11: Going to navigate to the KMS page" + self.instanceURL)              
            if self.common.base.navigate(self.instanceURL)== False:
                writeToLog("INFO","Step 11: FAILED to navigate to the KMS page" + self.instanceURL)             
                return
             
            writeToLog("INFO","Step 12: Going to navigate to the entry page of " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step 12: FAILED to navigate to the entry page of " + self.entryName)
                return
                 
            writeToLog("INFO","Step 13: Going to verify that the hotspots from the " + self.entryName + " entry are kept, while Hotspots Module is disabled")
            if self.common.player.hotspotVerification(self.hotspotOneDict, enums.Location.ENTRY_PAGE, embed=False) == False:
                writeToLog("INFO","Step 13: FAILED to display existing hotspots for the " + self.entryName + " entry, while the Hotspots Module is disabled")
                return
            self.common.base.switch_to_default_content()
            
            writeToLog("INFO","Step 14: Going to verify that the Launch Editor cannot be accessed")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True) != False:
                writeToLog("INFO","Step 14: FAILED, the Launch Editor could be accessed, although it should have been disabled")
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
            self.common.admin.allowEditor(True)
            self.common.base.navigate(self.instanceURL)
            self.common.admin.allowHotspots(True)
            self.common.base.navigate(self.instanceURL)
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')