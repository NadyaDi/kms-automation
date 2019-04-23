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
    # Test Name : Hotspots - Hotspots list - General UI
    # Test description:
    # Verify the hotspots while using
    # Long titles
    # Long URLs
    # Invalid URLs in both Advanced Settings and Add Hotspot Tool Tip
    # Verify the hotspots creation while using a random generated number of 15 hotsptos
    #================================================================================================================================
    testNum = "5124"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "While using a High Number of Hotsptos and Hotspots with special configurations"
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - HS List General UI", self.testNum)
            
            hotspotSpecialCharacters                 = ['#!@$%^%&%^*&(_+\];dsaHa123', enums.keaLocation.BOTTOM_LEFT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
            hotspotLongTitle                         = ['Hotspot Long Title, How Long you may Ask, well I don t really know, who knows?', enums.keaLocation.CENTER, 10, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
            hotspotLongURL                           = ['Hotspot Long URL', enums.keaLocation.TOP_RIGHT, 15, 20, 'https://autoone.kaltura.com/we-need-a-long-url-for-our-automation-project/it-s-this-long-enough-question-mark', enums.textStyle.BOLD, '', '', 18, 12]
            
            hotspotSpecialDict                       = {'1':hotspotSpecialCharacters, '2':hotspotLongTitle, '3':hotspotLongURL}
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to generate a dictionary that will contain a list of 15 hotspots")
            generatedHotspotDictionary = self.common.kea.keaGenerateHotspotsDictionary(15, 30)
            if len(generatedHotspotDictionary) != 15:
                writeToLog("INFO","Step 1: Going to generate a dictionary that will contain a list of 15 hotspots")
                return
             
            writeToLog("INFO","Step 2: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryName + " entry")
                return
                   
            writeToLog("INFO","Step 3: Going to navigate to the KEA Hotspots Tab for " + self.entryName + " entry")
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, True, 40, False) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to the KEA Hotspots Tab for " + self.entryName + " entry")
                return 
  
            writeToLog("INFO","Step 4: Going to verify the Invalid URL functionality in " + enums.keaHotspotCreationScreen.ADVANCED_SETTINGS.value + " screen")
            if self.common.kea.verifyHotspotsCreationWithInvalidURL(enums.keaHotspotCreationScreen.ADVANCED_SETTINGS, 'invalidurlformat') == False:
                writeToLog("INFO","Step 4: FAILED to verify the Invalid URL functionality in " + enums.keaHotspotCreationScreen.ADVANCED_SETTINGS.value + " screen")
                return
   
            writeToLog("INFO","Step 5: Going to verify the Invalid URL functionality in " + enums.keaHotspotCreationScreen.ADD_HOTSPOT_TOOL_TIP.value + " screen")
            if self.common.kea.verifyHotspotsCreationWithInvalidURL(enums.keaHotspotCreationScreen.ADD_HOTSPOT_TOOL_TIP, 'invalidurlformat') == False:
                writeToLog("INFO","Step 5: FAILED to verify the Invalid URL functionality in " + enums.keaHotspotCreationScreen.ADD_HOTSPOT_TOOL_TIP.value + " screen")
                return
   
            writeToLog("INFO","Step 6: Going to create special hotspots inside the " + self.entryName + " entry")
            if self.common.kea.hotspotCreation(hotspotSpecialDict, False, enums.keaHotspotCreationType.VIDEO_PAUSED) == False:
                writeToLog("INFO","Step 6: FAILED to create special hotspots inside the " + self.entryName + " entry")
                return
               
            writeToLog("INFO","Step 7: Going to verify the timeline section for " + self.entryName +" entry, while having special hotspot configurations")
            if self.common.kea.hotspotTimelineVerification(hotspotSpecialDict, 3) == False:
                writeToLog("INFO","Step 7: FAILED to verify the timeline section for " + self.entryName +" entry, while having special hotspot configurations")
                return
              
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 8: Going to navigate to the entry page for " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                writeToLog("INFO","Step 8: FAILED to navigate to the entry page for " + self.entryName)
                return
                   
            writeToLog("INFO","Step 9: Going to verify the hotspots from the " + self.entryName + " entry, while having special hotspot configurations")
            if self.common.player.hotspotVerification(hotspotSpecialDict, enums.Location.ENTRY_PAGE, embed=False) == False:
                writeToLog("INFO","Step 9: FAILED to verify the hotspots from the " + self.entryName + " entry, while having special hotspot configurations")
                return
                
            writeToLog("INFO","Step 10: Going to navigate back to KEA " + enums.keaTab.HOTSPOTS.value  + " Section for the " + self.entryName + " entry")
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, True, 0) == False:
                writeToLog("INFO","Step 10: FAILED to navigate back to KEA " + enums.keaTab.HOTSPOTS.value  + " Section for the " + self.entryName + " entry")
                return
             
            i = 11
            for x in range(0, len(hotspotSpecialDict)):
                hotspotCurrentName = hotspotSpecialDict[str(x+1)][0]
                writeToLog("INFO","Step " + str(i) + ": Going to empty the Hotspots list from " + self.entryName + " by removing the hotspot: " + hotspotCurrentName)
                if self.common.kea.hotspotActions(hotspotCurrentName, enums.keaHotspotActions.DELETE)== False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to empty the Hotspots list from " + self.entryName + " by removing the hotspot: " + hotspotCurrentName)
                    return
                else:
                    i += 1
       
            writeToLog("INFO","Step " + str(i) + ": Going to create a list of 15 random generated hotspots inside the " + self.entryName + " entry")
            if self.common.kea.hotspotCreation(generatedHotspotDictionary, False, enums.keaHotspotCreationType.VIDEO_PAUSED) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a list of 15 random generated hotspots inside the " + self.entryName + " entry")
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