import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "353"
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
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\timelineQRCode.pptx'
    slidesQrCodeAndTimeList = None
    chaptersList = None
    slidesWithoutChapter = None
    firstChapterSlidesList = None
    secondChapterSlidesList = None
    
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
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload - add chapters", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2 
            self.slidesQrCodeAndTimeList = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04','5': '00:05', '6': '00:06', '7': '00:07', '8': '00:08', '9': '00:09',
                                            '10': '00:10', '11': '00:11','12': '00:12', '13': '00:13','14': '00:14','15': '00:15', '16': '00:16', '17': '00:17', '18': '00:18', '19': '00:19',
                                            '20': '00:20', '21': '00:21','22': '00:22', '23': '00:23','24': '00:24','25': '00:25', '26': '00:26', '27': '00:27', '28': '00:28', '29': '00:29'}
            
            self.chaptersList = {'First Chapter':'00:05', 'Second Chapter':'00:14'}
            self.slidesWithoutChapter = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04'}
            self.firstChapterSlidesList = {'1.1': '00:05', '1.2': '00:06', '1.2': '00:07', '1.3': '00:08', '1.4': '00:09', '1.5': '00:10', '1.6': '00:11','1.7': '00:12', '1.8': '00:13'}
            self.secondChapterSlidesList = {'2.1': '00:14','2.2': '00:15', '2.3': '00:16', '2.4': '00:17', '2.5': '00:18', '2.6': '00:19','2.7': '00:20', '2.8': '00:21','2.9': '00:22',
                                            '2.10': '00:23', '2.11': '00:24','2.12': '00:25', '2.13': '00:26', '2.14': '00:27', '2.15': '00:28', '2.16': '00:29'}
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            self.common.editEntryPage.addChapters("QR_30_sec_new.mp4", self.chaptersList)
            
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
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
                           
            writeToLog("INFO","Step 4: Going remove slides from time line")
            if self.common.editEntryPage.deleteSlidesFromTimeLine(self.entryName, self.deleteSlidesList) == False:
                writeToLog("INFO","Step 4: FAILED to remove slides from time line")
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
                return
            sleep(4)
            
            writeToLog("INFO","Step 7: Going verify that the deleted slides doesn't appear in the player")
            if self.common.player.verifySlidesInPlayerSideBar(self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify only the correct slides display in the player")
                return  

            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload - add chapters' was done successfully")            
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