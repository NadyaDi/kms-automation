from asyncio.tasks import sleep
import csv, pytest, os.path, sys, uuid, datetime, time
import importlib
from timeit import Timer

from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles import colors
from selenium import webdriver

from base import Base
from clsBrowserMobCapture import clsBrowserMobCapture
import clsCommon
from clsPractiTest import clsPractiTest
from localSettings import *
import localSettings
from logger import *
import utilityTestFunc


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
    test, capture, driver = initialize(test, driverFix, duration)
    # Login
    common = clsCommon.Common(test.driver)
    if common.loginAsUser() == True:
        writeToLog("INFO","Logged in successfully as User")
    else:
        writeToLog("INFO","Driver created, but unable to login")
        raise Exception("Driver created, but unable to login")
    return (test, capture, driver)

#===============================================================================
# Load the driver
#===============================================================================
def initialize(test,driverFix,duration=60):
    clearFilesFromLogFolderPath('.png')
    #setup the test, initialize self and capture
    test,capture = basicSetUp(test,driverFix,duration) #we set the timeout for each interval (video playing until the end) to be 35 (expect 30 sec video)
    #write to log we started the test
    driver = initializeDriver(test,driverFix)
    return (test, capture, driver)        
    
#host and hostBrowser are optional.
#if we want to run the tests locally the default browser is firefox, we can give a different browser value. 
#if we don't want to run the functions locally then host contains the host address and hostBrowser contains the requested browser.    
def testWebDriverLocalOrRemote (hostBrowser,myProxy=None):
    if(LOCAL_SETTINGS_RUN_MDOE == LOCAL_RUN_MODE):
        if(hostBrowser == PC_BROWSER_FIREFOX):
            if (myProxy != None): 
                PROXY_HOST = myProxy.proxy[:myProxy.proxy.index(":")]
                PROXY_PORT = myProxy.proxy[myProxy.proxy.index(":")+1:]                  
                fp = webdriver.FirefoxProfile()
                fp.set_preference("plugin.state.npctrl", 2)
                fp.set_preference("network.proxy.type", 1)
                fp.set_preference("network.proxy.http",PROXY_HOST)
                fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
                fp.set_preference("network.proxy.https",PROXY_HOST)
                fp.set_preference("network.proxy.https_port",int(PROXY_PORT))
                fp.set_preference("network.proxy.ssl",PROXY_HOST)
                fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))  
                fp.set_preference("network.proxy.ftp",PROXY_HOST)
                fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))   
                fp.set_preference("network.proxy.socks",PROXY_HOST)
                fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))   
                fp.update_preferences()
                return webdriver.Firefox(firefox_profile=fp)
            else:
                return webdriver.Firefox()
        elif(hostBrowser == PC_BROWSER_CHROME):
            if (myProxy != None): 
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--proxy-server=http://' + myProxy.proxy)
                return webdriver.Chrome(LOCAL_SETTINGS_WEBDRIVER_LOCAL_CHROME_PATH,chrome_options=chrome_options)
            else:
                return webdriver.Chrome(LOCAL_SETTINGS_WEBDRIVER_LOCAL_CHROME_PATH)
        elif(hostBrowser == PC_BROWSER_IE):
            return webdriver.Ie(LOCAL_SETTINGS_WEBDRIVER_LOCAL_IE_PATH,capabilities={'ignoreZoomSetting':True,"nativeEvents": False,"unexpectedAlertBehaviour": "accept","ignoreProtectedModeSettings": True,"disable-popup-blocking": True,"enablePersistentHover": True})
        elif (hostBrowser == ANDROID_CHROME):
            capabilities = {
                'chromeOptions': {
                'androidPackage': 'com.android.chrome',
                }
            }
            driver = webdriver.Remote('http://localhost:9515', capabilities)
            return driver 
    else: #remote, capture traffic using proxy
        if (myProxy != None):
            if (localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_IE):
                return webdriver.Remote(command_executor=LOCAL_SETTINGS_SELENIUM_HUB_URL,proxy=myProxy, desired_capabilities={'unexpectedAlertBehaviour':'accept', 'browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,'ignoreZoomSetting':True,"nativeEvents": False,"unexpectedAlertBehaviour": "accept","ignoreProtectedModeSettings": True,"disable-popup-blocking": True,"enablePersistentHover": True,"applicationName": LOCAL_SETTINGS_SELENIUM_GRID_POOL})
            elif (localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_CHROME or localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_FIREFOX):
                return webdriver.Remote(command_executor=LOCAL_SETTINGS_SELENIUM_HUB_URL,proxy=myProxy, desired_capabilities={'browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,"applicationName": LOCAL_SETTINGS_SELENIUM_GRID_POOL})
        else:
            if (localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_IE):
                return webdriver.Remote(command_executor=LOCAL_SETTINGS_SELENIUM_HUB_URL,desired_capabilities={'unexpectedAlertBehaviour':'accept','browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,'ignoreZoomSetting':True,"nativeEvents": False,"unexpectedAlertBehaviour": "accept","ignoreProtectedModeSettings": True,"disable-popup-blocking": True,"enablePersistentHover": True,"applicationName": LOCAL_SETTINGS_SELENIUM_GRID_POOL})
            elif(localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_FIREFOX):
                return webdriver.Remote(command_executor=LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'browserName': hostBrowser.split("_")[1], 'requireWindowFocus':True, 'applicationName': LOCAL_SETTINGS_SELENIUM_GRID_POOL})

            elif(localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_CHROME):
                return webdriver.Remote(command_executor=LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'setNoProxy': '' , 'browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,"applicationName": LOCAL_SETTINGS_SELENIUM_GRID_POOL})

#the function checks if a time out happened and writes it to the log  
def testTimedOut(testNum, startTime,reason):
    if((time.time() - startTime) > TEST_TIMEOUT): # timer is set to each test differently
            writeToLog("INFO","test_" + testNum + " Timed-out. " + reason)
            return True
    return False    

# Get from testPartners scv the test credentials by test id and env
def updatePlatforms(test_num):
    
    env = ""
    for arg in sys.argv[1:]:
        if "--env" in arg:
            env = arg[6:]
            
    supported_platforms=[]
    case_str = "test_" + test_num
    matrixPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testSet' + env +  '.csv'))
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
                
        # Update localSetting partner details(base URL, credentials, Practitest ID
        if updateTestCredentials(case_str) == False:
            writeToLog("INFO","Unable to find credentials for test: '" + case_str + "'")
            raise Exception("Unable to find credentials for test")
    return supported_platforms        

    
# Read from testPartners csv the test details(base URL, credentials, Practitest ID       
def updateTestCredentials(case_str):    
    found = False
    if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
        newuiStr = "NewUI"
    else:
        newuiStr = ""
    testPartnersPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testPartners' + localSettings.LOCAL_SETTINGS_RUN_ENVIRONMENT + newuiStr + '.csv'))
    with open(testPartnersPath, 'r') as csv_mat: #windows
        testPartners = csv.DictReader(csv_mat)
        for row in testPartners:
            if (row['case'] == case_str):
                # SET PARTNER DETAILS
                localSettings.LOCAL_SETTINGS_PARTNER            = row['partner']
                localSettings.LOCAL_SETTINGS_LOGIN_USERNAME     = row['login_username']
                localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD     = row['login_password']
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME     = row['admin_username']
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD     = row['admin_password']
                
                # SET KMS URLS
                localSettings.LOCAL_SETTINGS_TEST_BASE_URL         = localSettings.LOCAL_SETTINGS_URL_PREFIX + row['partner'] + '.' + row['base_url']
                localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL         = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/user/login'
                localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL      = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media'
                localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL   = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-channels'              
                found = True
    return found          
#===============================================================================
# function to setup the following things:
#  - capture traffic object
#  - create client proxy
#  - initialize driver and specific log
#  - test url and status 
#  - max running time until timeout, we ass +- 1 min more then avg result 
#===============================================================================
def basicSetUp(test,driverFix,estimatedDuration=600):
    capture  = None
    test.myProxy = None
    test.TEST_TIMEOUT = estimatedDuration
    localSettings.LOCAL_RUNNING_BROWSER = driverFix
    localSettings.LOCAL_SETTINGS_GUID = str(uuid.uuid4())[:8].upper()
    
    if (test.enableProxy == True):
        try:
            capture = clsBrowserMobCapture(test.testNum,driverFix)
            for attempt in range(2):
                if (localSettings.LOCAL_RUNNING_BROWSER == ANDROID_CHROME):
                    proxyUrl = LOCAL_SETTINGS_BROWSER_PROXY_MOBILES
                else:
                    proxyUrl = LOCAL_SETTINGS_BROWSER_PROXY
                try:
                    test.myProxy = capture.createProxyClient(proxyUrl)
                    break
                except Exception as inst:
                    if (localSettings.LOCAL_RUNNING_BROWSER == ANDROID_CHROME):
                        capture.shutDownProxy(LOCAL_SETTINGS_BROWSER_PROXY_MOBILES, LOCAL_SETTINGS_BROWSER_PROXY_MOBILES_PORT)
            else:
                if (test.myProxy is None):
                    writeToLog("INFO","Unable to create proxy object")
                    raise Exception("Unable to create proxy object")
            test.driver = testWebDriverLocalOrRemote(driverFix,test.myProxy)
            test.myProxy.new_har("externalTests",{"captureHeaders":True, "captureContent":True})
        except Exception as inst:
            handleException (test,inst,test.startTime)
            raise
    else:
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
    return test,capture                 

#===========================================================================================
# the function handles exception inst, mark the test as fail and writes the error in the log 
#===========================================================================================
def handleException(test,inst,startTime):
    
    log_exception(inst)
    
    test.status = "Fail"
    return test.status

#===============================================================================
# the function tears down the driver and the proxy. if a debug column was given we update the test resul in results matrix
#===============================================================================
def basicTearDown(test):
    
    practiTest = clsPractiTest()
    
    try:
        if (test.driver != None):
            #if (test.status == "Fail"): TODO: OLEG take last screenshot if failed 
            #    createScreenshot(test)
            test.driver.quit()
            writeToLog("DEBUG", "tearDown: closed web driver")
        if (test.myProxy != None):
            test.myProxy.close()
            if (LOCAL_SETTINGS_RUN_MDOE == LOCAL_RUN_MODE):
                disableLocalSystemProxyViaRegistry()
            else:
                pass
                #disableRemoteSystemProxyViaRegistry()
        if (isAutomationEnv() == True):
            practiTest.setPractitestInstanceTestResults(test.status,str(test.testNum))            
        writeToLog("DEBUG", "Finished tearDown function")
    except Exception as inst:
            test.status = handleException(test,inst,test.startTime)

#===============================================================================
# the function that returns true if the environment variable env is set to Auto 
#===============================================================================   
    
def isAutomationEnv():
        
        env = ""
        
        for arg in sys.argv[1:]:
            if ("--env" in arg):
                env = arg[6:]
                break
        if (env == "Auto"):
            return True
        else:
            return False
        
#===============================================================================
# the function that disables system proxy via windows registry
#===============================================================================

def disableLocalSystemProxyViaRegistry(self):
    
    import winreg
    
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.SetValueEx(key, "ProxyHttp1.1", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

#===============================================================================
# the function takes a screenshot of the test at the end of it, and save it
#===============================================================================
def createScreenshot(test):
    LOG_FOLDER_PREFIX = ""
    if (os.getenv('BUILD_ID',"") != ""):
        LOG_FOLDER_PREFIX = '/' + os.getenv('BUILD_ID',"") + '/'
    runningTestNum = os.getenv('RUNNING_TEST_ID',"")
    if (runningTestNum != ""):
        LOG_FOLDER_PREFIX = LOG_FOLDER_PREFIX + "/" + runningTestNum + "/" 
    pngPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','logs' + LOG_FOLDER_PREFIX,runningTestNum + "_" + localSettings.LOCAL_RUNNING_BROWSER + '.png'))
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
        #alert = driver.switch_to_alert()
        #alert.accept();
        #driver.maximize_window()
        raise
    return driver


# Delete old filed from the log folder
# fileType - Exmaple: '.png'
def clearFilesFromLogFolderPath(fileType):
    path = getLogFileFolderPath()
    filelist = [ f for f in os.listdir(path) if f.endswith(fileType) ]
    for f in filelist:
        os.remove(os.path.join(path, f))
        
        
def addGuidToString(value):
    return localSettings.LOCAL_SETTINGS_GUID + '_' + value        