import pytest
import sys,os
from test.test_bigmem import ListTest
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','lib')))
from utilityTestFunc import *
from clsPractiTest import clsPractiTest
import clsTestService

class Test:
    
    #=============================================================================================================
    #This is the test that does setup
    #=============================================================================================================
    
    practiTest = clsPractiTest()
    testNum     = "0001"
    status      = "Pass"   
#     csvPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','EE_export_auto.csv'))
    csvPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','kms','EE_export_manual.csv'))
    # Filter ID of regression test sets: 373033
    ptFilterId = '373033'
    # Field ID of Automation EE: '---f-38303'
#     ptFieldId = '---f-38303'
    # Field ID of Manual EE: '---f-38302'
    ptFieldId = '---f-38302'
    def test_01(self,env):
        
        os.environ["RUNNING_TEST_ID"] = self.testNum 
        
        try:
            self.startTime = time.time() 
            writeToLog("INFO","************************************************************************************************************************")
            writeToLog("INFO","Start setup test test_0001")            
            
            # Get all test sets by filter - Will get the regression test sets
            listTestSet = self.practiTest.getPractiTestTestSetByFilterId(self.ptFilterId)
            # Loop over all test sets and sync with CSV file
            for testSet in listTestSet:
                self.practiTest.syncTestSetData(testSet, self.csvPath, self.ptFieldId)
         
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
                
    def teardown_method(self,method):
        duration = str(round(time.time() - self.startTime))
        assert (self.status == "Pass")   
        
    pytest.main('test_' + testNum  + '.py --tb=line')
         
