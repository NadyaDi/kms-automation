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
    # Test Name : Slide Deck Upload - change slide location
    # Test description:
    # Slide Deck Upload - - change slide location:
    # Enter entry edit page and go to time line tab
    # Upload a pptx file.
    # All file slides will spread evenly in the entry time line
    # In the player check that all the slides appear in the slides menu
    # From the Time line delete several slides 
    # Change to several slides their time in the time line  
    # In the player verify that the slides that was changed display now in the new time
    #================================================================================================================================
    testNum     = "3276"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\timelineQRCode.pptx'
    slidesQrCodeAndTimeList = None
    deleteSlidesList = None
    changeTimeOfSlidesList = None
    
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
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload - change slide location", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2 
            
            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'),('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09'),
                                            ('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:21'), ('22','00:22'), ('23','00:23'), ('24','00:24'), ('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28'), ('29','00:29')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)  

            self.deleteSlidesList = [('15','00:15'), ('21','00:21')]
            self.deleteSlidesList = collections.OrderedDict(self.deleteSlidesList)  
            
            # in this list the key is the current time and the value is the new time
            self.changeTimeOfSlidesList = [('00:01','00:15'), ('00:23','00:21'), ('00:07','00:23')]
            self.changeTimeOfSlidesList = collections.OrderedDict(self.changeTimeOfSlidesList)
            
            self.newSlidesQrCodeAndTimeList = [('0','00:00'), ('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('8','00:08'), ('9','00:09'),('10','00:10'), 
                                            ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:01'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:23'), ('22','00:22'), ('23','00:07'), ('24','00:24'),('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28')]
            self.newSlidesQrCodeAndTimeList = collections.OrderedDict(self.newSlidesQrCodeAndTimeList)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                                   
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                return
                          
            writeToLog("INFO","Step 3: Going add upload slide deck")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList) == False:
                writeToLog("INFO","Step 3: FAILED to add slides to entry time line")
                return
                   
            # remove slides from  slides list (slidesQrCodeAndTimeList) in order to move different slides location  
            writeToLog("INFO","Step 4: Going to remove slides from slides main list (slidesQrCodeAndTimeList)")
            if self.common.editEntryPage.deleteSlidesFromTimeLine(self.entryName, self.deleteSlidesList) == False:
                writeToLog("INFO","Step 4: FAILED to remove slides from time line")  
                return 
                                    
            writeToLog("INFO","Step 5: Going change slides time")
            if self.common.editEntryPage.changeSlidesTimeInTimeLine(self.entryName, self.changeTimeOfSlidesList) == False:
                writeToLog("INFO","Step 5: FAILED to change slide time in time line")
                return
                       
            writeToLog("INFO","Step 6: Going to navigate to entry page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to entry page: " + self.entryName)
                return  
                
            sleep(3)
            writeToLog("INFO","Step 7: Going to change player view")
            if self.common.player.changePlayerView(enums.PlayerView.SWITCHVIEW) == False:
                writeToLog("INFO","Step 7: FAILED change player view to: " + enums.PlayerView.SWITCHVIEW)
                return
                
            writeToLog("INFO","Step 8: Going to verify that the new slides display correctly")
            if self.common.player.verifyslidesThatChangedLocationInTimeLine(self.changeTimeOfSlidesList) == False:
                writeToLog("INFO","Step 8: FAILED to verify slide change")
                return
              
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload - change slide location' was done successfully")            
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")  
        except:
            pass       
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')