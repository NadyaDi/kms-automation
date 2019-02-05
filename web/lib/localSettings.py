import os,sys,enums

def isAutomationEnv():
        if os.getenv('ENV_AUTO') == 'Auto':
            return True
        else:
            return False
        
LOCAL_SETTINGS_KMS_WEB_DIR                  = os.getenv('KMS_WEB')
LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR           = 'C:\\selenium\\kms-automation\\web\\'
if (os.getenv('MD_RELEASE',"") != ""):
    LOCAL_SETTINGS_TESTED_RELEASE           = os.getenv('MD_RELEASE',"")
else:
    LOCAL_SETTINGS_TESTED_RELEASE           = "v2.61.rc8"
        
LOCAL_SETTINGS_WEBDRIVER_LOCAL_CHROME_PATH  = 'C:\\selenium\\drivers\\chromedriver.exe'
LOCAL_SETTINGS_WEBDRIVER_LOCAL_IE_PATH      = 'C:\\selenium\\drivers\\IEDriverServer.exe'

LOCAL_RUNNING_BROWSER                       = ''
LOCAL_QR_DECODER_PATH                       = "C:\\Program Files (x86)\\Kaltura\\QRCodeDetector\\QRCodeDetector.exe"

LOCAL_SETTINGS_IMPLICITLY_WAIT              = 30
LOCAL_SETTINGS_WEBDRIVER_START_FF_RETRIES   = 5
LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY        = "il-AutoKmsHub-qa.dev.kaltura.com"
LOCAL_SETTINGS_SELENIUM_HUB_URL             = "http://" + LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":4444/wd/hub" #hub address
LOCAL_SETTINGS_BROWSER_PROXY                = LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":9090" #proxy server address and port.    
LOCAL_SETTINGS_BROWSER_PROXY_MOBILES        = LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":9091" #proxy server address and port.
LOCAL_SETTINGS_BROWSER_PROXY_MOBILES_PORT   = 9600
LOCAL_SETTINGS_AUTOIT_SERVICE_PORT          = '4723'
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST          = 'il-kmsnode1'  + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST2         = 'il-kmsnode2' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST3         = 'il-kmsnode3' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST4         = 'il-kmsnode4' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST5         = 'il-kmsnode5' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST6         = 'il-kmsnode6' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST7         = 'il-kmsnode7' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST8         = 'il-kmsnode8' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST9         = 'il-kmsnode9' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST10        = 'il-kmsnode10' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST11        = 'il-kmsnode11' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST12        = 'il-kmsnode12' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST13        = 'il-kmsnode13' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST14        = 'il-kmsnode14' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST15        = 'il-kmsnode15' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST16        = 'il-classroom6' + ':' + LOCAL_SETTINGS_AUTOIT_SERVICE_PORT

LOCAL_SETTINGS_APACHE_SERVER                = 'qa-auto-report'
LOCAL_SETTINGS_APACHE_EMBED_PATH            = 'http://' + LOCAL_SETTINGS_APACHE_SERVER + '/embed/'
LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER    = '/mnt/auto_kms_py1/embed/'


    
LOCAL_SETTINGS_SELENIUM_GRID_POOL           = "qaKmsFrontEnd"  
    
LOCAL_RUN_MODE                              = "LOCAL"
REMOTE_RUN_MODE                             = "REMOTE"
if isAutomationEnv() == True:
    LOCAL_SETTINGS_RUN_MDOE                     = REMOTE_RUN_MODE
else:
    LOCAL_SETTINGS_RUN_MDOE                     = LOCAL_RUN_MODE

LOCAL_SETTINGS_PRACTITEST_PROJECT_ID                  = 1328
LOCAL_SETTINGS_PRACTITEST_AUTOMATED_SESSION_FILTER_ID = 259788 #PractiteTest Filter: Pending
LOCAL_SETTINGS_PRACTITEST_NIGHT_RUN_FILTER_ID         = '437000'
LOCAL_SETTINGS_PRACTITEST_ONLY_EXECUTE_AT_NIGHT       = True
LOCAL_SETTINGS_PRACTITEST_API_TOKEN                   = "deee12e1d8746561e1815d0430814c82c9dbb57d"
LOCAL_SETTINGS_DEVELOPER_EMAIL                        = "oleg.sigalov@kaltura.com"

