from asyncio.tasks import sleep
import csv, pytest, os.path, sys, uuid, datetime, time
import importlib
from timeit import Timer

from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles import colors
from selenium import webdriver

from base import Base
import clsCommon
from clsPractiTest import clsPractiTest
from localSettings import *
import localSettings
from logger import *
import utilityTestFunc
import shutil
import glob, os



#===========================================================================
#the class contains basic test functions and macros. 
#driver and logs initialization, timeout handlers. 
#check supported browsers to run on, update final results matrix.
#===========================================================================
WEB_DRIVER                      = None
LOGIN = None
PC_BROWSER_IE                   = "pc_internet explorer"
PC_BROWSER_CHROME               = "pc_chrome"
PC_BROWSER_FIREFOX              = "pc_firefox"
MAC_BROWSER_SAFARI              = "mac_Safari"    
ANDROID_CHROME                  = "android_chrome"   
IMPLICITLY_WAIT_TIME_TO_WAIT    = 30
TEST_TIMEOUT                    = 60 
    
    
#===============================================================================
# function with all the redundant start functions 
#===============================================================================
def initializeAndLoginAsUser(test, driverFix, duration=60):
    test, driver = initialize(test, driverFix, duration)
    # Login
    common = clsCommon.Common(test.driver)
    if common.loginAsUser() == True:
        writeToLog("INFO","Logged in successfully as User")
    else:
        writeToLog("INFO","Driver created, but unable to login")
        raise Exception("Driver created, but unable to login")
    return (test, driver)


#===============================================================================
# Load the driver
#===============================================================================
def initialize(test,driverFix,duration=60):
    if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.LOCAL_RUN_MODE:
        cleanTempQrCodeFolder()
    # Setup the test, initialize
    test = basicSetUp(test,driverFix,duration) #we set the timeout for each interval (video playing until the end) to be 35 (expect 30 sec video)
    # Start driver - Open browser and navigate to base URL
    driver = initializeDriver(test,driverFix)
    return (test, driver)    
    
    
