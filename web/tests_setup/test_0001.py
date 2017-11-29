import time, pytest, sys,os
from logger import *
from utilityTestFunc import *
from clsBackendAPI import clsBackendAPI

sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','..','lib')))

class Test:
    
    #=============================================================================================================
    #This is the test that does setup
    #=============================================================================================================
    
    practiTest = clsPractiTest()
    testService = clsTestService()
    testNum     = "0001"
    status      = "Pass"   
    
    def updatePlayerVersion(self,env):
 
        try:
        
            self.startTime = time.time() 
            writeToLog("INFO","************************************************************************************************************************")
            writeToLog("INFO","Start setup test test_0001")                  
            
            playerSettings = self.testService.loadPlayerSettings(env)
            myBackend = clsBackendAPI()
            ks = myBackend.getKS()
            if (ks != False):
                if (myBackend.updateUIConfhtml5Url(ks,playerSettings.DEFAULT_PLAYER_LIST,LOCAL_SETTINGS_TESTED_RELEASE) != True):
                    self.status = "Fail"
         
        except Exception as inst:
            self.status = self.testService.handleException(self,inst,self.startTime) 
    
    def test_01(self,env):
        
        os.environ["RUNNING_TEST_ID"] = self.testNum 
        
        self.startTime = time.time()
        self.updatePlayerVersion(env)
                
    def teardown_method(self,method):
        
        duration = str(round(time.time() - self.startTime))
        writeToLog("INFO","test_" + self.testNum + ": " + self.status + " (" + duration + " sec)")
        assert (self.status == "Pass")   
        
    pytest.main('test_' + testNum  + '.py --tb=line')
         
