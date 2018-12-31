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
    #  @Author: Tzachi guetta
    # Test Name : Trim entry with slides and captions
    #================================================================================================================================
    testNum     = "4622"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    captionLanguage = 'Afar'
    captionLabel = 'abc'
    captionText = '- Caption search 2'    
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Trim-Caption.srt'        
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Trim entry with slides and captions", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2
            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'),('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09'),
                                            ('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:21'), ('22','00:22'), ('23','00:23'), ('24','00:24'), ('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28'), ('29','00:29')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)           
            
            
            self.deleteSlidesList = [('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'), ('20','00:20'), ('21','00:21')]
            self.deleteSlidesList = collections.OrderedDict(self.deleteSlidesList) 
            expectedEntryDuration = "0:20"
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

            writeToLog("INFO","Step 4: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
                return    
            
            writeToLog("INFO","Step 5: Going to click on caption tab")
            if self.common.editEntryPage.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to click on caption tab")
                return            
            
            writeToLog("INFO","Step 6: Going to add caption")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to upload caption")
                return
                        
            writeToLog("INFO","Step 7: Going to trim the entry from 10sec to 20sec")  
            if self.common.kea.trimEntry(self.entryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to trim the entry from 10sec to 20sec")
                return
            
            writeToLog("INFO","Step 8: Going to collect the new entry's QR codes")  
            self.QRlist = self.common.player.collectQrOfSlidesFromPlayer(self.entryName)
            if  self.QRlist == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to collect the new entry's QR codes")
                return
                        
            self.isExistQR = ["5", "7", "22", "28"];
            self.isAbsentQR = ["12", "13", "15", "17"];
            writeToLog("INFO","Step 9: Going to verify the entry duration (using QR codes)")  
            if self.common.player.compareLists(self.QRlist, self.isExistQR, self.isAbsentQR, enums.PlayerObjects.QR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify the entry duration (using QR codes)")
                return
            
            writeToLog("INFO","Step 10: Going to collect all the presented captions on the player (after the entry was trimmed)")  
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.entryName, fromActionBar=False)
            if  self.captionList == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to collect all the presented captions on the player (after the entry was trimmed)")
                return
             
            self.isExist = ["Caption5search", "Caption7search", "Caption22search", "Caption28search"];
            self.isAbsent = ["Caption12search", "Caption13search", "Caption15search", "Caption17search"];
            writeToLog("INFO","Step 11: Going to verify the captions that were collected")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify the captions that were collected")
                return
                
            #########################################################################
            writeToLog("INFO","TEST PASSED")            
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