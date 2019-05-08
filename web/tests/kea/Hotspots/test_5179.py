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
    # Test Name : Hotspots - Edit hotspots start and end time (Advanced settings)
    # Test description:
    # Create four hotspots that have different configurations and unique hotspot time stamp location ( start time / end time )
    # Change the time stamp of a hotspot only by end time
    # Change the time stamp of a hotspot with a new start and end time
    # Change the time stamp of a hotspot with a lower start time and lower end time
    # Leave a hotspot untouched
    # Verify the new time stamp configuration of the hotspots in both KEA Timeline section and Entry Page
    #================================================================================================================================
    testNum = "5179"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entry that had Three Hotspots with time stamp changed and One Hotspot untouched"
    description         = "Description"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to specify the path of the video entry
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # These lists and dictionary are used in order to create new hotspots inside the entry
    hotspotInitialZeroFive               = ['Zero Five To Zero Ten', enums.keaLocation.CENTER, 0, 5, '', enums.textStyle.THIN, '', '', 12, 12]
    hotspotInitialZeroTen                = ['Zero Ten to Five Fifteen', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotInitialTenTwenty              = ['Ten Twenty to Five Ten', enums.keaLocation.TOP_LEFT, 10, 20, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotZeroFifteenUnchanged          = ['Zero Fifteen Unchanged', enums.keaLocation.BOTTOM_RIGHT, 0, 15, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotsDict                         = {'1':hotspotInitialZeroFive,'2':hotspotInitialZeroTen, '3':hotspotInitialTenTwenty, '4':hotspotZeroFifteenUnchanged}
    
    # These lists are used in order to change the time stamp location of the below hotspots
    hotspotZeroTen                       = [hotspotInitialZeroFive[0], '00:00', '00:10']
    hotspotTenFifteen                    = [hotspotInitialZeroTen[0], '00:05', '00:15']
    hotspotFiveTen                       = [hotspotInitialTenTwenty[0], '00:05', '00:10']
    hotspotNewTimeStampList              = [hotspotZeroTen, hotspotTenFifteen, hotspotFiveTen]

    # These lists and dictionary are used in order to create verify the hotspots new time stamp in timeline section and entry page
    hotspotInitialZeroFiveUpdated        = ['Zero Five To Zero Ten', enums.keaLocation.CENTER, 0, 10, '', enums.textStyle.THIN, '', '', 12, 12]
    hotspotInitialZeroTenUpdated         = ['Zero Ten to Five Fifteen', enums.keaLocation.TOP_RIGHT, 5, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotInitialTenTwentyUpdated       = ['Ten Twenty to Five Ten', enums.keaLocation.TOP_LEFT, 5, 10, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotZeroFifteenUnchangedUpdated   = ['Zero Fifteen Unchanged', enums.keaLocation.BOTTOM_RIGHT, 0, 15, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotsDictUpdated                  = {'1':hotspotInitialZeroFiveUpdated,'2':hotspotInitialZeroTenUpdated, '3':hotspotInitialTenTwentyUpdated, '4':hotspotZeroFifteenUnchangedUpdated}
    
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Time Stamp changed with Advanced Settings", self.testNum)
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
            for x in range(0,len(self.hotspotNewTimeStampList)):
                currentHotspotList  = self.hotspotNewTimeStampList[x]
                  
                writeToLog("INFO","Step " + str(i) + ": Going to change the time stamp for " + currentHotspotList[0] + " hotspot")
                if self.common.kea.changeHotspotTimeStamp(currentHotspotList[0], currentHotspotList[1], currentHotspotList[2]) == False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to change the time stamp for " + currentHotspotList[0] + " hotspot")
                    return
                else:
                    i += 1
  
            writeToLog("INFO","Step " + str(i) + ": Going to verify the timeline section for " + self.entryName +" entry, after changing the time stamp of the hotspots")
            if self.common.kea.hotspotTimelineVerification(self.hotspotsDictUpdated, 4) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the timeline section for " + self.entryName +" entry, after changing the time stamp of the hotspots")
                return
            else:
                i += 1
                 
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to the entry page for " + self.entryName)
                return
            else:
                i += 1

            presentedHotspotsDetailsList = self.common.player.returnPresentedHotspotDetails()
            writeToLog("INFO","Step " + str(i) + ": Going to verify the hotspots from the " + self.entryName + " entry, after changing the time stamp of the hotspots")
            if self.common.player.hotspotVerification(self.hotspotsDictUpdated, presentedHotspotsDetailsList) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the hotspots from the " + self.entryName + " entry, after changing the time stamp of the hotspots")
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