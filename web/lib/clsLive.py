import time
from clsTestService import clsTestService
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from clsQrCodeReader import clsQrCodeReader
from logger import *

class clsLive:
    
    #============================================================================================================
    #The class contains functions that relates to Live actions
    #============================================================================================================
    testService = clsTestService()
    qr          = clsQrCodeReader()
    
    #This function verifies that Live Red icon is visible and live status is visible
    def verifyControlBarLiveIndecators(self, test, driver):
        if test.player.getLiveIconOnAirElement(driver) == None:
            writeToLog("INFO","Step FAILED: Red icon is not visible")
            return False
        
        if test.player.getControlBarLiveStatus(driver) != "LIVE":
            writeToLog("INFO","Step FAILED: Failed to verify control live status")
            return False
        
    #Waits till the playback is playing
    #Going take timer from QR code, number of times. We want to see the timer is moving forward.
    def waitForLivePlaybackByQRCode(self, player, driver, timeOut, sampleCount=3, fullScreen=False):
        count = 0
        timeElapsed = 0
        newTime = 0
        liveTime = 0
        startTime =  time.time()
        
        while (timeElapsed <= timeOut) and (count < sampleCount):
            newTime = self.qr.getTimerFromQrCodeInSeconds(player, driver, fullScreen)
            if newTime > liveTime:
                count += 1
            else:
                count = 0
            liveTime = newTime
            #Get elapsed time
            timeElapsed = int(time.time() - startTime)
            time.sleep(1)
        
        if (count >= sampleCount) and (timeElapsed <= timeOut):
            writeToLog("DEBUG","Live is playing")
            return True
        else:
            writeToLog("DEBUG","Live is not playing")
            return False
            