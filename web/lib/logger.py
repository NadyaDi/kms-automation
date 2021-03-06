import datetime
import os, sys
import time
import traceback

from localSettings import *
import localSettings
import utilityTestFunc


def writeStatsToCSV(test):
    
    timeSuffix = ""
    if (os.getenv('SESSION_RUN_TIME',"") != ""):
        timeSuffix = '_' + os.getenv('SESSION_RUN_TIME',"")
    
    CSV_STATS_FILE            = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'logs', LOCAL_SETTINGS_TESTED_RELEASE + timeSuffix + '.csv'))
    
    practiTestSessionID = os.getenv('MD_PRACTITEST_SET_ID',"") 
    
    if (os.path.isfile(CSV_STATS_FILE) == False):
        file = open(CSV_STATS_FILE, "w")
        file.write ("testSessionID,testNum,browser,browserVersion,startTime,duration,status,testedRelease,proxyEnabled,practitestSessionID\n")
        file.close()

    file = open(CSV_STATS_FILE, "a")
    file.write (os.getenv('SESSION_RUN_TIME','') + "," + test.testNum + "," + test.browserName + "," + test.browserVersion + "," + str(test.startTime) + "," + test.duration + "," + test.status + "," + LOCAL_SETTINGS_TESTED_RELEASE + "," + practiTestSessionID + "\n")
    file.close()
    
def getLogFileFolderPath():
    runningTestNum    = os.getenv('RUNNING_TEST_ID',"")
    return os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR, 'logs', runningTestNum))    
    
#===========================================================================
#the class contains functions that manage and update the log file
#===========================================================================
def writeToLog(logLevel, logLine):
    
    timeSuffix        = ""
    runningTestNum    = os.getenv('RUNNING_TEST_ID',"")
    LOG_FOLDER_PREFIX = ""
    if (os.getenv('BUILD_ID',"") != ""):
        LOG_FOLDER_PREFIX = os.getenv('BUILD_ID',"")
    if (os.getenv('SESSION_RUN_TIME',"") != ""):
        timeSuffix = '_' + os.getenv('SESSION_RUN_TIME',"")

    if utilityTestFunc.isAutoEnvironment() == True:
        LOGFILE                   = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR, '..', 'logs', LOG_FOLDER_PREFIX, LOCAL_SETTINGS_TESTED_RELEASE + str(timeSuffix) + '.log'))
    else:
        LOGFILE                   = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR, 'logs', LOG_FOLDER_PREFIX, LOCAL_SETTINGS_TESTED_RELEASE + str(timeSuffix) + '.log'))
    TEST_LOG_FILE_FOLDER_PATH = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR, 'logs', runningTestNum))
    TEST_LOG_FILE             = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR, 'logs' , runningTestNum, runningTestNum + '.log'))
    
    # Write to main log file
    d = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    
    try:
        file = open(LOGFILE, 'r')
    except IOError:
        file = open(LOGFILE, 'w')
        file.close()  
    file = open(LOGFILE, "a")
    file.write (d + " " + logLine + "\n")
    if (logLevel == "INFO"):        
        print (d + " " + logLine)
    file.close()
    
    # Write to test logfile
    if (os.path.isdir(TEST_LOG_FILE_FOLDER_PATH) == False):
        os.makedirs(TEST_LOG_FILE_FOLDER_PATH, exist_ok=True)             
        d = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    try:
        file = open(TEST_LOG_FILE, 'r')
    except IOError:
        file = open(TEST_LOG_FILE, 'w')
        file.close()      
    file = open(TEST_LOG_FILE, "a")
    file.write (d + " " + logLine + "\n")
    file.close()

#===============================================================================
# the function writes to the log that we started the test, on browser X and player version Y. we allso write the test url
#===============================================================================
def logStartTest(test, browser, application=enums.Application.MEDIA_SPACE):
    # Set the Application under test (KMS, BB, Moodle, Canvas...) - Default is Media Space
    if application == enums.Application.PITCH:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.PITCH
    elif application == enums.Application.BLACK_BOARD:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.BLACK_BOARD
    elif application == enums.Application.SHARE_POINT:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.SHARE_POINT
    elif application == enums.Application.MOODLE:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.MOODLE
    elif application == enums.Application.CANVAS:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.CANVAS
    elif application == enums.Application.D2L:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.D2L
    elif application == enums.Application.JIVE:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.JIVE
    elif application == enums.Application.SAKAI:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.SAKAI
    elif application == enums.Application.BLACKBOARD_ULTRA:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.BLACKBOARD_ULTRA
    else:
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.MEDIA_SPACE
     
    os.environ["RUNNING_TEST_ID"] = test.testNum
    try:
        # Clear log folder
        if os.environ["RUNNING_TEST_ID"] != "":
            utilityTestFunc.clearFilesFromLogFolderPath('.png')
            utilityTestFunc.clearFilesFromLogFolderPath('.log') 
    except:
        pass  
    hostname = 'Localhost'
    if isAutomationEnv() == True:
        hostname = localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL
    writeToLog("INFO","************************************************************************************************************************")
    writeToLog("INFO",str(localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST) + ": test_" + test.testNum + " Start on browser '" + browser + "'on host '" + hostname + "'")
    
    try:        
        # Update localSetting partner details(base URL, credentials, Practitest ID
        if utilityTestFunc.updateTestCredentials('test_' + test.testNum, application) == False:
            writeToLog("INFO","Unable to find credentials for test: '" + test.testNum + "'")
            return False
    except:
        return False
    
    writeToLog("INFO","NEW UI is " + str(localSettings.LOCAL_SETTINGS_IS_NEW_UI) + "; Page url: " + localSettings.LOCAL_SETTINGS_TEST_BASE_URL) 
    return True

     
#===============================================================================
# the function writes to the log that we started sniffing http traffic
#===============================================================================
def logStartSniffing(test):
    writeToLog("INFO","starts sniffing HTTP traffic")
    test.myProxy.new_har()
        
#===============================================================================
# the function writes to the log that we finished playing the entry/playlist
#===============================================================================    
def logFinishedPlaying(test):
    writeToLog("INFO","finished playing")
  
#===============================================================================
# the function writes to the log that we finished sniffing http traffic
#===============================================================================
def logFinishedSniffing(test):    
    writeToLog("INFO","done sniffing HTTP traffic")  
        
#===============================================================================
# the function writes in the log that we finished the test. we write if the test failed or succeeded and how much time it took 
#===============================================================================
def logFinishedTest(test,startTime):
        test.duration = str(round(time.time() - startTime))
        writeToLog("INFO","test_" + test.testNum + ": " + test.status + " (" + test.duration + " sec)")
        writeStatsToCSV(test)
        writeToLog("INFO", "TEST FINISHED - LAST ROW")  
        
#===========================================================================================
# the function writes to log the excption 
#===========================================================================================    
    
def log_exception(inst):
    writeToLog("INFO",str(inst))
    var = traceback.format_exc()
    writeToLog("INFO","Exception : " + str(var))