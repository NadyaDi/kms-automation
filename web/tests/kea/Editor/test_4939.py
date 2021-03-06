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
    # @Author: Horia Cus
    # Test Name : Editor: Undo timeline functionality
    # Test description:
    # Verify that the undo option has functionality after performing the following actions to a section:
    # 1. Delete
    # 2. Split
    # 3. Set In
    #================================================================================================================================
    testNum     = "4939"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    
    # Test variables
    entryName           = None
    entryDescription    = "Description"
    entryTags           = "Tags,"
    filePathVideo       = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'   
    testType            = "Entry that had sections split,deleted and set in, then undo the actions"
    
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
            self.entryName        = clsTestService.addGuidToString("Editor Undo functionality", self.testNum)
            self.entryNameClipped = "Clip of " + self.entryName
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 2: Going to navigate to " + self.entryName + " entrie's KEA editor")  
            if self.common.kea.launchKEA(self.entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to " + self.entryName + "entrie's KEA editor") 
                return        
 
            writeToLog("INFO","Step 3: Going to delete " + self.entryName + " entrie's 00:05 to 00:10 interval")  
            if self.common.kea.editorTimelineActions("00:05", '00:10', True, enums.KeaEditorTimelineOptions.DELETE) == False:
                writeToLog("INFO","Step 3: FAILED to delete " + self.entryName + " entrie's 00:05 to 00:10 interval") 
                return
            
            writeToLog("INFO","Step 4: Going to split " + self.entryName + " entrie's section from second 00:15")  
            if self.common.kea.editorTimelineActions("00:15", '', True, enums.KeaEditorTimelineOptions.SPLIT) == False:
                writeToLog("INFO","Step 4: FAILED to split " + self.entryName + " entrie's section from second 00:15")   
                return            

            writeToLog("INFO","Step 5: Going to Set In " + self.entryName + " entrie's section from second 00:15 to 00:25")  
            if self.common.kea.editorTimelineActions("00:25", '', True, enums.KeaEditorTimelineOptions.SET_IN) == False:
                writeToLog("INFO","Step 5: Going to Set In " + self.entryName + " entrie's section from second 00:15 to 00:25")  
                return
            
            writeToLog("INFO","Step 6: Going to use the Undo option in order to undo a Set In action")  
            if self.common.kea.timeLineUndoRedoReset(enums.KeaEditorTimelineOptions.UNDO) == False:
                writeToLog("INFO","Step 6: FAILED to use the Undo option in order to undo a Set In action")  
                return
            
            writeToLog("INFO","Step 7: Going to use the Undo option in order to undo a Split action")  
            if self.common.kea.timeLineUndoRedoReset(enums.KeaEditorTimelineOptions.UNDO) == False:
                writeToLog("INFO","Step 7: FAILED to use the Undo option in order to undo a Split action")  
                return
            
            writeToLog("INFO","Step 8: Going to use the Undo option in order to undo a Delete action")  
            if self.common.kea.timeLineUndoRedoReset(enums.KeaEditorTimelineOptions.UNDO) == False:
                writeToLog("INFO","Step 8: FAILED to use the Undo option in order to undo a Delete action")  
                return
            
            writeToLog("INFO","Step 9: Going to save the KEA Editor Timeline section for " + self.entryName + " entry")
            if self.common.kea.saveEditorChanges(True)== False:
                writeToLog("INFO","Step 9: FAILED to save the KEA Editor Timeline section for " + self.entryName + " entry")
                return
            
            writeToLog("INFO","Step 10: Going to compare the time length of the entry from KEA Editor and Entry Page for " + self.entryNameClipped + " entry")
            if self.common.kea.compareEntryDurationInKeaAndEntryPage(self.entryNameClipped, '00:30')== False:
                writeToLog("INFO","Step 10: FAILED to compare the time length of the entry from KEA Editor and Entry Page for " + self.entryNameClipped + " entry")
                return 
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED for an " + self.testType)            
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.entryNameClipped])
            writeToLog("INFO","**************** Ended: teardown_method *******************")  
        except:
            pass       
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')