# Will be updated after test starts
LOCAL_SETTINGS_AUTOIT_SCRIPTS                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'autoit'))
if LOCAL_SETTINGS_RUN_MDOE == LOCAL_RUN_MODE:
    LOCAL_SETTINGS_MEDIA_PATH                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'media'))
    LOCAL_SETTINGS_TEMP_PATH                    = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'temp'))
    LOCAL_SETTINGS_TEMP_DOWNLOADS               = None # Will updated in clsTestService, basicSetUp method
    LOCAL_QRCODE_TEMP_DIR                       = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'screenShots', 'qrCode'))
else:
    LOCAL_SETTINGS_TEMP_PATH                    = os.path.abspath(os.path.join(os.getenv('KMS_WEB'),'temp'))
    LOCAL_QRCODE_TEMP_DIR                       = os.path.abspath(os.path.join(os.getenv('KMS_WEB'),'screenShots','qrCode'))
    LOCAL_SETTINGS_MEDIA_PATH                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'media'))
    LOCAL_SETTINGS_TEMP_DOWNLOADS               = None # Will updated in clsTestService, basicSetUp method

LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD = None # Will updated in clsTestService, basicSetUp method
LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH      = '/home/local/KALTURA/oleg.sigalov/build/workspace/qaKmsFrontEnd/web/media'
if isAutomationEnv() == True:
    LOCAL_SETTINGS_MEDIA_PATH               = 'C:\\selenium\\kms-automation\\web\\media'


# Will updates in 'utilityTestFunc' class, 'updateTestCredentials' method:
LOCAL_SETTINGS_GUID                         = None
LOCAL_SETTINGS_URL_PREFIX                   = 'http://'
LOCAL_SETTINGS_TEST_BASE_URL                = LOCAL_SETTINGS_URL_PREFIX
LOCAL_SETTINGS_KMS_LOGIN_URL                = None 
LOCAL_SETTINGS_KMS_MY_MEDIA_URL             = None
LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL         = None
LOCAL_SETTINGS_KMS_MY_CHANNELS_URL          = None
LOCAL_SETTINGS_KMS_CHANNELS_URL             = None
LOCAL_SETTINGS_KMS_ADMIN_URL                = None
LOCAL_SETTINGS_KMS_MY_HISTORY_URL           = None
LOCAL_SETTINGS_KMS_MEDIA_SELECTION_URL      = None
LOCAL_SETTINGS_KMS_HOME_URL                 = None
LOCAL_SETTINGS_KMS_GALLERIES_URL            = None

LOCAL_SETTINGS_TESTING_NEW_UI_ENV           = 'TestingNewUI'
LOCAL_SETTINGS_TESTING_ENV                  = 'Testing'
LOCAL_SETTINGS_PROD_NEW_UI_ENV              = 'ProdNewUI'
LOCAL_SETTINGS_PROD_ENV                     = 'Prod'
LOCAL_SETTINGS_ENV_NAME                     = LOCAL_SETTINGS_TESTING_ENV
LOCAL_SETTINGS_IS_NEW_UI                    = True

# Partner credentials
LOCAL_SETTINGS_PARTNER                      = None
LOCAL_SETTINGS_LOGIN_USERNAME               = None
LOCAL_SETTINGS_LOGIN_PASSWORD               = None
LOCAL_SETTINGS_ADMIN_USERNAME               = None
LOCAL_SETTINGS_ADMIN_PASSWORD               = None
LOCAL_SETTINGS_USERNAME_AFTER_LOGIN         = None

# Test run variables
LOCAL_SETTINGS_APPLICATION_UNDER_TEST       = enums.Application.MEDIA_SPACE
TEST_CURRENT_IFRAME_ENUM                    = enums.IframeName.DEFAULT

# KAF Variables
LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL      = 'https://il-qa-blackboard-q2-2018.dev.kaltura.com:8443'
LOCAL_SETTINGS_KAF_SHAREPOINT_BASE_URL      = 'https://kalturasp2013.sharepoint.com/sites/QA/QAtesting/automation/SitePages'
LOCAL_SETTINGS_KAF_MOODLE_BASE_URL          = 'https://extqa4.dev.kaltura.com/moodle3.2vs4.0.10new/moodle'
LOCAL_SETTINGS_KAF_CANVAS_BASE_URL          = 'https://kaltura.instructure.com'
LOCAL_SETTINGS_KAF_D2L_BASE_URL             = 'https://kalturaqa2.d2l-partners.brightspace.com/d2l/home'
LOCAL_SETTINGS_KAF_JIVE_BASE_URL            = 'http://il-qa-jive.kaltura.com'
LOCAL_SETTINGS_KAF_SAKAI_BASE_URL           = 'https://sakai.dev.kaltura.com/portal'