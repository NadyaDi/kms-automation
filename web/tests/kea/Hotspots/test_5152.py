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
    # Test Name : Hotspots - Change Hotspot Size using Advanced Settings
    # Test description:
    # Create three hotspots inside a new entry that contains:
    # The First hotspot is created using smaller sizes that the default one
    # The second and third are created using larger sizes that the default one
    # Hotspots container sizes and the style properties are verified in the entry page
    #================================================================================================================================
    testNum = "5152"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entry that used three other sizes than the default one, inserted in Advanced Settings"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to specify the path of the video entry
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # These lists and dictionary are used in order to create new hotspots inside the entry
    hotspotSmall                = ['Hotspot Small', enums.keaLocation.CENTER, 0, 10, '', enums.textStyle.NORMAL, '', '', 12, 12, enums.keaHotspotContainerSize.SMALL]
    hotspotMedium               = ['Hotspot Medium', enums.keaLocation.CENTER, 15, 20, '', enums.textStyle.THIN, '', '', 12, 12, enums.keaHotspotContainerSize.MEDIUM]
    hotspotLarge                = ['Hotspot Large', enums.keaLocation.CENTER, 25, 30, '', enums.textStyle.BOLD, '', '', 12, 16, enums.keaHotspotContainerSize.LARGE]
    hotspotsDict                = {'1':hotspotSmall, '2':hotspotMedium, '3':hotspotLarge}
    
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Changed Size using Advanced Settings", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
             
            writeToLog("INFO","Step 2: Going to navigate to the KEA Editor for " + self.entryName + " entry")
            if self.common.kea.launchKEA(self.entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Editor for " + self.entryName + " entry")
                return
                    
            writeToLog("INFO","Step 3: Going to create hotspots inside the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotsDict, openHotspotsTab=True) == False:
                writeToLog("INFO","Step 3: FAILED to create hotspots inside the " + self.entryName)
                return
                            
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 4: Going to navigate to the entry page of " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED to navigate to the entry page of " + self.entryName)
                return
            
            presentedHotspotsDetailsList = self.common.player.returnPresentedHotspotDetails()
            writeToLog("INFO","Step 5: Going to verify the hotspots from the " + self.entryName + " entry")
            if self.common.player.hotspotVerification(self.hotspotsDict, presentedHotspotsDetailsList) == False:
                writeToLog("INFO","Step 5: FAILED to verify the hotspots from the " + self.entryName + " entry")
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Hotspot Test case has been successfully verified for an " + self.typeTest)
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