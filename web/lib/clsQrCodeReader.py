#########################################################################
# This class meant to create screen shots of video's/pictures
# contain QR code, read them and compare to expected return 
# value of this QR code
#########################################################################
from utilityTestFunc import *
from clsTestService import *
from PIL import Image
import localSettings
try:
    import zbarlight
except:
    pass
import platform

class clsQrCodeReader():
               
    # Take screenshot of the whole page, return the full file path of the screenshot 
    def takeQrCodeScreenshot(self, driver):
        if platform.system() == 'Windows':
            filePath = LOCAL_QRCODE_TEMP_DIR_WINDOWS + "\\" + generateTimeStamp() + ".png"
        elif platform.system() == 'Linux':    
            filePath = LOCAL_QRCODE_TEMP_DIR_LINUX + "/" + generateTimeStamp() + ".png"
        if saveScreenshotToFile(driver, filePath) == True:
            writeToLog("DEBUG","Screenshot of the page save to: " + filePath)
            return filePath
        else:
            writeToLog("DEBUG","Failed to take screenshot of the page")
            return
        
    #Take screenshot of the iframe (player), return the full file path of the screenshot
    def takeQrCodePlayerScreenshot(self, player, driver, fullScreen=False, live=True):
        outTop = -1
        outBottom = -1
        outLeft = -1
        outRight = -1
        try:
            #Get the Iframe element
            if fullScreen:
                element = self.testElement.waitForElementByXpath(driver, player.PLAYER_ELEMENT, 15)
                #Get the location and size of the Iframe (for cropping the image)
                outTop, outBottom, outLeft, outRight = self.getTopBottomLeftRightOfElement(driver, element, live, fullScreen)
                strForDebugMsg = "Player"
            else:
                # Restore to original window driver
                player.switchToPlayerHostPage(driver)            
                element = self.testElement.waitForElementByXpath(driver, player.IFARME_ELEMENT, 15)
                #Get the location and size of the Iframe (for cropping the image)
                outTop, outBottom, outLeft, outRight = self.getTopBottomLeftRightOfElement(driver, element, live, fullScreen)
                player.switchToPlayerIframe(driver)
                strForDebugMsg = "Iframe"
            if element == None:
                writeToLog("DEBUG","DEBUG: Failed to get " + strForDebugMsg + " element")
                return
            
            #Take screenshot (of the whole page)
            filePath = self.takeQrCodeScreenshot(driver)
            im = Image.open(filePath) # uses PIL library to open image in memory
            
            #Crop the image - we want image of the player only
            im = im.crop((int(outLeft), int(outTop), int(outRight), int(outBottom)))
            im.save(filePath) # saves new cropped image
            writeToLog("DEBUG","Screenshot of the QR code from the player saved to: " + filePath)
            return filePath 
        except:
            writeToLog("DEBUG","Failed to take screenshot of the player")
            return
        
        
    def getTopBottomLeftRightOfElement(self, driver, element, isLive, isFullScreen):
        #Get the location and size of the Iframe (for cropping the image)
        location = element.location
        size = element.size
        outTop = -1
        outBottom = -1
        outLeft = -1
        outRight = -1
        locataionY = -1
                 
        if isLive:
            if isFullScreen:
                outTop = 0
                outBottom = (size['height'] * 24) / 100
                if localSettings.LOCAL_SETTINGS_RUN_MDOE == "REMOTE":
                    outLeft = (size['width'] * 73) / 100
                    outRight = (size['width'] * 88) / 100
                else:    
                    outLeft = (size['width'] * 71) / 100
                    outRight = (size['width'] * 85) / 100
            else:
                currentBrowserName = localSettings.LOCAL_RUNNING_BROWSER
                if currentBrowserName == clsTestService.PC_BROWSER_CHROME:
                    locataionY = location['y']
                elif currentBrowserName == clsTestService.PC_BROWSER_FIREFOX:
                    locataionY = 0
                elif currentBrowserName == clsTestService.PC_BROWSER_IE:
                    locataionY = location['y']
                else:
                    self.testService.writeToLog("Unknown browser: " + currentBrowserName)
                    self.status="Fail"
                    return
                outTop = locataionY
                outBottom = locataionY + (size['height'] * 21) / 100
                outLeft = location['x'] + (size['width'] * 78) / 100
                outRight = location['x'] + (size['width'] * 97) / 100       
        else:
            if isFullScreen:
                outTop = 0
                outBottom = (size['height'] * 60) / 100
                outLeft = (size['width'] * 62) / 100   
                outRight = (size['width'] * 86) / 100       
            else:
                outTop = location['y']
                outBottom = location['y'] + (size['height'] * 56) / 100
                outLeft = location['x'] + (size['width'] * 63) / 100
                outRight = location['x'] + (size['width'] * 93) / 100                
        return outTop, outBottom, outLeft, outRight 
     
    # Resolve and return the given path to image with QR code    
    def resolveQrCode(self, filePath):
        if platform.system() == 'Windows':
            proc = subprocess.Popen(LOCAL_QR_DECODER_PATH + ' ' + filePath, stdout=subprocess.PIPE)
            output = str(proc.stdout.read(),'utf-8')
            rcArr = output.split('"')
            try:
                rc = rcArr[1]
                return rc
            except:
                return
            
        elif platform.system() == 'Linux':
            with open(filePath, 'rb') as image_file:
                try:
                    image = Image.open(image_file)
                    image.load()
                    codes = zbarlight.scan_codes('qrcode', image)
                    writeToLog("DEBUG", "DEBUG 1: " + str(codes[0]))
                    rcArr = str(codes[0]).split("'")
                    rc = str(rcArr[1])
                    writeToLog("DEBUG", "DEBUG 1: " + rc)
                    return rc
                except:
                    return
                
                        

        
    # Take screenshot of the PALYER object page and resolve QR code    
    def getAndResolvePlayerQrCode(self, player, driver, fullScreen=False, live=True):
        sc = self.takeQrCodePlayerScreenshot(player, driver, fullScreen, live)
        if sc == None:
            writeToLog("DEBUG","Failed to get screenshot for QR code")
            return None
        result = self.resolveQrCode(sc)
        if result == None:
            writeToLog("DEBUG","Failed to resolve QR code")
            return None
        else:
            writeToLog("DEBUG","QR code result is: " + result)
            return result
    
    #Return live timer in seconds, if function failed, return -1    
    def getTimerFromQrCodeInSeconds(self, player, driver, fullScreen=False, live=True):
        result = self.getAndResolvePlayerQrCode(player, driver, fullScreen, live)
        if result == None:
            return -1
        timer = self.getTimerFromQrResult(result)
        seconds = self.convertTimerToSeconds(timer)
        if seconds == None or seconds == "":
            return -1
        else:
            return seconds

    #Extract the timer (without the milliseconds) from the next format:"2016-08-14T06:27:29.282 00:41:13.597" ==> will return:"00:41:13" 
    def getTimerFromQrResult(self, result):
        resTime = result.split(" ")
        try:
            rtArr = resTime[1]
            rt = rtArr.split(".")
            res = rt[0]
            return res
        except:
            writeToLog("DEBUG","Failed to get timer from string: '" + result + "'")
            return
        
    # Converts timer (time format: HH:MM:SS) to seconds  
    def convertTimerToSeconds(self, timer):
        try:
            x = time.strptime(timer,'%H:%M:%S')
            sec = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
            return sec
        except:
            writeToLog("DEBUG","Failed to convert timer to seconds, origin timer string: '" + timer + "'")
            return
        
        
    #Waits till the playback is playing
    #Going take timer from QR code, number of times. We want to see the timer is moving forward.
    def waitForBasicEntryPlaybackByQRCode(self, player, driver, timeOut, sampleCount=3, fullScreen=False):
        count = 0
        timeElapsed = 0
        newTime = 0
        liveTime = 0
        startTime =  time.time()
        
        while (timeElapsed <= timeOut) and (count < sampleCount):
            newTime = self.getTimerFromQrCodeInSeconds(player, driver, fullScreen, False)
            if newTime > liveTime:
                count += 1
            else:
                count = 0
            liveTime = newTime
            #Get elapsed time
            timeElapsed = int(time.time() - startTime)
            time.sleep(1)
        
        if (count >= sampleCount) and (timeElapsed <= timeOut):
            writeToLog("DEBUG","Entry is playing")
            return True
        else:
            writeToLog("DEBUG","Entry is not playing")
            return False

    
    
    #Works only with QR entries
    #We assume if there is no QR and the timer started from 0:00
    #Return True no QR exists and timer is less than a few seconds (tolerance)
    def waitForAdStartPlaying(self, player, driver, expectedLow, expectedHigh, timeOut, fullScreen=False):
        #Wait for QR stop - not exist
        timeElapsed = 0
        startTime =  time.time()
        curQrTime = 0
        
        while (timeElapsed <= timeOut):
            curQrTime = self.getTimerFromQrCodeInSeconds(player, driver, fullScreen, False)
            if curQrTime == -1:
                #Get elapsed time
                timeElapsed = int(time.time() - startTime)
