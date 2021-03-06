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
from time import sleep
from selenium.webdriver.remote.file_detector import FileDetector



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
    # Handle case when unable to find credentials for test
    if localSettings.LOCAL_SETTINGS_LOGIN_USERNAME == '':
        test.status = 'Fail'
        raise Exception("Unable to find credentials for test: '" + test.testNum + "'")
    
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
        fp.set_preference('browser.helperApps.alwaysAsk.force', False)
        fp.set_preference('pdfjs.disabled', True)
        fp.set_preference('plugin.scan.plid.all;true', False)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/x-download,application/pdf,video/mpeg,video/avi,video/MP2T,video/3gpp,' +
                            'video/quicktime,video/x-msvideo,video/x-flv,video/mp4,application/x-mpegURL,video/x-ms-wmv,' +
                            'video/x-ms-asf,image/bmp,image/x-png,image/gif,audio/wav,image/png,image/jpg,audio/x-ms-wma,application/vnd.ms-asf')
        fp.update_preferences()
        
    elif(hostBrowser == PC_BROWSER_CHROME):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS,
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True,
                 "profile.default_content_setting_values.media_stream_mic": 1, 
                 "profile.default_content_setting_values.media_stream_camera": 1,
                 "profile.default_content_setting_values.geolocation": 1, 
                 "profile.default_content_setting_values.notifications": 1}
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
            # Due to unknown Webdriver issue, implementing workaround: add try-except with retries loop
            retries = localSettings.LOCAL_SETTINGS_WEBDRIVER_START_FF_RETRIES
            for i in range(retries):
                try:
                    if i > 0:
                        writeToLog("INFO","WARNING: Webdriver issue, can't start Firefox after " + str(i) + " retries of " + str(retries) + ". Going to try again...")
                    # Convert path for Windows
                    return webdriver.Remote(browser_profile=fp,command_executor=localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'browserName': hostBrowser.split("_")[1], 'requireWindowFocus':True, 'applicationName': localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL, 'acceptInsecureCerts': True})
                except Exception:
                    writeToLog("INFO","FAILED to start Firefox, retry number " + str(i))
                    writeToLog("INFO","Going to wait 5 seconds and try again")
                    sleep(5)                    
                    pass
        elif(localSettings.LOCAL_RUNNING_BROWSER == PC_BROWSER_CHROME):
            return webdriver.Remote(command_executor=localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL, desired_capabilities={'setNoProxy': '' , 'browserName': hostBrowser.split("_")[1],'requireWindowFocus':True,"applicationName": localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL},options=chromeOptions)


# The function checks if a time out happened and writes it to the log  
def testTimedOut(testNum, startTime,reason):
    if((time.time() - startTime) > TEST_TIMEOUT): # timer is set to each test differently
            writeToLog("INFO","test_" + testNum + " Timed-out. " + reason)
            return True
    return False    


