import os
import shutil
from admin import Admin
from autoit import Autoit
from base import Base
from category import Category
from channel import Channel
from clsQrCodeReader import QrCodeReader
import clsTestService
from editEntryPage import EditEntryPage
from entryPage import EntryPage
from general import General
from kea import Kea
import localSettings
from logger import *
from login import Login
from myHistory import MyHistory
from myMedia import MyMedia
from myPlaylists import MyPlaylists
from player import Player
from upload import Upload
from webcast import Webcast
from home import Home
from freeTrial import FreeTrial
from pitch import Pitch
from kafBB import BlackBoard
from kafSharepoint import SharePoint
from selenium.webdriver.common.keys import Keys
from api import ApiClientSession
from globalSearch import GlobalSearch
import filecmp
from kafGeneric import KafGeneric
from kafMoodle import Moodle
from kafCanvas import Canvas
from kafD2L import D2L
from kafJive import Jive
from kafSakai import Sakai
from recscheduling import Recscheduling
from kafBBUltra import BlackBoardUltra
from quizAnalytics import QuizAnalytics
from reach import Reach



    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
class Common():
    # Parameters
    driver = None
   
    def __init__(self, driver):
        self.driver             = driver
        self.base               = Base(driver)
        self.autoit             = Autoit(self) 
        self.admin              = Admin(self, driver)
        self.login              = Login(self, driver)
        self.upload             = Upload(self, driver)
        self.general            = General(self, driver)
        self.myMedia            = MyMedia(self, driver)
        self.entryPage          = EntryPage(self, driver)
        self.editEntryPage      = EditEntryPage(self, driver)
        self.category           = Category(self, driver)
        self.channel            = Channel(self, driver)
        self.myPlaylists        = MyPlaylists(self, driver)
        self.player             = Player(self, driver)
        self.myHistory          = MyHistory(self, driver)
        self.qrcode             = QrCodeReader(self, driver)
        self.kea                = Kea(self, driver)
        self.home               = Home(self, driver)
        self.freeTrail          = FreeTrial(self, driver)
        self.apiClientSession   = ApiClientSession(self, driver)
        self.globalSearch       = GlobalSearch(self, driver)
        self.webcast            = Webcast(self, driver)
        self.recscheduling      = Recscheduling(self, driver)
        self.quizAnalytics      = QuizAnalytics(self, driver)
        self.pitch              = Pitch(self, driver)
        self.reach              = Reach(self, driver)
        ### KAF ###
        self.kafGeneric         = KafGeneric(self, driver)
        self.blackBoard         = BlackBoard(self, driver)
        self.sharePoint         = SharePoint(self, driver)
        self.moodle             = Moodle(self, driver)
        self.canvas             = Canvas(self, driver)
        self.d2l                = D2L(self, driver)
        self.jive               = Jive(self, driver)
        self.sakai              = Sakai(self, driver)
        self.blackBoardUltra    = BlackBoardUltra(self, driver)
        
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def instertPathInFileUploadWindows(self, path):
        if localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd":
            autoitDr = self.autoit.autoitDriver
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd2":
            autoitDr = self.autoit.autoitDriver2
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd3":
            autoitDr = self.autoit.autoitDriver3
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd4":
            autoitDr = self.autoit.autoitDriver4
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd5":
            autoitDr = self.autoit.autoitDriver5
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd6":
            autoitDr = self.autoit.autoitDriver6
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd7":
            autoitDr = self.autoit.autoitDriver7    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd8":
            autoitDr = self.autoit.autoitDriver8    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd9":
            autoitDr = self.autoit.autoitDriver9    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd10":
            autoitDr = self.autoit.autoitDriver10                                        
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd11":
            autoitDr = self.autoit.autoitDriver11
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd12":
            autoitDr = self.autoit.autoitDriver12
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd13":
            autoitDr = self.autoit.autoitDriver13
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd14":
            autoitDr = self.autoit.autoitDriver14
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd15":
            autoitDr = self.autoit.autoitDriver15         
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd16":
            autoitDr = self.autoit.autoitDriver16  
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd17":
            autoitDr = self.autoit.autoitDriver17  
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd18":
            autoitDr = self.autoit.autoitDriver18  
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd19":
            autoitDr = self.autoit.autoitDriver19  
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd20":
            autoitDr = self.autoit.autoitDriver20
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd21":
            autoitDr = self.autoit.autoitDriver21 
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd22":
            autoitDr = self.autoit.autoitDriver22
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd23":
            autoitDr = self.autoit.autoitDriver23             
                
                        
        if (localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_IE):
            # TODO IE not implemented yet
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFile.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_FIREFOX):
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileFirefox.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            # If running on chrome, use autoitDriver2 because it on another node
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileChrome.exe', path)
        else:
            writeToLog("INFO","FAILED to type into 'Choose File' window, unknown browser: '" + localSettings.LOCAL_RUNNING_BROWSER + "'")
        
        
    def loginAsUser(self):
        if self.base.getAppUnderTest() == enums.Application.MEDIA_SPACE:
            return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
        elif self.base.getAppUnderTest() == enums.Application.PITCH:
            return self.pitch.loginToPitch(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)        
        elif self.base.getAppUnderTest() == enums.Application.BLACK_BOARD:
            return self.blackBoard.loginToBlackBoard(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
        elif self.base.getAppUnderTest() == enums.Application.SHARE_POINT:
            return self.sharePoint.loginToSharepoint(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)      
        elif self.base.getAppUnderTest() == enums.Application.MOODLE:
            return self.moodle.loginToMoodle(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)   
        elif self.base.getAppUnderTest() == enums.Application.CANVAS:
            return self.canvas.loginToCanvas(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) 
        elif self.base.getAppUnderTest() == enums.Application.D2L:
            return self.d2l.loginToD2L(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) 
        elif self.base.getAppUnderTest() == enums.Application.JIVE:
            return self.jive.loginToJive(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) 
        elif self.base.getAppUnderTest() == enums.Application.SAKAI:
            return self.sakai.loginToSakai(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) 
        elif self.base.getAppUnderTest() == enums.Application.BLACKBOARD_ULTRA:
            return self.blackBoardUltra.loginToBlackBoardUltra(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) 
    
    
    # Author: Tzachi Guetta     
    def navigateTo(self, navigateTo, navigateFrom='', nameValue='', forceNavigate=False):
        if navigateTo == enums.Location.ENTRY_PAGE:
            if self.entryPage.navigateToEntry(nameValue, navigateFrom) == False:
                writeToLog("INFO","FAILED navigate to entry: '" + nameValue)
                return False
                
        elif navigateTo == enums.Location.EDIT_ENTRY_PAGE:
            if self.editEntryPage.navigateToEditEntry(nameValue, navigateFrom) == False:
                writeToLog("INFO","FAILED navigate to edit entry: '" + nameValue)
                return False

        elif navigateTo == enums.Location.MY_MEDIA:
            if self.myMedia.navigateToMyMedia(forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to my media")
                return False
        
        elif navigateTo == enums.Location.CHANNELS_PAGE:
            if self.channel.navigateToChannels() == False:
                writeToLog("INFO","FAILED navigate to Channels page")
                return False
            
        elif navigateTo == enums.Location.MY_CHANNELS_PAGE:
            if self.channel.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED navigate to my Channels")
                return False
            
        elif navigateTo == enums.Location.CHANNEL_PAGE:
            if self.channel.navigateToChannel(nameValue, navigateFrom) == False:
                writeToLog("INFO","FAILED navigate to Channel: " + nameValue)
                return False
            
        elif navigateTo == enums.Location.MY_PLAYLISTS:
            if self.myPlaylists.navigateToMyPlaylists(forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to my Playlists")
                return False

        elif navigateTo == enums.Location.CATEGORY_PAGE:
            if self.category.navigateToCategory(nameValue) == False:
                writeToLog("INFO","FAILED navigate to Category: " + str(nameValue))
                return False

        elif navigateTo == enums.Location.MY_HISTORY:
            if self.myHistory.navigateToMyHistory(forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to my history")
                return False
            
        elif navigateTo == enums.Location.HOME:
            if self.home.navigateToHomePage(forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to home page")
                return False      
                                                            
        return True 
    
    
    # @Author: Inbar Willman
    def writeToFile(self, path, text):
        try:
            file1 = open(path,"w")
            file1.write(text)
            file1.close()
        except:
            writeToLog("INFO","FAILED to write file: " + path + "; Text: " + text)
            return False
        return True
    
    
    # @Author: Oleg Sigalov
    def deleteFile(self, path):
        try:
            os.remove(path)
        except:
            writeToLog("INFO","FAILED to delete file: " + path)
            return False
        return True        
        
        
    # @Author: Oleg Sigalov
    # Use ONLY for linux    
    def createFolder(self, path):
        try:     
            os.makedirs(path)
            writeToLog("INFO","Created folder: " + path)
        except:
            writeToLog("INFO","FAILED to create folder: " + path)
            return False
        return True
    
    
    # @Author: Oleg Sigalov
    # Use ONLY for linux    
    def deleteFolder(self, path):
        try:     
            shutil.rmtree(path)
            writeToLog("INFO","Deleted folder: " + path)
        except:
            writeToLog("INFO","FAILED to delete folder: " + path)
            return False
        return True            
    
    
    # @Author: Oleg Sigalov
    # leavePageExpected=True if the test may fail somewhere, and Leave Page may appear.
    # we need to click leave page, because it will not continue to tearDown and other tests...
    def handleTestFail(self, status, leavePageExpected=False):
        self.switch_to_default_iframe_generic()
        if status == "Fail":
            # Get the page source
            #TODO 
            #self.base.craetePageSourceLogFile()
            # Take last screenshot
            self.base.takeScreeshotGeneric('LAST_SCRENNSHOT')
            if leavePageExpected==True:
                # Try to navigate to any place to show leave page if it was not visible
                self.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL)
                # Try to click leave page if already present
                self.base.click_leave_page()
        return True
    
                    
    # @Author: Oleg Sigalov
    # Switch to default Media Space Iframe, if testing Media Space it will switch to default_content
    # If testing KAF, it will switch to KAF Media Space Iframe
    def switch_to_default_iframe_generic(self):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MEDIA_SPACE:
            return self.base.switch_to_default_content() 
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            return self.blackBoard.switchToBlackboardIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
            return self.moodle.switchToMoodleIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
            return self.canvas.switchToCanvasIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
            return self.d2l.switchToD2LIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            return self.jive.switchToJiveIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            return self.sakai.switchToSakaiIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            return self.sharePoint.switchToSharepointIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
            return self.blackBoardUltra.switchToBlackboardUltraIframe()
        else:
            self.base.switch_to_default_content()
            
            
    def sendKeysToBodyElement(self, keys, multipleAction=1):
        for i in range(multipleAction):
            self.base.send_keys_to_element(self.base.get_body_element(), keys)
        return True
    
    
    # Check which search bar do we have: old or new (elastic)
    def isElasticSearchOnPage(self):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            return True
        if len(self.base.get_elements(self.myMedia.MY_MEDIA_ELASTIC_SEARCH_BAR)) > 1:
            return True
        else:
            return False
        
        
    # @Author: Inbar Willman
    # Compare between two files binary
    def compareBetweenTwoFilesBinary(self, path1, path2): 
        # Compare between two files
        if filecmp.cmp(path1, path2) == False:
            writeToLog("INFO","FAILED to find match between two files")
            return False      
        else:
            writeToLog("INFO","Two files are identical (binary)")
            
        writeToLog("INFO","File Path 1: '" + path1 + "'")
        writeToLog("INFO","File Path 2: '" + path2 + "'")            
        return True    
    
    
    # @Author: Horia Cus
    # This functions verifies if a file is present in the specific filePath location
    # filePath must contain the following format: os.path.join(localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS, name + ".extension")
    def verifyFilePathLocationIsValid(self, filePath):
        if os.path.isfile(filePath) == True:
            writeToLog("INFO", "The following path location is present: " + filePath )
            return True
        else:
            writeToLog("INFO", "The following path location is not present: " + filePath )
            return False       
        
        
    # @Author: Horia Cus
    # This functions verifies if a file has a minimum size
    # filePath must contain the following format: os.path.join(localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS, name + ".extension")
    def verifyMinimumSizeOfAFile(self, filePath, fileSize=1024):
        if os.path.getsize(filePath) >= fileSize:
            writeToLog("INFO", "The downloaded file has content in it")
            return True
        
        elif os.path.getsize(filePath) <= 1:
            writeToLog("INFO", "The " + filePath + " file location is empty")
            return False
        
        
    # @Author: Inbar Willman
    # Compare between two csv files
    def compareBetweenTwoCsvFiles(self, file1, file2):
        with open(file1, 'r', encoding='utf-8') as t1, open(file2, 'r', encoding='utf-8') as t2:
            fileOne = t1.readlines()
            fileTwo = t2.readlines()
 
        for line in fileTwo:
            if line not in fileOne:
                writeToLog("INFO", "FAILED: Files aren't matching")
                return False                    
            
        writeToLog("INFO", "Success: files are matching")
        return True        