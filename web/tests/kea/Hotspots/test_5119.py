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
    # Test Name : Hotspots - Delete Hotspots using multiple type of actions
    # Test description:
    # Going to verify the delete action option in the following scenarios:
    # 1. Confirm the delete action when the video is paused
    # 2. Cancel the delete action when the video is paused
    # 3. Confirm the delete action in a list of five hotspots
    # 4. Cancel the delete action in a list of five hotspots
    # 5. Delete a hotspot when the video is playing and the hotspot is displayed on the player
    # 6. Delete a hotspot when the video is playing and the hotspot is not yet displayed on the player
    #================================================================================================================================
    testNum = "5119"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "For Hotspots that were deleted / cancel deleted, when using a single hotspot or a list of five Hotspots"
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list contains the details that are used in the hotspot creation and verification
    singleHotspot        = ['Single Hotspot', enums.keaLocation.TOP_LEFT, 0, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    
    # This dictionary is used in order to create the Hotspot
    singleHotspotDict    = {'1':singleHotspot}
    
    # Each list contains the details that are used in the hotspot creation and verification
    listHostpotOne       = ['List Hotspot One', enums.keaLocation.TOP_LEFT, 0, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    listHostpotTwo       = ['List Hotspot Two', enums.keaLocation.TOP_RIGHT, 0, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    listHostpotThree     = ['List Hotspot Three', enums.keaLocation.CENTER, 0, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    listHostpotFour      = ['List Hotspot Four', enums.keaLocation.BOTTOM_LEFT, 0, 15, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    listHostpotFive      = ['List Hotspot Five', enums.keaLocation.BOTTOM_RIGHT, 20, 30, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '', '', 18, 12]
    
    # This dictionary is used in order to create the Hotspot
    listHotspotDict     = {'1':listHostpotOne, '2':listHostpotTwo, '3':listHostpotThree, '4':listHostpotFour, '5':listHostpotFive}
    listHotspotDictFour = {'1':listHostpotOne, '2':listHostpotTwo, '3':listHostpotThree, '4':listHostpotFour}
         
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
            self.entryName             = clsTestService.addGuidToString("Hotspots - Delete Types", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
                  
            writeToLog("INFO","Step 2: Going to navigate to the KEA Hotspots tab for " + self.entryName + " entry")              
            if self.common.kea.launchKEATab(self.entryName, enums.keaTab.HOTSPOTS, navigateToEntry=True, timeOut=40) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the KEA Hotspots tab for " + self.entryName + " entry")
                return
             
            writeToLog("INFO","Step 3: Going to create a single hotspot to the " + self.entryName)
            if self.common.kea.hotspotCreation(self.singleHotspotDict, openHotspotsTab=True) == False:
                writeToLog("INFO","Step 3: FAILED to create a single hotspot to the " + self.entryName)
                return
             
            writeToLog("INFO","Step 4: Going to verify that the single hotspot from the " + self.entryName + " can be Cancel Deleted")
            if self.common.kea.hotspotActions(self.singleHotspot[0], enums.keaHotspotActions.CANCEL_DELETE) == False:
                writeToLog("INFO","Step 4: FAILED to verify that the single hotspot from the " + self.entryName + " can be Cancel Deleted")
                return
             
            writeToLog("INFO","Step 5: Going to verify that the single hotspot from the " + self.entryName + " can be Deleted")
            if self.common.kea.hotspotActions(self.singleHotspot[0], enums.keaHotspotActions.DELETE) == False:
                writeToLog("INFO","Step 5: FAILED to verify that the single hotspot from the " + self.entryName + " can be Deleted")
                return
             
            writeToLog("INFO","Step 6: Going to create a list of Five hotspot to the " + self.entryName)
            if self.common.kea.hotspotCreation(self.listHotspotDict, openHotspotsTab=True) == False:
                writeToLog("INFO","Step 6: FAILED to create a single hotspot to the " + self.entryName)
                return
             
            writeToLog("INFO","Step 7: Going to verify that the last hotspot from the list can be Cancel Deleted")
            if self.common.kea.hotspotActions(self.listHostpotFive[0], enums.keaHotspotActions.CANCEL_DELETE) == False:
                writeToLog("INFO","Step 7: FAILED to verify that the last hotspot from the list can be Cancel Deleted")
                return
             
            writeToLog("INFO","Step 8: Going to verify that the last hotspot, " + self.listHostpotFive[0] + " from the list can be Deleted")
            if self.common.kea.hotspotActions(self.listHostpotFive[0], enums.keaHotspotActions.DELETE) == False:
                writeToLog("INFO","Step 8: FAILED to verify that the last hotspot, " + self.listHostpotFive[0] + " from the list can be Deleted")
                return
             
            i = 9
            for x in range(0, len(self.listHotspotDictFour)):
                currentHotspot = self.listHotspotDictFour[str(x+1)]
                 
                writeToLog("INFO","Step " + str(i) + " : Going to verify that the hotspot, " + currentHotspot[0] + " from the list can be Deleted")
                if self.common.kea.hotspotActions(currentHotspot[0], enums.keaHotspotActions.DELETE) == False:
                    writeToLog("INFO","Step " + str(i) + " : FAILED to verify that the hotspot, " + currentHotspot[0] + " from the list can be Deleted")
                    return
                else:
                    i += 1

            writeToLog("INFO","Step " + str(i) + ": Going to create a list of Five hotspot to the " + self.entryName)
            if self.common.kea.hotspotCreation(self.listHotspotDict, openHotspotsTab=True) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a single hotspot to the " + self.entryName)
                return
            else:
                i += 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to trigger the playing process of the " + self.entryName)
            if self.common.base.click(self.common.kea.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to trigger the playing process of the " + self.entryName)
                return
            else:
                i += 1

            writeToLog("INFO","Step " + str(i) + ": Going to verify that the presented hotspot, " + self.listHostpotOne[0] + " can be Deleted while its displayed on the player")
            if self.common.kea.hotspotActions(self.listHostpotOne[0], enums.keaHotspotActions.DELETE) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that the presented hotspot, " + self.listHostpotOne[0] + " can be Deleted while its displayed on the player")
                return
            else:
                i += 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to trigger the playing process of the " + self.entryName)
            if self.common.base.click(self.common.kea.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to trigger the playing process of the " + self.entryName)
                return
            else:
                i += 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to verify that the presented hotspot, " + self.listHostpotFive[0] + " can be Deleted while its not displayed yet on the player")
            if self.common.kea.hotspotActions(self.listHostpotFive[0], enums.keaHotspotActions.DELETE) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that the presented hotspot, " + self.listHostpotFive[0] + " can be Deleted while its not displayed yet on the player")
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