#host and hostBrowser are optional.
#if we want to run the tests locally the default browser is firefox, we can give a different browser value. 
#if we don't want to run the functions locally then host contains the host address and hostBrowser contains the requested browser.    
def testWebDriverLocalOrRemote (hostBrowser,myProxy=None):
    if(hostBrowser == PC_BROWSER_FIREFOX):
        # This code for Firefox browser profile (remote and local)
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2) # custom location
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mpeg,video/avi,video/MP2T,video/3gpp,' +
                            'video/quicktime,video/x-msvideo,video/x-flv,video/mp4,application/x-mpegURL,video/x-ms-wmv,' +
                            'video/x-ms-asf,image/bmp,image/x-png,image/gif,audio/wav,image/png,image/jpg,audio/x-ms-wma,application/vnd.ms-asf')
        fp.update_preferences()
        
    elif(hostBrowser == PC_BROWSER_CHROME):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS,
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True}    
        chromeOptions.add_experimental_option('prefs', prefs)  
    
    
    if(LOCAL_SETTINGS_RUN_MDOE == LOCAL_RUN_MODE):
        if(hostBrowser == PC_BROWSER_FIREFOX):
            return webdriver.Firefox(firefox_profile=fp)
        elif(hostBrowser == PC_BROWSER_CHROME):
            return webdriver.Chrome(executable_path=localSettings.LOCAL_SETTINGS_WEBDRIVER_LOCAL_CHROME_PATH, chrome_options=chromeOptions)
        elif(hostBrowser == PC_BROWSER_IE):
            return webdriver.Ie(localSettings.LOCAL_SETTINGS_WEBDRIVER_LOCAL_IE_PATH,capabilities={'ignoreZoomSetting':True,"nativeEvents": False,"unexpectedAlertBehaviour": "accept","ignoreProtectedModeSettings": True,"disable-popup-blocking": True,"enablePersistentHover": True})
        elif (hostBrowser == ANDROID_CHROME):
            capabilities = {
                'chromeOptions': {
                'androidPackage': 'com.android.chrome',
                }
            }
            driver = webdriver.Remote('http://localhost:9515', capabilities)
            return driver 
    else: #Remote
        if (localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_IE):
            return webdriver.Remote(command_executor=localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL,desired_capabilities={'unexpectedAlertBehaviour':'accept','browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,'ignoreZoomSetting':True,"nativeEvents": False,"unexpectedAlertBehaviour": "accept","ignoreProtectedModeSettings": True,"disable-popup-blocking": True,"enablePersistentHover": True,"applicationName": LOCAL_SETTINGS_SELENIUM_GRID_POOL})
        elif(localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_FIREFOX):
            return webdriver.Remote(browser_profile=fp,command_executor=localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'marionette:False','browserName': hostBrowser.split("_")[1], 'requireWindowFocus':True, 'applicationName': localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL})
        elif(localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_CHROME):
            return webdriver.Remote(command_executor=localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'setNoProxy': '' , 'browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,"applicationName": localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL},options=chromeOptions)


# The function checks if a time out happened and writes it to the log  
def testTimedOut(testNum, startTime,reason):
    if((time.time() - startTime) > TEST_TIMEOUT): # timer is set to each test differently
            writeToLog("INFO","test_" + testNum + " Timed-out. " + reason)
            return True
    return False    


# Get from testPartners scv the test credentials by test id and env
def updatePlatforms(test_num):
    env = ""
    if isAutomationEnv() == True:
        env = "Auto"
    
    supported_platforms=[]
    case_str = "test_" + test_num
    matrixPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSet' + env +  '.csv'))
    with open(matrixPath, 'r') as csv_mat: #windows
        platform_matrix = csv.DictReader(csv_mat)
        for row in platform_matrix:
            if (row['case'] == case_str):
                if (row['pc_firefox']=='1'):
                    supported_platforms.append(pytest.mark.ff('pc_firefox'))
                if (row['pc_chrome']=='1'):
                    supported_platforms.append(pytest.mark.ch('pc_chrome'))
                if (row['pc_internet explorer']=='1'):
                    supported_platforms.append(pytest.mark.ie('pc_internet explorer'))    
                if (row['android_chrome']=='1'):
                    supported_platforms.append(pytest.mark.ie('android_chrome'))
                    
                if env == 'Auto': #If running from PractiTests (Trigger from Jenkins)
                    # Set the node hostname to run
                    localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL = row['hostname']
                    
                    # Set the environment
                    env = row['environment']
                    if 'Testing' in env:
                        # Update the localSetting run with running environment (prod/test)
                        localSettings.LOCAL_SETTINGS_RUN_ENVIRONMENT = localSettings.LOCAL_SETTINGS_TESTING_ENVIRONMENT
                    elif 'Prod' in env:
                        localSettings.LOCAL_SETTINGS_RUN_ENVIRONMENT = localSettings.LOCAL_SETTINGS_PROD_ENVIRONMENT
                    else:
                        writeToLog("INFO","Unable to define environment: '" + env + "'")
                        
                    if 'NewUI' in env:
                        localSettings.LOCAL_SETTINGS_IS_NEW_UI = True
                    else:
                        localSettings.LOCAL_SETTINGS_IS_NEW_UI = False
    return supported_platforms        


#===============================================================================
# function to setup the following things:
#  - initialize driver and specific log
#  - test url and status 
#  - max running time until timeout, we ass +- 1 min more then avg result 
#===============================================================================
def basicSetUp(test,driverFix,estimatedDuration=600):
    test.TEST_TIMEOUT = estimatedDuration
    localSettings.LOCAL_RUNNING_BROWSER = driverFix
    localSettings.LOCAL_SETTINGS_GUID = str(uuid.uuid4())[:8].upper()
    
    # Set auto download path
    # If you need a shared folder between the win node and Jenkins node, create a folder in your test: localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS
    localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD = '/mnt/auto_kms_py1/downloads/' + str(localSettings.LOCAL_SETTINGS_GUID)
    if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.LOCAL_RUN_MODE:
        localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS           = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'temp', 'downloads'))
    else:
        localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS           = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'temp','downloads'))
    
    if isAutomationEnv() == True:
        # Z:\\ - Is shared folder on il-AutoKmsJenkinsNode-qa.dev.kaltura.com/mnt/auto_kms_py1/downloads/
        localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS           = 'Z:\\' + str(localSettings.LOCAL_SETTINGS_GUID)

    test.driver = testWebDriverLocalOrRemote(driverFix)        
        
    if ("version" in test.driver.capabilities):
        test.browserVersion = test.driver.capabilities['version']
    else:
        test.browserVersion = test.driver.capabilities['browserVersion']
    test.browserName = test.driver.capabilities['browserName']
    writeToLog("INFO","Browser " + test.driver.capabilities['browserName'] + " version is: " + test.browserVersion)
    test.driver.implicitly_wait(IMPLICITLY_WAIT_TIME_TO_WAIT)
    
    test.base_url = localSettings.LOCAL_SETTINGS_TEST_BASE_URL
    test.verificationErrors = []    
    test.status = "Pass"
    test.timeout_accured = "False"
    return test                 


