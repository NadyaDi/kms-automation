import subprocess
from symbol import except_clause

import win32com.client  

from base import *
import clsTestService
from general import General

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



class Channel(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #                                   Channel locators:                                                        #
    #=============================================================================================================
    MY_CHANNELS_CREATE_CHANNEL_BUTTON               = ('id', 'createChannelBtn')
    CHANNEL_DETAILS_NAME_FIELD                      = ('id', 'Category-name')
    CHANNEL_DETAILS_CHANNEL_TAGS                    = ('id', 's2id_tags')
    CHANNEL_DETAILS_PRIVACY_OPEN                    = ('xpath', "//strong[contains(text(),'Open')]")
    CHANNEL_DETAILS_PRIVACY_RESTRICTED              = ('xpath', "//strong[contains(text(),'Restricted')]")
    CHANNEL_DETAILS_PRIVACY_PRIVATE                 = ('xpath', "//strong[contains(text(),'Private')]")
    CHANNEL_DETAILS_PRIVACY_SHARED_REPOSITORY       = ('xpath', "//strong[contains(text(),'Shared Repository')]")
    CHANNEL_DETAILS_PRIVACY_PUBLIC                  = ('xpath', "//strong[contains(text(),'Public')]")
    CHANNEL_DETAILS_OPTION_MODARATE                 = ('id', 'Category-options-moderation')
    CHANNEL_DETAILS_OPTION_COMMENT                  = ('id', 'Category-options-enableComments')
    CHANNEL_DETAILS_OPTION_SUBSCRIPTION             = ('id', 'Category-options-enableChannelSubscription')
    CHANNEL_SAVE_BUTTON                             = ('id', 'Category-submit')
    CHANNEL_CREATION_DONE                           = ('xpath', "//h1[@id='channel_title_edit']")
    MY_CHANNELS_SERACH_FIELD                        = ('id', 'searchBar')
    MY_CHANNELS_EDIT_BUTTON                         = ('xpath', "//a[contains(@class,'edit')]")
    MY_CHANNELS_HOVER                               = ('xpath', "//*[@class='channel_content' and contains(text(), 'CHANNEL_NAME')]")
    EDIT_CHANNEL_DELETE                             = ('xpath', "//*[contains(.,'Delete Channel')]")
    EDIT_CHANNEL_DELETE_CONFIRM                     = ('xpath', "//a[contains(.,'Delete')]")
    #============================================================================================================
    def deleteChannel(self, channelName):
        try:
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            
            if self.click(self.MY_CHANNELS_SERACH_FIELD) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, channelName) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            
            sleep(1)
            self.clsCommon.general.waitForLoaderToDisappear()
            
            tmp_entry_name = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', channelName))
            element = self.get_element(tmp_entry_name)
            hover = ActionChains(self.driver).move_to_element(element)
            
            if hover.perform() == False:
                writeToLog("INFO","FAILED to Hover above Channel's thumbnail")
                return False
    
            sleep(1)
            if self.click(self.MY_CHANNELS_EDIT_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Edit channel button")
                return False
            
            if self.click(self.EDIT_CHANNEL_DELETE) == False:
                writeToLog("INFO","FAILED to click on Delete channel button")
                return False
            
            if self.click(self.EDIT_CHANNEL_DELETE_CONFIRM) == False:
                writeToLog("INFO","FAILED to click on Delete confirmation button")
                return False
            
            sleep(2)
        except NoSuchElementException:
            return False
        
        return True


    # This function will create a Channel, please follow the following instructions:
    # in order to choose the Channel's privacy please use one of the following values ONLY: open , restricted , private , shared-repository , public
    # for isModarated, isCommnets, isSubscription - use boolean
    # TODO: linkToCategoriesList
    def createChannel(self, channelName, channelDescription, channelTags, privacyType, isModarated, isCommnets, isSubscription, linkToCategoriesList):
        try:
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to native to my channels page")
                return False
            if self.click(self.MY_CHANNELS_CREATE_CHANNEL_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Create channel button")
                return False
            
            # Starting filling channel Data
            if self.click(self.CHANNEL_DETAILS_NAME_FIELD) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            if self.send_keys(self.CHANNEL_DETAILS_NAME_FIELD, channelName) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            if self.clsCommon.upload.fillFileUploadEntryDescription(channelDescription) == False:
                writeToLog("INFO","FAILED to type in 'description' text field")
                return False
            if self.fillChannelTags(channelTags) == False:
                writeToLog("INFO","FAILED to type in 'Tags' field")
                return False
            if self.selectChannelPrivacy(privacyType) == False:
                writeToLog("INFO","FAILED to Choose Channel privacy")
                return False
            
            # Checking Channel options
            if isModarated == True:
                if self.click(self.CHANNEL_DETAILS_OPTION_MODARATE, 30) == False:
                    writeToLog("INFO","FAILED to click on Moderate checkbox")
                    return False
 
            if isCommnets == False:
                if self.click(self.CHANNEL_DETAILS_OPTION_COMMENT, 30) == False:
                    writeToLog("INFO","FAILED to click on comments checkbox")
                    return False
                
            if isSubscription == True:
                if self.click(self.CHANNEL_DETAILS_OPTION_SUBSCRIPTION, 30) == False:
                    writeToLog("INFO","FAILED to click on subscription checkbox")
                    return False  
            
            if self.click(self.CHANNEL_SAVE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Save button")
                return False 
            
            if self.wait_visible(self.CHANNEL_CREATION_DONE, 30) == False:
                writeToLog("INFO","FAILED to create a Channel")
                return False                                        
            else:
                writeToLog("INFO","Channel successfully created")
                
        except NoSuchElementException:
            return False
        
        return True
        
        
    def navigateToMyChannels(self):
        # Check if we are already in my Channels page
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL, False) == True:
            writeToLog("INFO","Already in my Channels page")
            return True     
           
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Channels
        if self.click(self.clsCommon.general.USER_MENU_MY_CHANNELS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on My Channels from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My Channels")
            return False
        
        return True
       
       
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillChannelTags(self, tags):
        try:
            self.switch_to_default_content()
            tagsElement = self.get_element(self.CHANNEL_DETAILS_CHANNEL_TAGS)
            
        except NoSuchElementException:
            writeToLog("DEBUG","FAILED to get Tags filed element")
            return False
                
        if tagsElement.click() == False:
            writeToLog("DEBUG","FAILED to click on Tags filed")
            return False            
        sleep(2)
        
        if self.send_keys(self.CHANNEL_DETAILS_CHANNEL_TAGS, tags) == True:
            return True
        else:
            writeToLog("DEBUG","FAILED to type in Tags")
            return False
        
        
    def selectChannelPrivacy(self, privacy):
        if privacy == "open":
            if self.click(self.CHANNEL_DETAILS_PRIVACY_OPEN) == False:
                writeToLog("INFO","FAILED to click on open option")
                return False
            
        elif privacy == "restricted":
            if self.click(self.CHANNEL_DETAILS_PRIVACY_RESTRICTED) == False:
                writeToLog("INFO","FAILED to click on restricted option")
                return False
            
        elif privacy == "private":
            if self.click(self.CHANNEL_DETAILS_PRIVACY_PRIVATE) == False:
                writeToLog("INFO","FAILED to click on private option")
                return False
            
        elif privacy == "sharedrepository":
            if self.click(self.CHANNEL_DETAILS_PRIVACY_SHARED_REPOSITORY) == False:
                writeToLog("INFO","FAILED to click on shared-repository option")
                return False
            
        elif privacy == "public":
            if self.click(self.CHANNEL_DETAILS_PRIVACY_PUBLIC) == False:
                writeToLog("INFO","FAILED to click on public option")
                return False  
        else:
            writeToLog("DEBUG","FAILED to choose Channel privacy")
            return False
        
        return True