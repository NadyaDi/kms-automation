import time, pytest

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
    # Slide Deck Upload - delete slides:
    # Enter entry edit page and go to time line tab
    # Upload a pdf file.
    # All file slides will spread evenly in the entry time line
    # In the player check that all the slides appear in the slides menu
    # From the Time line delete several slides 
    # In the player check that just the needed slides appear in the slides menu
    #================================================================================================================================
    testNum     = "3274"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\PDFtimelineQRCode.pdf'
    slidesQrCodeAndTimeList = None
    deleteSlidesList = None
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload-delete slides", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2
            
            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'),('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09'),
                                            ('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:21'), ('22','00:22'), ('23','00:23'), ('24','00:24'), ('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28'), ('29','00:29')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)           
            
            
            self.deleteSlidesList = [('5','00:05'), ('11','00:11'), ('15','00:15'), ('21','00:21'), ('24','00:24'), ('28','00:28')]
            self.deleteSlidesList = collections.OrderedDict(self.deleteSlidesList) 
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                        
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                self.status = "Fail"
                return
               
            writeToLog("INFO","Step 3: Going add upload slide deck")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList) == False:
                writeToLog("INFO","Step 3: FAILED to add slides to entry time line")
                self.status = "Fail"
                return
                           
            writeToLog("INFO","Step 4: Going remove slides from time line")
            if self.common.editEntryPage.deleteSlidesFromTimeLine(self.entryName, self.deleteSlidesList) == False:
                writeToLog("INFO","Step 4: FAILED to remove slides from time line")
                self.status = "Fail"
                return
              
            # remove deleted slides from  slides list (slidesQrCodeAndTimeList)
            writeToLog("INFO","Step 5: Going to remove the deleted slides from slides main list (slidesQrCodeAndTimeList)")
            try:
                for slide in self.deleteSlidesList:
                    self.slidesQrCodeAndTimeList.pop(slide)
            except:
                writeToLog("INFO","Step 5: FAILED to remove slide item number " + str(slide) + "from slides main list")  
                self.status = "Fail"
                return 
            
            writeToLog("INFO","Step 6: Going to navigate to Entry Page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED navigate to entry page")
                self.status = "Fail"
                return
            sleep(4)
            
            writeToLog("INFO","Step 7: Going verify that the deleted slides doesn't appear in the player")
            if self.common.player.verifySlidesInPlayerSideBar(self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify only the correct slides display in the player")
                return  
             
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload -delete slide' was done successfully")            
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
            writeToLog("INFO","**************** Ended: teardown_method *******************")  
        except:
            pass       
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')