# Get from testPartners scv the test credentials by test id and env
def updatePlatforms(test_num, application=enums.Application.MEDIA_SPACE):
    env = ""
    if isAutomationEnv() == True:
        env = "Auto"
    
    supported_platforms=[]
    case_str = "test_" + test_num
    if application==enums.Application.PITCH:
        matrixPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','pitch','testSet' + env +  '.csv'))
    else:
        matrixPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','kms','testSet' + env +  '.csv'))
        
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
                    localSettings.LOCAL_SETTINGS_ENV_NAME = env    
                    writeToLog("INFO","Going to test: '" + env + "' environment")
                        
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
        # Z:\\ - Is shared folder on il-autojenkins-qa.dev.kaltura.com/mnt/auto_kms_py1/downloads/
        localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS           = 'Z:\\' + str(localSettings.LOCAL_SETTINGS_GUID)

        # Create temp folder and dummy file
        try:     
            os.makedirs(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
            writeToLog("INFO","Created folder: " + localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
                        
            with open(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + "/" + str(test.testNum) + "-dummy.txt", "w") as file:
                file.write("This is dummy file inside temp download folder for test ID: " + str(test.testNum))            
        except:
            writeToLog("INFO","FAILED to create folder: " + localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
    
    # Set Selenium HUB (Grid) URL
    localSettings.LOCAL_SETTINGS_SELENIUM_HUB_URL = getSeleniumHubURL(localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)
    test.driver = testWebDriverLocalOrRemote(driverFix)        
        
    if ("version" in test.driver.capabilities):
        test.browserVersion = test.driver.capabilities['version']
    else:
        test.browserVersion = test.driver.capabilities['browserVersion']
    test.browserName = test.driver.capabilities['browserName']
    writeToLog("INFO","Browser " + test.driver.capabilities['browserName'] + " version is: " + test.browserVersion)
    test.driver.implicitly_wait(IMPLICITLY_WAIT_TIME_TO_WAIT)
    test.base_url = localSettings.LOCAL_SETTINGS_TEST_BASE_URL
    return test                 


#===========================================================================================
# the function handles exception inst, mark the test as fail and writes the error in the log 
#===========================================================================================
def handleException(test, inst, startTime=''):
    log_exception(inst)
    test.status = "Fail"
    return test.status


#===============================================================================
# the function tears down the driver and the proxy. if a debug column was given we update the test resul in results matrix
#===============================================================================
def basicTearDown(test):
    practiTest = clsPractiTest()
    if isAutomationEnv() == True:
        # Delete temp folder
        try:     
            shutil.rmtree(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
            writeToLog("INFO","Deleted folder: " + localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
        except:
            writeToLog("INFO","FAILED to delete folder: " + localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
    
    try:
        if (test.driver != None):
            test.driver.quit()
            writeToLog("INFO", "tearDown: closed web driver")
    except Exception as inst:
            test.status = handleException(test,inst,test.startTime)
    
    try:                    
        if (isAutomationEnv() == True):
            if practiTest.setPractitestInstanceTestResults(test.status,str(test.testNum)) == False:
                writeToLog("INFO", "tearDown: FAILED report to PractiTest")
    except Exception as inst:
            writeToLog("INFO", "tearDown: FAILED report to PractiTest")


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
    try:
        driver = test.driver
        driver.implicitly_wait(localSettings.LOCAL_SETTINGS_IMPLICITLY_WAIT)
        driver.get(test.base_url)
        utilityTestFunc.wait_for_page_readyState(driver)
    except Exception as inst:
        raise Exception("Driver: FAILED to navigate to: " + str(test.base_url))        
    try:
        if (driverFix != ANDROID_CHROME):
            driver.maximize_window()
    except Exception as inst:
        raise Exception("Driver: FAILED to maximaize windows")
    
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


# Will return a Selenium HUB (Grid) URL according the mapping allocation per Windows Node
def getSeleniumHubURL(applicationName):
    switcher = {
        # il-KmsHub1-qa.dev.kaltura.com
        "qaKmsFrontEnd": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd2": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd3": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd4": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd5": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd6": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd7": "il-KmsHub1-qa.dev.kaltura.com",
        "qaKmsFrontEnd8": "il-KmsHub1-qa.dev.kaltura.com",
        # il-KmsHub2-qa.dev.kaltura.com
        "qaKmsFrontEnd9": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd10": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd11": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd12": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd13": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd14": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd15": "il-KmsHub2-qa.dev.kaltura.com",
        "qaKmsFrontEnd16": "il-KmsHub2-qa.dev.kaltura.com",
        # il-KmsHub3-qa.dev.kaltura.com
        "qaKmsFrontEnd17": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd18": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd19": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd20": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd21": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd22": "il-KmsHub3-qa.dev.kaltura.com",
        "qaKmsFrontEnd23": "il-KmsHub3-qa.dev.kaltura.com",
        # Pitch
        "PitchNode1": "il-KmsHub3-qa.dev.kaltura.com",
        "PitchNode2": "il-KmsHub3-qa.dev.kaltura.com"
    }
    return("http://" + switcher.get(applicationName, "Invalid Application Name of the windows node") + ":4444/wd/hub")    
    
    