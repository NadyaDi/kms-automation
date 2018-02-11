import os,sys,enums

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
LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY        = "il-AutoKmsHub-qa.dev.kaltura.com"
LOCAL_SETTINGS_SELENIUM_HUB_URL             = "http://" + LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":4444/wd/hub" #hub address
LOCAL_SETTINGS_BROWSER_PROXY                = LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":9090" #proxy server address and port.    
LOCAL_SETTINGS_BROWSER_PROXY_MOBILES        = LOCAL_SETTINGS_INHOUSE_HUB_AND_PROXY + ":9091" #proxy server address and port.
LOCAL_SETTINGS_BROWSER_PROXY_MOBILES_PORT   = 9600
LOCAL_SETTINGS_WINDOWS_NODE_HOSTNAME        ='il-AutoKmsNode-qa'
LOCAL_SETTINGS_AUTOIT_SERVICE_HOST          = LOCAL_SETTINGS_WINDOWS_NODE_HOSTNAME + ':4723'
    
LOCAL_SETTINGS_SELENIUM_GRID_POOL_FRONTEND  = "qaKmsFrontEnd"
# LOCAL_SETTINGS_SELENIUM_GRID_POOL_BACKEND   = "qaCoreBackEnd"
LOCAL_SETTINGS_SELENIUM_GRID_POOL           = LOCAL_SETTINGS_SELENIUM_GRID_POOL_FRONTEND  
    
LOCAL_RUN_MODE                              = "LOCAL"
REMOTE_RUN_MODE                             = "REMOTE"
LOCAL_SETTINGS_RUN_MDOE                     = LOCAL_RUN_MODE


LOCAL_SETTINGS_PRACTITEST_PROJECT_ID                  = 1328
LOCAL_SETTINGS_PRACTITEST_AUTOMATED_SESSION_FILTER_ID = 259788 #PractiteTest Filter: Pending
LOCAL_SETTINGS_PRACTITEST_API_TOKEN                   = "deee12e1d8746561e1815d0430814c82c9dbb57d"
LOCAL_SETTINGS_DEVELOPER_EMAIL                        = "oleg.sigalov@kaltura.com"

# Will be updated after test starts
LOCAL_SETTINGS_AUTOIT_SCRIPTS                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'autoit'))
if LOCAL_SETTINGS_RUN_MDOE == LOCAL_RUN_MODE:
    LOCAL_SETTINGS_MEDIA_PATH                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'media'))
    LOCAL_SETTINGS_TEMP_PATH                    = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'media'))
    LOCAL_SETTINGS_TEMP_DOWNLOADS               = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'temp\\downloads\\'))
    LOCAL_SETTINGS_TEMP_DOWNLOADS               = os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'temp\\downloads\\')
    LOCAL_QRCODE_TEMP_DIR_WINDOWS               = os.path.abspath(os.path.join(LOCAL_SETTINGS_KMS_WEB_DIR,'screenShots\\qrCode'))
else:
    LOCAL_SETTINGS_MEDIA_PATH                   = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'media'))
    LOCAL_SETTINGS_TEMP_PATH                    = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'temp'))
    LOCAL_SETTINGS_TEMP_DOWNLOADS               = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'temp','downloads'))  
    LOCAL_QRCODE_TEMP_DIR_LINUX                 = os.path.abspath(os.path.join(LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR,'screenShots','qrCode'))
    
    if isAutomationEnv() == True:
        LOCAL_SETTINGS_MEDIA_PATH               = 'C:\\selenium\\kms-automation\\web\\media'
    
LOCAL_SETTINGS_GUID                         = None
LOCAL_SETTINGS_URL_PREFIX                   = 'http://'
LOCAL_SETTINGS_TEST_BASE_URL                = LOCAL_SETTINGS_URL_PREFIX
LOCAL_SETTINGS_KMS_LOGIN_URL                = None 
LOCAL_SETTINGS_KMS_MY_MEDIA_URL             = None
LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL         = None
LOCAL_SETTINGS_KMS_MY_CHANNELS_URL          = None
LOCAL_SETTINGS_KMS_ADMIN_URL                = None

LOCAL_SETTINGS_PROD_ENVIRONMENT             = 'Prod'              
LOCAL_SETTINGS_TESTING_ENVIRONMENT          = 'Testing'
LOCAL_SETTINGS_IS_NEW_UI                    = True
LOCAL_SETTINGS_RUN_ENVIRONMENT              = LOCAL_SETTINGS_TESTING_ENVIRONMENT
# Partner credentials
LOCAL_SETTINGS_PARTNER                      = None
LOCAL_SETTINGS_LOGIN_USERNAME               = None
LOCAL_SETTINGS_LOGIN_PASSWORD               = None
LOCAL_SETTINGS_ADMIN_USERNAME               = None
LOCAL_SETTINGS_ADMIN_PASSWORD               = None
LOCAL_SETTINGS_USERNAME_AFTER_LOGIN         = None
# Test run variables
TEST_CURRENT_IFRAME_ENUM                    = enums.IframeName.DEFAULT



#TO DELETE
# LOCAL_SETTINGS_QA_BACKEND_API_URL           = "http://qa-apache-php7.dev.kaltura.com"
# LOCAL_SETTINGS_BACKEND_API_URL              = LOCAL_SETTINGS_QA_BACKEND_API_URL
# LOCAL_SETTINGS_PARTNER                      = '4783'
# LOCAL_SETTINGS_PARTNER_SECRET               = '87e3c95b849a9cc4be5c14d7a130ccfc'
# LOCAL_SETTINGS_KS_TYPE                      = '2'