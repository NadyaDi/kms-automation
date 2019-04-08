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
    # Test Name : Hotspots - Add Hotspot from HS list
    # Test description:
    # Verify that proper information are displayed in the HS List when no Hotsptos are displayed
    # Verify that the HS List is populated with the new hotspots created
    # Verify that the HS List is properly updated after removing available Hotspots from the list
    #================================================================================================================================
    testNum = "5112"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For Hotspots List while having an empty list of hotspots and then a populated list of hotspots"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotOne            = ['Hotspot Title One', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', '', '']
    hotspotTwo            = ['Hotspot Title Two', enums.keaLocation.TOP_LEFT, 5, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    
    # This Dictionary is used in order to create and verify the hotspots
    hotspotOneDict               = {'1':hotspotOne}
    hotspotTwoDict               = {'1':hotspotTwo}
    hotspotOneTwoDict            = {'1':hotspotOne, '2':hotspotTwo}
         
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - HS List", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
             
            writeToLog("INFO","Step 2: Going to navigate to the KEA Hotspots tab for " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True, timeOut=40) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Hotspots tab for " + self.entryName + " entry")
                return

            writeToLog("INFO","Step 3: Going to verify the Hotspot List while having no Hotspots Available")
            if self.common.kea.hotspotListVerification('', 0) == False:
                writeToLog("INFO","Step 3: FAILED to verify the Hotspot List while having no Hotspots Available")
                return 
            
            writeToLog("INFO","Step 4: Going to add a new hotspot for the " + self.entryName + " entry")
            if self.common.kea.hotspotCreation(self.hotspotOneDict, False) == False:
                writeToLog("INFO","Step 4: FAILED to add a new hotspot for the " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 5: Going to verify the Hotspot List while having one Hotspot Available")
            if self.common.kea.hotspotListVerification(self.hotspotOneDict, None) == False:
                writeToLog("INFO","Step 5: FAILED to verify the Hotspot List while having one Hotspot Available")
                return
            
            writeToLog("INFO","Step 6: Going to add the second hotspot for the " + self.entryName + " entry")
            if self.common.kea.hotspotCreation(self.hotspotTwoDict, False) == False:
                writeToLog("INFO","Step 6: FAILED to add second hotspot for the " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 7: Going to verify the Hotspot List while having two Hotspots Available")
            if self.common.kea.hotspotListVerification(self.hotspotOneTwoDict, None) == False:
                writeToLog("INFO","Step 7: FAILED to verify the Hotspot List while having two Hotspots Available")
                return
            
            writeToLog("INFO","Step 8: Going to remove one hotspot from the " + self.entryName + " entry")
            if self.common.kea.hotspotActions(self.hotspotOne[0], enums.keaHotspotActions.DELETE) == False:
                writeToLog("INFO","Step 8: FAILED to remove one hotspot from the " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 9: Going to verify the Hotspot List after removing one Hotspot from the list")
            if self.common.kea.hotspotListVerification(self.hotspotTwoDict, None) == False:
                writeToLog("INFO","Step 9: FAILED to verify the Hotspot List after removing one Hotspot from the list")
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