#===========================================================================================
# the function handles exception inst, mark the test as fail and writes the error in the log 
#===========================================================================================
def handleException(test, inst, startTime=''):
    log_exception(inst)
    #createScreenshot(test, 'EXCEPTION') #20-08-18, Not sure need this, because we have screenshot in tearDown method
    test.status = "Fail"
    return test.status


#===============================================================================
# the function tears down the driver and the proxy. if a debug column was given we update the test resul in results matrix
#===============================================================================
def basicTearDown(test):
    practiTest = clsPractiTest()
    try:
        if (test.driver != None):
            test.driver.quit()
            writeToLog("INFO", "tearDown: closed web driver")
        if (isAutomationEnv() == True):
            practiTest.setPractitestInstanceTestResults(test.status,str(test.testNum))            
        writeToLog("INFO", "Finished tearDown function")
    except Exception as inst:
            test.status = handleException(test,inst,test.startTime)


#===============================================================================
# the function that returns true if the environment variable env is set to Auto 
#===============================================================================   
def isAutomationEnv():
        if os.getenv('ENV_AUTO') == 'Auto':
            return True
        else:
            return False
        
        
#===============================================================================
# the function takes a screenshot of the test at the end of it, and save it
#===============================================================================
def createScreenshot(test, scName=''):
    if scName != '':
        scName = '_' + scName
    runningTestNum = os.getenv('RUNNING_TEST_ID',"")
    if (runningTestNum != ""):
        pngPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'logs', runningTestNum, scName + '.png'))
    if test.driver != None:
        test.driver.save_screenshot(pngPath)          

    
def initializeDriver(test, driverFix):
    writeToLog("INFO","initialize driver " + driverFix)
    driver = test.driver
    driver.implicitly_wait(localSettings.LOCAL_SETTINGS_IMPLICITLY_WAIT)
    driver.get(test.base_url)
    utilityTestFunc.wait_for_page_readyState(driver)
    try:
        if (driverFix != ANDROID_CHROME):
            driver.maximize_window()
    except Exception as inst:
        raise
    return driver

        
def cleanTempDownloadFolder():
    folder = os.path.join(localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS, '')
    return cleanFolder(folder)
    
    
def cleanTempQrCodeFolder():
    folder = os.path.join(localSettings.LOCAL_QRCODE_TEMP_DIR, '')
    return cleanFolder(folder)
               
               
def cleanFolder(folderPath):
    for the_file in os.listdir(folderPath):
        file_path = os.path.join(folderPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
            return False
            
    return True


def addGuidToString(value, testID="", delimiter="-"):
    if testID=="":
        return localSettings.LOCAL_SETTINGS_GUID + delimiter + value
    else:
        return localSettings.LOCAL_SETTINGS_GUID + delimiter + testID + delimiter + value     
