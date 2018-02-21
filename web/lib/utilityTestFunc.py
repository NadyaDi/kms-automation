import csv
from datetime import timedelta
import subprocess
from time import sleep

import requests
from selenium.webdriver.common.action_chains import ActionChains

from logger import *


# Read from testPartners csv the test details(base URL, credentials, Practitest ID       
def updateTestCredentials(case_str):    
    found = False
    if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
        newuiStr = "NewUI"
    else:
        newuiStr = ""
    testPartnersPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testPartners' + localSettings.LOCAL_SETTINGS_RUN_ENVIRONMENT + newuiStr + '.csv'))
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
                localSettings.LOCAL_SETTINGS_TEST_BASE_URL          = localSettings.LOCAL_SETTINGS_URL_PREFIX + row['partner'] + '.' + row['base_url']
                localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL          = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/user/login'
                localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL       = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media'
                localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL   = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-playlists'
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL          = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/admin'
                localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL    = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-channels'  
                localSettings.LOCAL_SETTINGS_KMS_MY_HISTORY_URL     = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/history'
                localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL       = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/channels'   
                found = True
                break
    return found 

#===============================================================================
#Take screenshoot of whole screen.
#'fullpath' should contain the file name with its extension PNG!
#===============================================================================
def saveScreenshotToFile(driver, fullPath):
    screenShotPath=os.path.abspath(fullPath)
    return driver.save_screenshot(screenShotPath)

#===============================================================================
# the function that disables system proxy via connectionto helper service
#===============================================================================

def disableRemoteSystemProxyViaRegistry():
    
    try:
        r = requests.get('http://52.16.122.203:8080/resetMachineProxy')
    except Exception as inst:
        raise Exception("Failed to disable proxy on remote player machine")
    
    if (r.status_code != 200):
        raise Exception("Failed to disable proxy on remote player machine")

#===============================================================================
# Press given key
#===============================================================================
def keyPress(test, key):
    ActionChains(test.driver).send_keys(key).perform()

#===============================================================================
# Press multiple time given key
#===============================================================================
def multipleKeyPress(test, key, count):
    for i in range(count):
        keyPress(test, key)
        time.sleep(0.5)

#===============================================================================
# Convert time to secods.
# Example "0:04:15" would produce an output of 255; "0:00:25" would produce an output of 25
#===============================================================================        
def convertTimeToSecondsHMMSS(test, s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

#===============================================================================
# Convert time to secods.
# Example "0:15" would produce an output of 15; "1:25" would produce an output of 85
#===============================================================================        
def convertTimeToSecondsMSS(s):
    l = s.split(':')
    return int(int(l[0]) * 60 + int(l[1]))

def getTimerInSeconds(driver, player):
    timerEl = player.getCurrentTimeElement(driver)
    timerText = timerEl.text
    return convertTimeToSecondsMSS(timerText)

#===============================================================================
# Generate timestamp DDmmYYHHMMSS
#===============================================================================        
def generateTimeStamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y%H%M%S')

#===============================================================================
# Run any shell command
#=============================================================================== 
def runProcess(self, exe):    
    proc = subprocess.Popen(exe, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    if output != "":
        return output
    else:
        return

#===============================================================================
# Return the HTTP response code as integer
#=============================================================================== 
def getUrlResponseCode(url):    
    try:
        return requests.head(url).status_code
    except requests.ConnectionError:
        writeToLog("DEBUG","failed to connect")
        return None   

#===============================================================================
# Return true if the URL response code is 200 (OK)
#=============================================================================== 
def isUrlResponse200(url):    
    if getUrlResponseCode(url) == 200:
        return True
    else:
        return False
    
def wait_for_page_readyState(driver, timeout=30):
    i = 0
    page_state = ''
    while i != timeout and page_state != 'complete':
        page_state = driver.execute_script('return document.readyState;')
        sleep(1)
        i += 1
    if page_state == 'complete':
        return True
    else:
        return False   

def isAutoEnvironment():
    env = ""   
    for arg in sys.argv[1:]:
        if ("--env" in arg):
            env = arg[6:]
            break
    if (env == "Auto"):
        return True
    
    return False