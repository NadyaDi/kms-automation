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
    # Test Name : Hotspots - Change Hotspot Location using Advanced Settings
    # Test description:
    # Create five hotspots in five different locations ( top right / top left / center / buttom right / buttom left )
    # Move the existing hotspots to a new location using Advanced Settings
    #================================================================================================================================
    testNum = "5151"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entry that had Five Hotspots set to an initial position and then Four of them Changed to a new position using Advanced Settings"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to specify the path of the video entry
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # These lists and dictionary are used in order to create new hotspots inside the entry
    hotspotOne                  = ['Hotspot One', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotTwo                  = ['Hotspot Two', enums.keaLocation.TOP_LEFT, 10, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotThree                = ['Hotspot Three', enums.keaLocation.CENTER, 15, 20, '', enums.textStyle.THIN, '', '', 12, 12]
    hotspotFour                 = ['Hotspot Four', enums.keaLocation.BOTTOM_RIGHT, 20, 25, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotFive                 = ['Hotspot Five', enums.keaLocation.BOTTOM_LEFT, 25, 30, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotsDictInitial         = {'1':hotspotOne,'2':hotspotTwo, '3':hotspotThree, '4':hotspotFour, '5':hotspotFive}
    
    # This list is used in order to specify the new location for our created hotspots
    hotspotOneNewLocation       = [hotspotOne[0], enums.keaLocation.BOTTOM_RIGHT]
    hotspotTwoNewLocation       = [hotspotTwo[0], enums.keaLocation.BOTTOM_LEFT]
    hotspotFourNewLocation      = [hotspotFour[0], enums.keaLocation.TOP_RIGHT]
    hotspotFiveNewLocation      = [hotspotFive[0], enums.keaLocation.TOP_LEFT]
    hotspotChangeLocationDict   = {'1':hotspotOneNewLocation, '2':hotspotTwoNewLocation, '3':hotspotFourNewLocation, '4':hotspotFiveNewLocation}
    
    # These lists and dictionary are used in order to verify new hotspots location in entry page
    hotspotOne                  = ['Hotspot One', enums.keaLocation.BOTTOM_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    hotspotTwo                  = ['Hotspot Two', enums.keaLocation.BOTTOM_LEFT, 10, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    hotspotThree                = ['Hotspot Three', enums.keaLocation.CENTER, 15, 20, '', enums.textStyle.THIN, '', '', 12, 12]
    hotspotFour                 = ['Hotspot Four', enums.keaLocation.TOP_RIGHT, 20, 25, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotFive                 = ['Hotspot Five', enums.keaLocation.TOP_LEFT, 25, 30, '', enums.textStyle.BOLD, '', '', 12, 16]
    hotspotsDictChanged         = {'1':hotspotOne,'2':hotspotTwo, '3':hotspotThree, '4':hotspotFour, '5':hotspotFive}    
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Change Location using Advanced Settings", self.testNum)
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
            if self.common.kea.hotspotCreation(self.hotspotsDictInitial, openHotspotsTab=True) == False:
                writeToLog("INFO","Step 3: FAILED to create hotspots for the " + self.entryName)
                return
             
            i = 4
            for x in range(0, len(self.hotspotChangeLocationDict)):
                # Take the details for the current hotspot
                hotspotNewLocationDetailsList = self.hotspotChangeLocationDict[str(x+1)]
                hotspotName                   = hotspotNewLocationDetailsList[0]
                hotspotNewLocation            = hotspotNewLocationDetailsList[1]
                writeToLog("INFO","Step " + str(i) +": Going to verify the timeline section for " + self.entryName +" entry, after creating multiple hotspots")
                if self.common.kea.changeHotspotLocationSettings(hotspotName, hotspotNewLocation) == False:
                    writeToLog("INFO","Step " + str(i) +": FAILED to verify the timeline section for " + self.entryName +" entry, after creating multiple hotspots")
                    return
                else:
                    i += 1
                              
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step " + str(i) +": Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step " + str(i) +": FAILED to navigate to the entry page for " + self.entryName)
                return
            else:
                i += 1
            
            presentedHotspotsDetailsList = self.common.player.returnPresentedHotspotDetails()
            writeToLog("INFO","Step " + str(i) +": Going to verify the hotspots from the " + self.entryName + " entry")
            if self.common.player.hotspotVerification(self.hotspotsDictChanged, presentedHotspotsDetailsList) == False:
                writeToLog("INFO","Step " + str(i) +": FAILED to verify the hotspots from the " + self.entryName + " entry")
                return
            else:
                i += 1
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