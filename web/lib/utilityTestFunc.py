import codecs
import csv
from datetime import timedelta
import io
import subprocess
from time import sleep
import localSettings
import requests
from selenium.webdriver.common.action_chains import ActionChains

from logger import *


# Read from testPartners csv the test details(base URL, credentials, Practitest ID       
def updateTestCredentials(case_str):    
    found = False
    # SET PARTNER DETAILS
    localSettings.LOCAL_SETTINGS_PARTNER            = ''
    localSettings.LOCAL_SETTINGS_LOGIN_USERNAME     = ''
    localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD     = ''
    localSettings.LOCAL_SETTINGS_ADMIN_USERNAME     = ''
    localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD     = ''    
    testPartnersPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testPartners' + localSettings.LOCAL_SETTINGS_ENV_NAME + '.csv'))
    with codecs.open(testPartnersPath,'r',encoding='utf8') as csv_mat: #windows
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
                setTestURLs(row)
                found = True
                break
    return found 


def getPartnerDetails(partner):
    testPartnerDetailsPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','partnerDetails.csv'))
    with open(testPartnerDetailsPath, 'r') as csv_mat:
        partnerDetails = csv.DictReader(csv_mat)
        for row in partnerDetails:
            if (row['partnerId'] == partner):
                return row['serverUrl'], row['adminSecret']
    return None,None     


def setTestURLs(row):
    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MEDIA_SPACE:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_URL_PREFIX + row['partner'] + '.' + row['base_url']
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/user/login'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media'
        localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL       = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-playlists'
        localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/admin'
        localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL        = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-channels'  
        localSettings.LOCAL_SETTINGS_KMS_MY_HISTORY_URL         = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/history'
        localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/channels'   
        localSettings.LOCAL_SETTINGS_KMS_MEDIA_SELECTION_URL    = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/quiz/entry/add-quiz/context/'
        localSettings.LOCAL_SETTINGS_KMS_GALLERIES_URL          = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/esearch/search-galleries/?keyword=gallery'
    
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + ''
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/webapps/osv-kaltura-BBLEARN/jsp/myMediaLTI.jsp'
        localSettings.LOCAL_SETTINGS_GALLERIES_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1'
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/webapps/osv-kaltura-BBLEARN/jsp/courseGalleryLTI.jsp?url=/hosted/index/course-gallery&course_id=_51_1'
        localSettings.LOCAL_SETTINGS_SHARED_REPOSITORY_URL      = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/webapps/osv-kaltura-BBLEARN/jsp/sharedRepository.jsp'
        
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
        if localSettings.LOCAL_SETTINGS_ENV_NAME == 'ProdNewUI':
            localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_SHAREPOINT_BASE_URL_PRODUCTION
        elif localSettings.LOCAL_SETTINGS_ENV_NAME == 'TestingNewUI':
            localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_SHAREPOINT_BASE_URL_TESTING
            
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/Home.aspx'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/My%20Media.aspx' 
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/Media%20Gallery.aspx'  
        
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_MOODLE_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/login/index.php'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/local/mymedia/mymedia.php'
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/local/kalturamediagallery/index.php?courseid=10'
        localSettings.LOCAL_SETTINGS_SITE_BLOG_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/blog/index.php'
        localSettings.LOCAL_SETTINGS_COURSE_URL                 = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/course/view.php?id=10'
        localSettings.LOCAL_SETTINGS_COURSE_STUDENT_GRADES_URL  = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/grade/report/user/index.php?id=10'
        localSettings.LOCAL_SETTINGS_COURSE_ADMIN_GRADES_URL    = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/grade/report/grader/index.php?id=10'
  
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_CANVAS_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/login/canvas'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471'
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471'
        localSettings.LOCAL_SETTINGS_GALLERY_ANNOUNCEMENTS_URL  = (localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471/announcements')
        localSettings.LOCAL_SETTINGS_GALLERY_ASSIGNMENTSS_URL   = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471/assignments'
        localSettings.LOCAL_SETTINGS_GALLERY_GRADEBOOK_URL      = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471/gradebook'
        localSettings.LOCAL_SETTINGS_GALLERY_GRADES_STUDENT_URL = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/courses/471/grades'

    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_D2L_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/login'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL 
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/6750'
    
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_JIVE_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/login.jspa'
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media.jspa'
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/community/new1'
    
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_SAKAI_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL
#        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media.jspa'
#        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/community/new1'
        localSettings.LOCAL_SETTINGS_SITE_NEW1_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/site/New1'
        
    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL              = localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_ULTRA_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL              = localSettings.LOCAL_SETTINGS_TEST_BASE_URL
        localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/ultra/tools'
        localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL           = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/ultra/courses'
        localSettings.LOCAL_SETTINGS_COURSE_CONTENT_PAGE        = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/ultra/course'
    return


#===============================================================================
#Take screenshoot of whole screen.
#'fullpath' should contain the file name with its extension PNG!
#===============================================================================
def saveScreenshotToFile(driver, fullPath):
    screenShotPath=os.path.abspath(fullPath)
    return driver.save_screenshot(screenShotPath)


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
    return datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y%H%M%S%f')

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
    if os.getenv('ENV_AUTO') == 'Auto':
        return True
    else:
        return False


# Delete old filed from the log folder
# fileType - Exmaple: '.png'
def clearFilesFromLogFolderPath(fileType):
    path = getLogFileFolderPath()
    filelist = [ f for f in os.listdir(path) if f.endswith(fileType) ]
    for f in filelist:
        os.remove(os.path.join(path, f))


        
# @Author: Oleg Sigalov
# Get all instances from csv file
def getListOfInstances():
    instacesList = {} #[instance:(adminUsername,adminPassword)]
    matrixPath=os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testPartners' + localSettings.LOCAL_SETTINGS_ENV_NAME + '.csv'))
    with open(matrixPath, 'r') as csv_mat: #windows
        testRow = csv.DictReader(csv_mat)
        for row in testRow:
            # Verify first four characters is a digit - instace number
            if row['partner'][:4].isdigit():
                # Update/Append new instance with admin user name and password
                instacesList.update({row['partner']:(row['admin_username'],row['admin_password'])})
                
    return instacesList        
        