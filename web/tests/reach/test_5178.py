import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *

class Test:
    
    #================================================================================================================================
    # @Author: Inbar Willman
    # Test Name: Navigate to captions requests
    # Test description:

    #================================================================================================================================
    testNum     = "5178"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName= None
    categorylName = 'OpenCategoryForMyHistory'
    categoryList = [categorylName]
    entryDescription = "description"
    entryTags = "tag1,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    captionFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\captionsForReach.str'
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('Reach - Add captions', self.testNum)
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return       
                 
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
                 
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
            
#             writeToLog("INFO","Step 5: Going to add captions to entry")
#             if self.common.editEntryPage.addCaptions(self.captionFilePath, captionLanguage, captionLabel) == False:
#                 writeToLog("INFO","Step 5: FAILED to add captions to entry")
#                 return            
#             
#             writeToLog("INFO","Step 5: Going to choose 'Captions Requests' option")
#             if self.common.entryPage.chooseCaptionsRequestsOption() == False:
#                 writeToLog("INFO","Step 5: FAILED to choose 'Captions Requests' option")
#                 return 
#             
#             writeToLog("INFO","Step 6: Going to verify that 'Captions Requests' section is empty")
#             if self.common.reach.verifyCaptionsRequestsSection(True) == False:
#                 writeToLog("INFO","Step 6: FAILED to verify that 'Captions Requests' section is empty")
#                 return
#             
#             writeToLog("INFO","Step 7: Going to order captions")
#             if self.common.reach.orderCaptionViaKMS(service=enums.OrderCaptionsServiceOptions.PROFESSIONAL) == False:
#                 writeToLog("INFO","Step 7: FAILED to order captions")
#                 return     
#                                                        
#             writeToLog("INFO","Step 8: Going to verify captions section")
#             if self.common.reach.verifyCaptionsRequestsSection(captionsRequestRowData=['08/05/19', 'Professional', 'Turkish', 'Pending'],captionsRequestDetails=['ella.lidich@kaltura.com', 'Captions', 'Immediate', '0']) == False:
#                 writeToLog("INFO","Step 8: FAILED to verify captions section")
#                 return 
#
#             writeToLog("INFO","Step 1: Going to approve captions request") 
#             self.common.apiClientSession.startCurrentApiClientSession('4769')
#             self.common.apiClientSession.getEntryCaptionsRequestsId("0_y9tusc4v")
#             if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description, None) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to approve captions request")
#                 return
# 
#             writeToLog("INFO","Step 8: Going to cancel captions request")
#             if self.common.reach.cancelCaptionsRequest(0, ['08/05/19', 'Professional', 'Turkish', 'Pending Approval']) == False:
#                 writeToLog("INFO","Step 8: FAILED to cancel captions reques")
#                 return
            
            writeToLog("INFO","Step 8: Going to cancel captions request")
            if self.common.reach.navigateToCaptionsEditor() == False:
                writeToLog("INFO","Step 8: FAILED to cancel captions reques")
                return              
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)        
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')