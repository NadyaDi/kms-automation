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
    # Test Name : Hotspots: Edited Hotspots
    # Test description:
    # Create a new entry with Five hotspots, and verify them in both time line section and entry page
    # Edit one of the hotspots and then verify them in both time line section and entry page
    #================================================================================================================================
    testNum = "5104"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For a new Entry that was verified while having five hotspots and then one edited"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotOne      = ['Hotspot Title One', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotOneEdit  = ['Hotspot Title One Edited', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotTwo      = ['Hotspot Title Two', enums.keaLocation.TOP_LEFT, 5, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotThree    = ['Hotspot Title Three', enums.keaLocation.CENTER, 15, 20, 'https://autothree.kaltura.com/', enums.textStyle.THIN, '', '', 12, 12]
    hotspotFour     = ['Hotspot Title Four', enums.keaLocation.BOTTOM_RIGHT, 20, 25, '', enums.textStyle.THIN, '', '', 12, 16]
    hotspotFive     = ['Hotspot Title Five', enums.keaLocation.BOTTOM_LEFT, 25, 30, '', enums.textStyle.BOLD, '', '', 18, 16]
    
    # This Dictionary is used in order to create and verify the hotspots
    hotspotsDict           = {'1':hotspotOne, '2':hotspotTwo, '3':hotspotThree, '4':hotspotFour, '5':hotspotFive}
    
    # This Dictionary is used in order to verify the hotspots after one hotspot has been deleted
    hotspotsDictUpdated    = {'1':hotspotOneEdit, '2':hotspotTwo, '3':hotspotThree, '4':hotspotFour, '5':hotspotFive}
    
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - With one Hotspot Edited", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
              
            writeToLog("INFO","Step 2: Going to navigate to the KEA Editor for " + self.entryName + " entry")
            if self.common.kea.launchKEA(self.entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Editor for " + self.entryName + " entry")
                return
                     
            writeToLog("INFO","Step 3: Going to create hotspots for the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotsDict, openHotspotsTab=True) == False:
                writeToLog("INFO","Step 3: FAILED to create hotspots for the " + self.entryName)
                return
                
            writeToLog("INFO","Step 4: Going to verify the timeline section for " + self.entryName +" entry, before editing the " + self.hotspotOne[0])
            if self.common.kea.hotspotTimelineVerification(self.hotspotsDict, 5) == False:
                writeToLog("INFO","Step 4: FAILED to verify the timeline section for " + self.entryName +" entry, before editing the " + self.hotspotOne[0])
                return
               
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 5: Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step 5: FAILED to navigate to the entry page for " + self.entryName)
                return
            
            presentedHotspotsDetailsList = self.common.player.returnPresentedHotspotDetails() 
            writeToLog("INFO","Step 6: Going to verify the hotspots from the " + self.entryName + " entry, before editing the " + self.hotspotOne[0])
            if self.common.player.hotspotVerification(self.hotspotsDict, presentedHotspotsDetailsList) == False:
                writeToLog("INFO","Step 6: FAILED to verify the hotspots from the " + self.entryName + " entry, before editing the " + self.hotspotOne[0])
                return
               
            writeToLog("INFO","Step 7: Going to navigate to navigate to KEA " + enums.keaTab.HOTSPOTS.value  + " Section for the " + self.entryName + " entry")
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, True, 0) == False:
                writeToLog("INFO","Step 7: FAILED to navigate to navigate to KEA " + enums.keaTab.HOTSPOTS.value  + " Section for the " + self.entryName + " entry")
                return
                 
            writeToLog("INFO","Step 8: Going to Edit the " + self.hotspotOne[0] + " hotspot from " + self.entryName)
            if self.common.kea.hotspotActions(self.hotspotOne[0], enums.keaHotspotActions.EDIT) == False:
                writeToLog("INFO","Step 8: FAILED to Edit the " + self.hotspotOne[0] + " hotspot from " + self.entryName)
                return
                
            writeToLog("INFO","Step 9: Going to verify the timeline section for " + self.entryName +" entry, after editing the " + self.hotspotOne[0])
            if self.common.kea.hotspotTimelineVerification(self.hotspotsDictUpdated, 5) == False:
                writeToLog("INFO","Step 9: FAILED to verify the timeline section for " + self.entryName +" entry, after editing the " + self.hotspotOne[0])
                return
              
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 10: Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step 10: FAILED to navigate to the entry page for " + self.entryName)
                return
            
            presentedHotspotsDetailsList = self.common.player.returnPresentedHotspotDetails()
            writeToLog("INFO","Step 11: Going to verify the hotspots from the " + self.entryName + " entry, after editing the " + self.hotspotOne[0])
            if self.common.player.hotspotVerification(self.hotspotsDictUpdated, presentedHotspotsDetailsList) == False:
                writeToLog("INFO","Step 11: FAILED to verify the hotspots from the " + self.entryName + " entry, after editing the " + self.hotspotOne[0])
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Hotspots were successfully verified " + self.typeTest)
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