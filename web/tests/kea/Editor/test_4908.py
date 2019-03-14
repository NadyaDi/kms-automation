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
    # Test Name : Editor: Clip video entry (with Slides and Captions)
    # Test description:
    # 1. Verify that the captions and slides are present before clipping a video entry
    # 2. Verify that the captions and slides are properly displayed after clipping a video entry
    #================================================================================================================================
    testNum = "4908"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    
    testType = "Video entry that was Clipped while having Slides and Captions"
    description = "Description" 
    tags = "Tags,"
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    
    captionLanguage = 'Afar'
    captionLabel = 'abc'
    captionText = '- Caption search 2'
    
    # Variables used in order to create a video entry with Slides and Captions
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Trim-Caption.srt'    
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
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
            
            
            # Variables used in order to proper create the Entry and the Slides inside it
            self.entryName = clsTestService.addGuidToString("Video Clipped with Slides and Captions", self.testNum)
            expectedEntryDuration = "0:20"
            
            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'),('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09'),
                                            ('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:21'), ('22','00:22'), ('23','00:23'), ('24','00:24'), ('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28'), ('29','00:29')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)           
            
            
            self.deleteSlidesList = [('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'), ('20','00:20'), ('21','00:21')]
            self.deleteSlidesList = collections.OrderedDict(self.deleteSlidesList) 
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return      
                 
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
                 
            writeToLog("INFO","Step 3: Going to wait until the " + self.entryName + " entry has been successfully processed")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED to wait until the " + self.entryName + " entry has been successfully processed")
                return
                 
            writeToLog("INFO","Step 4: Going to navigate to edit entry page for " + self.entryName + " entry")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page for " + self.entryName + " entry")
                return
              
            writeToLog("INFO","Step 5: Going to upload a slide deck for the " + self.entryName + " entry")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList) == False:
                writeToLog("INFO","Step 5: FAILED to upload a slide deck for the " + self.entryName + " entry")
                return
               
            writeToLog("INFO","Step 6: Going to navigate to the Captions Edit Tab")
            if self.common.editEntryPage.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to the Captions Edit Tab")
                return            
               
            writeToLog("INFO","Step 7: Going to add caption for the " + self.entryName + " entry")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                writeToLog("INFO","Step 7: FAILED to add caption for the " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 8: Going to collect " + self.entryName + " entrie's QR codes from Slider, before clipping")  
            self.QRlist = self.common.player.collectQrOfSlidesFromPlayer(self.entryName)
            if  self.QRlist == False:
                writeToLog("INFO","Step 8: FAILED to collect " + self.entryName + " entrie's QR codes from Slider, before clipping")  
                return
                        
            self.isExistQR = ["5", "7", "10", "13", "17", "22", "28"];
            self.isAbsentQR = ["33", "55", "100", "99"];
            writeToLog("INFO","Step 9: Going to verify that all the available Slides are displayed, before clipping")
            if self.common.player.compareLists(self.QRlist, self.isExistQR, self.isAbsentQR, enums.PlayerObjects.QR) == False:
                writeToLog("INFO","Step 9: FAILED  to verify that all the available Slides are displayed, before clipping")
                return
   
            writeToLog("INFO","Step 10: Going to collect all the presented captions from the " + self.entryName + " entrie's player before clipping")  
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.entryName)
            if  self.captionList == False:
                writeToLog("INFO","Step 10: FAILED to collect all the presented captions from the " + self.entryName + " entrie's player before clipping")
                return
               
            self.isExist = ["Caption5search", "Caption7search", "Caption12search", "Caption13search"];
            self.isAbsent = ["Caption100search", "Caption32search"];
            writeToLog("INFO","Step 11: Going to verify that all the captions for " + self.entryName + " entry are presented")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                writeToLog("INFO","Step 11: FAILED to verify that all the captions for " + self.entryName + " entry are presented") 
                return               
                
            writeToLog("INFO","Step 12: Going to trim the " + self.entryName + " entry from second 10 to second 20, leaving a length of the entry of 20 seconds")  
            if self.common.kea.clipEntry(self.entryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 12: FAILED to trim the " + self.entryName + " entry from second 10 to second 20, leaving a length of the entry of 20 seconds")  
                return
            
            writeToLog("INFO","Step 13: Going to collect " + self.entryName + " entrie's QR codes from Slider")  
            self.QRlist = self.common.player.collectQrOfSlidesFromPlayer("Clip of " + self.entryName)
            if  self.QRlist == False:
                writeToLog("INFO","Step 13: FAILED to collect " + self.entryName + " entrie's QR codes from Slider")  
                return
                        
            self.isExistQR = ["5", "7", "22", "28"];
            self.isAbsentQR = ["12", "13", "15", "17"];
            writeToLog("INFO","Step 14: Going to verify that only the Slides that should be kept are presented ( after the entry was clipped)")
            if self.common.player.compareLists(self.QRlist, self.isExistQR, self.isAbsentQR, enums.PlayerObjects.QR) == False:
                writeToLog("INFO","Step 14: FAILED to verify that only the Slides that should be kept are presented ( after the entry was clipped)")
                return
            
            writeToLog("INFO","Step 15: Going to collect all the presented captions on the player (after the entry was clipped)")  
            self.captionList = self.common.player.collectCaptionsFromPlayer("Clip of " + self.entryName)
            if  self.captionList == False:
                writeToLog("INFO","Step 15: FAILED to collect all the presented captions on the player (after the entry was clipped)")
                return
             
            self.isExist = ["Caption5search", "Caption7search", "Caption22search", "Caption28search"];
            self.isAbsent = ["Caption12search", "Caption13search", "Caption15search", "Caption17search"];
            writeToLog("INFO","Step 16: Going to verify the captions that were collected")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                writeToLog("INFO","Step 16: FAILED to verify the captions that were collected")
                return
            ####################################################################################################
            self.status = "Pass"              
            writeToLog("INFO","TEST PASSED, all the elements were properly verified for a " + self.testType)
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(["Clip of " + self.entryName, self.entryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')