#                 Verify timer less than few sec - Ad started
                if player.waitForPlayerTimeIsBetween(driver, expectedLow, expectedHigh, timeOut - timeElapsed) == False:
                    writeToLog("DEBUG","Expected timer less than few seconds")
                    return False
                else:
                    break               
            #Get elapsed time
            timeElapsed = int(time.time() - startTime)
                
        if (timeElapsed <= timeOut):
            writeToLog("DEBUG","Ad started to play")
            return True
        else:
            writeToLog("DEBUG","Ad NOT started to play")
            return False        
            
    # Verify that the QR from the video is corresponding with the timer.
    # This works function works only with specific entries which have QR code like this: "2015-06-14T19:50:59.600 00:00:18.666"
    def VerifyQrCorrespondingWithTimer(self, player, driver, tolerance, fullScreen=False, live=False):
        timerTime = getTimerInSeconds(driver, player)
        writeToLog("DEBUG", "TIMMMMMMMER: " + str(timerTime))
        qrTime = self.getTimerFromQrCodeInSeconds(player, driver, fullScreen, live)
        writeToLog("DEBUG", "QRRRRRRRRRR: " + str(qrTime))
        if qrTime <= timerTime + tolerance and qrTime >= timerTime - tolerance:
            return True
        else:
            writeToLog("DEBUG","QR code = " + str(qrTime) + "; Player Timer = " + str(timerTime) + "; Tolarance = " + str(tolerance))
            return False