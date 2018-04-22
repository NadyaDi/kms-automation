#########################################################################
# This class meant to create screen shots of video's/pictures
# contain QR code, read them and compare to expected return 
# value of this QR code
#########################################################################
from utilityTestFunc import *
from clsTestService import *
from selenium.webdriver.common.keys import Keys
from PIL import Image
import localSettings
from time import sleep
try:
    import zbarlight
except:
    pass
import platform

class QrCodeReader(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
               
    # Take screenshot of the whole page, return the full file path of the screenshot 
    def takeQrCodeScreenshot(self):
        filePath = os.path.abspath(os.path.join(LOCAL_QRCODE_TEMP_DIR, generateTimeStamp() + ".png"))
        if self.takeScreeshot(filePath) == True:
            writeToLog("INFO","Screenshot of the page save to: " + filePath)
            return filePath
        else:
            writeToLog("INFO","FAILED to take screenshot of the page")
            return False
        
        
    # Take screenshot upper half of the player, return the full file path of the screenshot 
    def takeQrCodeVideoScreenshot(self):
        filePath = os.path.abspath(os.path.join(LOCAL_QRCODE_TEMP_DIR, generateTimeStamp() + ".png"))
        if self.takeScreeshot(filePath) == True:
            writeToLog("INFO","Screenshot of the page save to: " + filePath)
        else:
            writeToLog("INFO","FAILED to take screenshot of the page")
            return False       
        playerElement = self.get_element_attributes(('xpath', '/html/body'))
        # Crop the image
        img = Image.open(filePath)
        img2 = img.crop((playerElement['right'] / 1.37, playerElement['top'], playerElement['right'], playerElement['bottom'] / 1.63))
        img2.save(filePath)
        
        return filePath
    

    # Take screenshot the bottom (slide on bottom right of the player) half of the player, return the full file path of the screenshot 
    def takeQrCodeSlideScreenshot(self):
        filePath = os.path.abspath(os.path.join(LOCAL_QRCODE_TEMP_DIR, generateTimeStamp() + ".png"))
        if self.takeScreeshot(filePath) == True:
            writeToLog("INFO","Screenshot of the page save to: " + filePath)
        else:
            writeToLog("INFO","FAILED to take screenshot of the page")
            return False       
        playerElement = self.get_element_attributes(('xpath', '/html/body'))
        # Crop the image
        img = Image.open(filePath)
        img2 = img.crop((playerElement['right'] / 1.37, playerElement['bottom'] / 1.63, playerElement['right'], playerElement['bottom']))
        img2.save(filePath)
        
        return filePath
        
        
        
        # Take screenshot of the upload,capture,auto-generate image in thumbnail tab and return the full file path of the screenshot 
    def takeQrCodeTumbnailTabScreenshot(self):
        self.get_element(self.clsCommon.editEntryPage.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA).send_keys(Keys.PAGE_DOWN)
        sleep(1)
        filePath = os.path.abspath(os.path.join(LOCAL_QRCODE_TEMP_DIR, generateTimeStamp() + ".png"))
        if self.takeScreeshot(filePath) == True:
            writeToLog("INFO","Screenshot of the page save to: " + filePath)
        else:
            writeToLog("INFO","FAILED to take screenshot of the page")
            return False       
        pageElement = self.get_element_attributes(('xpath', '/html/body'))
        # Crop the image
        img = Image.open(filePath)
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            img2 = img.crop((pageElement['right'] /10, pageElement['bottom'] / 4.75, pageElement['right'] , pageElement['bottom']))
            
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            img2 = img.crop((pageElement['right'] /10, pageElement['bottom'] / 2, pageElement['right'] , pageElement['bottom']))
            
        img2.save(filePath)
        
        return filePath
        
        
        
    # Take custom screenshot home page playlist thumbnail and return the full file path of the screenshot 
    def takeCustomQrCodeScreenshot(self, left, top, right, buttom):
        filePath = os.path.abspath(os.path.join(LOCAL_QRCODE_TEMP_DIR, generateTimeStamp() + ".png"))
        if self.takeScreeshot(filePath) == True:
            writeToLog("INFO","Screenshot of the page save to: " + filePath)
        else:
            writeToLog("INFO","FAILED to take screenshot of the page")
            return False       
        pageElement = self.get_element_attributes(('xpath', '/html/body'))
        # Crop the image
        img = Image.open(filePath)
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            img2 = img.crop((pageElement['right'] /left , pageElement['bottom'] / top, pageElement['right'] / right , pageElement['bottom'] / buttom))
            
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            img2 = img.crop(pageElement['right'] /10, pageElement['bottom'] / 2, pageElement['right'] , pageElement['bottom'])
            
        img2.save(filePath)
        
        return filePath
    
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
        
        
    # Resolve and return the given path to image with QR code    
    def resolveQrCode(self, filePath):
        if platform.system() == 'Windows':
            proc = subprocess.Popen(LOCAL_QR_DECODER_PATH + ' "' + filePath + '"', stdout=subprocess.PIPE)
            output = str(proc.stdout.read(),'utf-8')
            rcArr = output.split('"')
            try:
                rc = rcArr[1]
                return rc
            except:
                return None
            
        elif platform.system() == 'Linux':
            with open(filePath, 'rb') as image_file:
                try:
                    image = Image.open(image_file)
                    image.load()
                    codes = zbarlight.scan_codes('qrcode', image)
                    rcArr = str(codes[0]).split("'")
                    rc = str(rcArr[1])
                    return rc
                except:
                    return
        
        
    # Take screenshot of the PALYER object page and resolve QR code    
    def getScreenshotAndResolvePlayerQrCode(self, playerPart=''):
        if playerPart == enums.PlayerPart.TOP:
            sc = self.takeQrCodeVideoScreenshot()
        elif playerPart == enums.PlayerPart.BOTTOM:
            sc = self.takeQrCodeSlideScreenshot()
        else:
            sc = self.takeQrCodeScreenshot()
        if sc == None:
            writeToLog("DEBUG","Failed to get screenshot for QR code")
            return None
        result = self.resolveQrCode(sc)
        if result == None:
            writeToLog("DEBUG","Failed to resolve QR code")
            return False
        else:
            writeToLog("DEBUG","QR code result is: " + result)
            return result        
        
        
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
    
    
    # Take screenshot of the image in thumbnail tab and resolve QR code    
    def getScreenshotAndResolveImageInThumbnailTabQrCode(self):
        sc = self.takeQrCodeTumbnailTabScreenshot()
        if sc == None:
            writeToLog("DEBUG","Failed to get screenshot for QR code")
            return None
        result = self.resolveQrCode(sc)
        if result == None:
            writeToLog("DEBUG","Failed to resolve QR code")
            return False
        else:
            writeToLog("DEBUG","QR code result is: " + result)
            return result 
        
    # Take screenshot of the image in home page playlist according to the coordinate  crop and resolve QR code  
    def getScreenshotAndResolveImageQrCodeInHomePagePlaylist(self, cropLeft, croTop, cropRight, cropButtom):
        sc = self.takeCustomQrCodeScreenshot(cropLeft, croTop, cropRight, cropButtom)
        if sc == None:
            writeToLog("DEBUG","Failed to get screenshot for QR code")
            return None
        result = self.resolveQrCode(sc)
        if result == None:
            writeToLog("DEBUG","Failed to resolve QR code")
            return False
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