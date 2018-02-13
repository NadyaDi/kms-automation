from base import *
import clsTestService
import enums


class Player(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=====================================================================================================================
    #                                                      Channel locators:                 
    #=====================================================================================================================
    PLAYER_IFRAME                                               = ('id', 'kplayer_ifp')
    PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER                       = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-play')]")
    PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER                      = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-pause')]")
    PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER                     = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-replay')]")
    PLAYER_GENERIC_PLAY_REPLAY_PASUSE_BUTTON_CONTROLS_CONTAINER = ('xpath', "//button[@data-plugin-name='playPauseBtn']")
    PLAYER_CURRENT_TIME_LABEL                                   = ('xpath', "//div[@data-plugin-name='currentTimeLabel']")
                                          
    #=====================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here switches to player Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any player method, please use switchToPlayerIframe method, before addressing to player elements
    # because you need to switch to player iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method to 
    # return to default iframe in the end of use of player methods or elements, meaning in the test or other classes.
    #======================================================================================================================
    def switchToPlayerIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
            self.swith_to_iframe(self.PLAYER_IFRAME)
    
    
    # fromActionBar = True, to click play on the bar below the player
    # fromActionBar = Flase, to click play on middle of the screen player
    def clickPlay(self, fromActionBar=True):
        self.switchToPlayerIframe()
        if fromActionBar == True:
            if self.click(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER) == False:
                writeToLog("INFO","FAILED to click Play; fromActionBar = " + str(fromActionBar))
                return False
            
        return True     
            
            
    # fromActionBar = True, to click pause on the bar below the player
    # fromActionBar = Flase, to click pause on middle of the screen player
    def clickPause(self, fromActionBar=True):
        self.switchToPlayerIframe()
        if fromActionBar == True:
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER) == False:
                writeToLog("INFO","FAILED to click Pause; fromActionBar = " + str(fromActionBar))
                return False
            
        return True      
    
    
    # delay - (string) time to play in seconds in format: M:SS (fro example, 3 secodns = '0:03'
    def clickPlayAndPause(self, delay, timeout=30):
        self.switchToPlayerIframe()
        if self.clickPlay() == False:
            return False
        
        # Wait for delay
        if self.wait_for_text(self.PLAYER_CURRENT_TIME_LABEL, delay, timeout) == False:
            writeToLog("INFO","FAILED to seek timer to: '" + delay + "'")
            return False
        
        if self.clickPause() == False:
            return False
        
        return True
    
    
    # The method will play, pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    def clickPlayPauseAndVerify(self, delay, timeout=30, tolerance=1):
        if self.clickPlayAndPause(delay, timeout) == False:
            return False
        
        qrCodeSc = self.clsCommon.qacode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            return False
        
        result = self.clsCommon.qacode.resolveQrCode(qrCodeSc)
        if result == None:
            return False
        
        # Convert delay string to seconds
        qrCodeResultInSeconds = utilityTestFunc.convertTimeToSecondsMSS(delay)
        
        if (qrCodeResultInSeconds > int(result) + tolerance) or (qrCodeResultInSeconds < int(result) - tolerance) == True:
            writeToLog("INFO","FAILED to verify playing, the image and timer are not synchronized; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
            return False
        
        writeToLog("INFO","Playing verified; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
        return True    
    
    
    # The method will play, pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    def navigateToEntryClickPlayPauseAndVerify(self, entryName, delay, timeout=30, tolerance=1):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False 
                  
                if self.clickPlayPauseAndVerify(delay, timeout, tolerance) == False:
                    writeToLog("INFO","FAILED to click Play Pause And Verify")
                    return False
            else:
                writeToLog("INFO","Entry name not supplied")
                return False
            
        except NoSuchElementException:
            return False
          
        return True