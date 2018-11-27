from base import *
from general import General
import localSettings
from logger import *
from selenium.webdriver.common.keys import Keys
import enums


class KafGeneric(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    KAF_MEDIA_GALLERY_TITLE                     = ('xpath', "//h1[@id='channel_title' and text()='Media Gallery']")
    KAF_GALLERY_ADD_MEDIA_BUTTON                = ('xpath', "//a[@id='tab-addcontent']")
    KAF_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD        = ('xpath', "//a[@id='next']")
    KAF_REFRSH_BUTTON                           = ('xpath', "//a[@id='automation-reload']") 
    KAF_EMBED_FROM_MY_MEDIA_PAGE                = ('xpath', "//a[@id='media-tab']")
    KAF_EMBED_FROM_MEDIA_GALLERY_PAGE           = ('xpath', "//a[@id='MediaGalleries-tab']")
    KAF_EMBED_FROM_SR_PAGE                      = ('xpath', "//a[contains(@id,'courseGallery') and text()='Shared Repository']")
    KAF_EMBED_FROM_MEDIA_GALLERY_NAME           = ('xpath', '//a[contains(@id, "courseGallery") and text()="MEDIA_GALLERY_NAME"]')
    KAF_EMBED_SELECT_MEDIA_BTN                  = ('xpath', '//a[@class="btn btn-small btn-primary" and text()="Select"]')
    #====================================================================================================================================
    #====================================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here, switches to blackboard media space Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any method, please use switchToBlackboardIframe method, before addressing to media space elements
    # because you need to switch to blackboard media space iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method
    # to return to default iframe in the end of use of blackboard media space methods or elements, meaning in the test or other classes.
    #====================================================================================================================================

    # Author: Michal Zomper
    def navigateToGallery(self, galleryName, forceNavigate=False):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.navigateToGalleryBB(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to gallery:" + galleryName)
                return False 
        
        return True
        
    
    # Author: Michal Zomper    
    def navigateToEntryPageFromGalleryPage(self, entryName, galleryName):
        tmpEntryName = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmpEntryName, 5) != False:
            writeToLog("INFO","Already in entry page: '" + entryName + "'")
            return True
        
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED navigate to gallery:" + galleryName)
            return False             
        sleep(2)
           
        if self.clsCommon.channel.searchEntryInChannel(entryName) == False:
            writeToLog("INFO","FAILED to search entry'" + entryName + "' in gallery" + galleryName)
            return False  
            
        # click on the entry
        if self.clsCommon.myMedia.clickResultEntryAfterSearch(entryName) == False:
            writeToLog("INFO","FAILED to click on entry " + entryName)
            return False 
        
        if self.wait_visible(tmpEntryName, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
           
        return True
    
    
    
    # Author: Michal Zomper  
    # isGalleryModerate - if the user is the admin of the gallery this parameter need to be NO, if not admin need to be YES 
    def addMediaToGallery(self, galleryName, entriesNames, isGalleryModerate,  channelType=""):
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to  gallery: " +  galleryName)
            return False
        
        if self.click(self.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to gallery button")
            return False           
        
        sleep(1)
        self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
        
#         if channelType == enums.ChannelPrivacyType.SHAREDREPOSITORY:
#             # open shared repository list
#             if self.click(self.CHANNEL_ADD_CONTENT_FOR_SHAREDREPOSITORY) == False:
#                 writeToLog("INFO","FAILED to open shared repository channels list")
#                 return False
#             
#             #chose shared repository channel 
#             tmpSharedRepositoryChannel = (self.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[0], self.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[1].replace('CHANNEL_NAME', sharedReposiytyChannel))
#             if self.click(tmpSharedRepositoryChannel) == False:
#                 writeToLog("INFO","FAILED to select channel '" + sharedReposiytyChannel + "' as the shared repository channel to add content from")
#                 return False
#             self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
            
        if self.addContentFromMyMedia(entriesNames) == False:
            writeToLog("INFO","FAILED to publish entries to gallery: " + galleryName)
            return False
            
        published = False
        
        if isGalleryModerate == True:
            if self.wait_visible(self.CHANNEL_MODARATE_PUBLISH_MSG, 30) != False:
                published = True
        else:
            if self.wait_visible(self.CHANNEL_PUBLISH_MSG, 30) != False:
                published = True
        
        if published == True:
            if type(entriesNames) is list: 
                entries = ", ".join(entriesNames)
                writeToLog("INFO","The following entries were published: " + entries + "")
            else:
                writeToLog("INFO","The following entry was published: " + entriesNames + "")
        else:
            if isGalleryModerate == True:
                writeToLog("INFO","Publish to gallery: confirmation massage was not presented")
                return False
            else:
                writeToLog("INFO","Publish to moderate gallery: confirmation massage was not presented")
                return False
        
        writeToLog("INFO","Success, Entries were added to gallery")   
        return True
    
    
    # Author: Michal Zomper
    # The function perform upload to new media from gallery page
    # each item in uploadEntrieList need to have to value from type  "UploadEntry":  
    # UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    # if we need only 1 upload we can set :self.entry1 = UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3) 
    # and pass only self.entry1
    # if we need to upload more then 1 entry we need to pass a list of UploadEntry : self.uploadEntrieList = [self.entry1, self.entry2,....]
    # isGalleryModerate - if the user is the admin of the gallery this parameter need to be NO, if not admin need to be YES 
    def addNewContentToGallery(self, galleryName, uploadEntrieList, isGalleryModerate=''):
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED navigate to gallery: " + galleryName)
            return False
        
        if type(uploadEntrieList) is list:
            for entry in uploadEntrieList:
                if self.addNewContentToGalleryWithoutNavigate(entry, isGalleryModerate) == False:
                    writeToLog("INFO","FAILED to upload new media to gallery")
                    return False 
                sleep(2)
        else:
            if self.addNewContentToGalleryWithoutNavigate(uploadEntrieList, isGalleryModerate) == False:
                writeToLog("INFO","FAILED to upload new media to gallery")
                return False  
        
            published = False
        
            if isGalleryModerate == True:
                if self.wait_visible(self.CHANNEL_MODARATE_PUBLISH_MSG, 30) != False:
                    published = True
            else:
                if self.wait_visible(self.CHANNEL_PUBLISH_MSG, 30) != False:
                    published = True
            
            if published == True:
                writeToLog("INFO","The following entry was published")
                    
            else:
                if isGalleryModerate == True:
                    writeToLog("INFO","Publish to gallery: confirmation massage was not presented")
                    return False
                else:
                    writeToLog("INFO","Publish to moderate gallery: confirmation massage was not presented")
                    return False
        
        writeToLog("INFO","Success, media was added to gallery successfully")
        return True
    
    
    # Author: Michal Zomper
    #UploadEntry parameter need to have : UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    def addNewContentToGalleryWithoutNavigate(self, uploadEntry, isGalleryModerate=''):
        if self.click(self.KAF_GALLERY_ADD_MEDIA_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to Gallery button")
            return False     
        sleep(4)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New at gallery page")
            return False
        sleep(2)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New -> Media upload, at gallery page")
            return False
        sleep(3)
        
        if self.clsCommon.upload.uploadEntry(uploadEntry.filePath, uploadEntry.name, uploadEntry.description, uploadEntry.tags, uploadEntry.timeout,retries=1,  uploadFrom=None, verifyModerationWarning=isGalleryModerate) == False:
            writeToLog("INFO","FAILED to upload media from gallery page: " + uploadEntry.name)
            return False
        
        # Click 'Go To media gallery'
        if self.click(self.KAF_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'Go To gallery'")
            return False
        
        return True
    
    
    def handlePendingEntriesIngallery(self, galleryName, toRejectEntriesNames, toApproveEntriesNames , navigate=True):
        if navigate == True:
            if self.navigateToGallery(galleryName) == False:
                writeToLog("INFO","FAILED navigate to  gallery: " +  galleryName)
                return False
            
            if self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on gallery moderation tab")
                return False        
        
        sleep(2)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30) 
        
        if self.clsCommon.channel.approveEntriesInPandingTab(toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED to approve entries")
            return False  
        
        self.click(self.KAF_REFRSH_BUTTON)
        sleep(6)
        self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, timeout=60, multipleElements=True)
        sleep(2)
        
        if self.clsCommon.channel.rejectEntriesInPandingTab(toRejectEntriesNames) == False:
            writeToLog("INFO","FAILED to reject entries")
            return False
        
        # verify that entry approve/ rejected in gallery 
        if self.navigateToGallery(galleryName, forceNavigate=True) == False:
            writeToLog("INFO","FAILED navigate to  gallery: " +  galleryName)
            return False

        if self.clsCommon.channel.verifyEntriesApprovedAndRejectedInChannelOrGallery(toRejectEntriesNames, toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED, not all entries was approved/ rejected as needed")
            return False 
        
        return True  
    
    
    # @Author: Inbar Willman
    # To Do
    def embedMedia(self, entryName, mediaGalleryName='', embedFrom=enums.Location.MY_MEDIA):
        if embedFrom == enums.Location.MY_MEDIA:
            if self.click(self.KAF_EMBED_FROM_MY_MEDIA_PAGE) == False:
                writeToLog("INFO","FAILED to click on embed from my media tab")
                return False  
              
        elif embedFrom == enums.Location.SHARED_REPOSITORY:   
            if self.click(self.KAF_EMBED_FROM_SR_PAGE) == False:    
                writeToLog("INFO","FAILED to click on embed from SR tab")
                return False        
        
        elif embedFrom == enums.Location.MEDIA_GALLARY: 
            if self.click(self.KAF_EMBED_FROM_MEDIA_GALLERY_PAGE) == False:
                writeToLog("INFO","FAILED to click on embed from media gallery tab")
                return False   
            
            tmpMediaGallery = (self.KAF_EMBED_FROM_MEDIA_GALLERY_NAME[0], self.KAF_EMBED_FROM_MEDIA_GALLERY_NAME[1].replace('MEDIA_GALLERY_NAME', mediaGalleryName))          
            if self.click(tmpMediaGallery) == False:
                writeToLog("INFO","FAILED to click on media gallery name in dropdown")
                return False 
            
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to make a search in embed page")
            return False 
        
        if self.click(self.KAF_EMBED_SELECT_MEDIA_BTN) == False:
            writeToLog("INFO","FAILED to click on 'select' media button")
            return False
        
        return True   