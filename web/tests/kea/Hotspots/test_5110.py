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
    # Test Name : Hotspots - Add / Select & Drag hotspots on player
    # Test description:
    # Create four hotspots on a specific location
    # Move the four hotspots into complete new locations
    # Verify the hotspots on the new locations in both KEA and Entry Page
    #================================================================================================================================
    testNum = "5110"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For four hotspots that location was changed and verified in both KEA and Entry page"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    hotspotTopCenter            = ['Initial Top Center', enums.keaLocation.CENTER, 0, 5, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', '', '']
    hotspotTopRight             = ['Initial Top Right', enums.keaLocation.TOP_RIGHT, 0, 10, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotBottomRight          = ['Initial Bottom Right', enums.keaLocation.BOTTOM_RIGHT, 0, 15, '', enums.textStyle.THIN, '', '', 12, 16]
    hotspotBottomLeft           = ['Initial Bottom Left', enums.keaLocation.BOTTOM_LEFT, 0, 20, '', enums.textStyle.BOLD, '', '', 18, 16]
    hotspotsDict                = {'1':hotspotTopCenter,'2':hotspotTopRight, '3':hotspotBottomRight, '4':hotspotBottomLeft}
    
    # These lists and dictionary are used in order to change the created hotspots to a new location
    hotspotMovedToTopLeft       = ['Initial Top Center', enums.keaLocation.TOP_LEFT]
    hotspotMovedToTopCenter     = ['Initial Top Right', enums.keaLocation.CENTER]
    hotspotMovedToTopRight      = ['Initial Bottom Right', enums.keaLocation.TOP_RIGHT]
    hotspotMovedToBottomRight   = ['Initial Bottom Left', enums.keaLocation.BOTTOM_RIGHT]
    hotspotNewOrderDict         = {'1':hotspotMovedToTopLeft, '2':hotspotMovedToTopCenter, '3':hotspotMovedToTopRight, '4':hotspotMovedToBottomRight}  
    
    # These lists and dictionary are used in order to verify the hotspots in the entry page with the new locations and configurations
    hotspotTopCenter            = ['Initial Top Center', enums.keaLocation.TOP_LEFT, 0, 5, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', '', '']
    hotspotTopRight             = ['Initial Top Right', enums.keaLocation.CENTER, 0, 10, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotBottomRight          = ['Initial Bottom Right', enums.keaLocation.TOP_RIGHT, 0, 15, '', enums.textStyle.THIN, '', '', 12, 16]
    hotspotBottomLeft           = ['Initial Bottom Left', enums.keaLocation.BOTTOM_RIGHT, 0, 20, '', enums.textStyle.BOLD, '', '', 18, 16]
    hotspotsDictChanged         = {'1':hotspotTopCenter,'2':hotspotTopRight, '3':hotspotBottomRight, '4':hotspotBottomLeft}       
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Changed Location", self.testNum)
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
                      
            i = 4
            for x in range(0,len(self.hotspotNewOrderDict)):
                writeToLog("INFO","Step " + str(i) + ": Going to change the hotspot location of " + self.hotspotNewOrderDict[str(x+1)][0] + " to " + self.hotspotNewOrderDict[str(x+1)][1].value)
                if self.common.kea.changeHotspotLocation(self.hotspotNewOrderDict[str(x+1)][0], self.hotspotNewOrderDict[str(x+1)][1]) == False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to change the hotspot location of " + self.hotspotNewOrderDict[str(x+1)][0] + " to " + self.hotspotNewOrderDict[str(x+1)][1].value)
                    return
                i += 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to verify the timeline section for " + self.entryName +" entry, while using the second Hotspot location")
            if self.common.kea.hotspotTimelineVerification(self.hotspotsDictChanged, 4) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the timeline section for " + self.entryName +" entry, while using the second Hotspot location")
                return
                             
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to the entry page for " + self.entryName)
                return
            else:
                i += 1
               
            writeToLog("INFO","Step " + str(i) + ": Going to verify the hotspots from the " + self.entryName + " entry, while using the second Hotspot location")
            if self.common.player.hotspotVerification(self.hotspotsDictChanged, enums.Location.ENTRY_PAGE, embed=False) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the hotspots from the " + self.entryName + " entry, while using the second Hotspot location")
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