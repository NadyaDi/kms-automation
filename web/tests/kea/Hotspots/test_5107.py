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
    # Test Name : Hotspots: Hover player and safe zone to select hotspot position 
    # Test description:
    # Verify that the Add New Hotspot tool tip is properly displayed while verifying it in five different places of the player
    # Verify that the Protected Zone tool tip is properly displayed while verifying it in three different places of the player
    # Verify that the Add New Hotspot tool tip is not presented on existing hotspots locations
    #================================================================================================================================
    testNum = "5107"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For tool tips while being in different locations of the player, including protected zone and hotspots"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotOne    = ['Hotspot Centered', enums.keaLocation.CENTER]
    
    # This Dictionary is used in order to create and verify the hotspots
    hotspotsDict  = {'1':hotspotOne}
    
    locationListWithoutHotspots  = [enums.keaLocation.TOP_LEFT, enums.keaLocation.TOP_RIGHT, enums.keaLocation.BOTTOM_LEFT, enums.keaLocation.BOTTOM_RIGHT, enums.keaLocation.CENTER, enums.keaLocation.PROTECTED_ZONE_LEFT, enums.keaLocation.PROTECTED_ZONE_CENTER, enums.keaLocation.PROTECTED_ZONE_RIGHT]
    locationListWithHotspots     = [enums.keaLocation.TOP_LEFT, enums.keaLocation.TOP_RIGHT, enums.keaLocation.BOTTOM_LEFT, enums.keaLocation.BOTTOM_RIGHT, enums.keaLocation.PROTECTED_ZONE_LEFT, enums.keaLocation.PROTECTED_ZONE_CENTER, enums.keaLocation.PROTECTED_ZONE_RIGHT]

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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Player and Safe Zone Verification", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
 
            writeToLog("INFO","Step 2: Going to navigate to the KEA Hotspots tab for " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True, timeOut=40) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Hotspots tab for " + self.entryName + " entry")
                return
             
            x = 3
            for location in self.locationListWithoutHotspots:
                writeToLog("INFO","Step " + str(x)+ " : Going to verify the hotspot tool tip at the following location: " + location.value + " before creating a hotspot")
                if self.common.kea.hotspotToolTipVerification(location) == False:
                    writeToLog("INFO","Step " + str(x) + ": FAILED  to verify the hotspot tool tip at the following location: " + location.value + " before creating a hotspot")
                    return
                 
                x += 1
                 
            writeToLog("INFO","Step " + str(x)+ " : Going to create hotspots for the " + self.entryName)
            if self.common.kea.hotspotCreation(self.hotspotsDict, openHotspotsTab=False) == False:
                writeToLog("INFO","Step " + str(x)+ " : FAILED to create hotspots for the " + self.entryName)
                return
            else:
                x += 1
 
            for location in self.locationListWithoutHotspots:
                writeToLog("INFO","Step " + str(x)+ " : Going to verify the hotspot tool tip at the following location: " + location.value + " after creating a hotspot")
                if self.common.kea.hotspotToolTipVerification(location) == False:
                    writeToLog("INFO","Step " + str(x) + ": FAILED  to verify the hotspot tool tip at the following location: " + location.value + " after creating a hotspot")
                    return
                x += 1

            writeToLog("INFO","Step " + str(x)+ " : Going to verify that the Add New Hotspot tool tip is not presented at the location where the hotspot has been created")
            if self.common.kea.hotspotToolTipVerification('', True) == False:
                writeToLog("INFO","Step " + str(x) + ": FAILED to verify that the Add New Hotspot tool tip is not presented at the location where the hotspot has been created")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')