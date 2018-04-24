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
    #  @Author: Michal Zomper
    # Test description:
    # Slide Deck Upload -  A-sync upload:
    # Upload 2 entries
    # Enter entry edit page and go to time line tab
    # Upload a pptx file.
    # will the ppt file is uploaded close the upload window by clicking on "back to time line"
    # Navigate to the second entry that uploaded
    # Perform play/ pause in the player 
    # Delete the entry
    # Go back to the first entry with the ppt file and verify that the upload was done and all slides display in the menu slide bar 
    # In entry page check some of the slides to see that the correct slide display in the correct time
    #================================================================================================================================
    testNum     = "3284"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10secQrMidLeftSmall.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\10SlidestimelineQRCode.pptx'
    slidesQrCodeAndTimeList = None
    timeToStop = "0:08"
    
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
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload- search slides", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2 
            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'), ('2','00:02'), ('3','00:03'),('4','00:04'),('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)
            self.slidesWithName = [('second slide','00:02'),('fifth slide','00:05'), ('eighth slide','00:08')]
            self.slidesWithName = collections.OrderedDict(self.slidesWithName)
                                         
                                            
           
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload first entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry name: " + self.entryName)
                return
                                     
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                return
                           
            writeToLog("INFO","Step 3: Going add upload slide deck")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add slides to entry time line")
                return
             
            writeToLog("INFO","Step 4: Going to add names to slides")
            if self.common.editEntryPage.addNameToslides(self.slidesWithName) == False:
                writeToLog("INFO","Step 4: FAILED to add names to slides")
                return
             
            writeToLog("INFO","Step 5: Going to navigate to entry page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to entry page: " + self.entryName1)
                return  
            
            writeToLog("INFO","Step 6: Going to search slides in slides menu bar")
            if self.common.player.searchSlideInSlidesBarMenu(self.slidesWithName, len(self.slidesQrCodeAndTimeList)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to search slides in slides menu bar")
                return            
            
            self.common.player.switchToPlayerIframe() 
            writeToLog("INFO","Step 7: Going to close slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 7: FAILED to click and open slides bar menu")
                return
            
#             sleep(3)
#             index = 0
#             writeToLog("INFO","Step 8: Going to check 4 slide (slide from the start / 2 in the middle / end of the video) and see that they appear at the correct time and did not deleted with the chapter")
#             for i in range(2):
#                 sleep(2)
#                 index = index + i + 4 
#                 if self.common.player.verifySlideDisplayAtTheCorrctTime(self.slidesQrCodeAndTimeList[str(index)][1:], index) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step 8: FAILED to verify slide") 
                  
              
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload - A-sync upload' was done successfully")            
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            writeToLog("INFO","**************** Ended: teardown_method *******************")  
        except:
            pass       
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')