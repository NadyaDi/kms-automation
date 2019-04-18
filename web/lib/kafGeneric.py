from base import *
from general import General
import localSettings
from logger import *
from selenium.webdriver.common.keys import Keys
import enums
from email.mime import application


class KafGeneric(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
        
    #=================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    KAF_MEDIA_GALLERY_TITLE                         = ('xpath', "//h1[@id='channel_title' and text()='Media Gallery']")
    KAF_GALLERY_ADD_MEDIA_BUTTON                    = ('xpath', "//a[@id='tab-addcontent']")
    KAF_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD            = ('xpath', "//a[@id='next' and contains(text(), 'Go To Media Gallery')]")
    KAF_REFRSH_BUTTON                               = ('xpath', "//a[@id='automation-reload']") 
    KAF_EMBED_FROM_MY_MEDIA_PAGE                    = ('xpath', "//a[@id='media-tab']")
    KAF_EMBED_FROM_MEDIA_GALLERY_PAGE_MULTIPLE      = ('xpath', "//a[@id='MediaGalleries-tab']")
    KAF_EMBED_FROM_SR_PAGE                          = ('xpath', "//a[contains(@id,'courseGallery') and text()='Shared Repository']")
    KAF_EMBED_FROM_MEDIA_GALLERY_NAME               = ('xpath', '//a[contains(@id, "courseGallery") and text()="MEDIA_GALLERY_NAME"]')
#    KAF_EMBED_SELECT_MEDIA_BTN                     = ('xpath', '//div[@class="btn-group singleSizeButton pull-right"]')
    KAF_EMBED_SELECT_MEDIA_BTN                      = ('xpath', '//a[contains(@aria-label, "ENTRY_NAME") and text()="Select"]')
    KAF_EMBED_RESULT_AFTER_SEARCH                   = ('xpath', '//em[text()="ENTRY_NAME"]/ancestor::td[contains(@id,"eSearch-result-")]')
    KAF_EMBED_EMBED_MEDIA_BTN                       = ('xpath', "//a[contains(@class,'embed-button') and contains(@href,'ENTRY_ID')]")
    KAF_EMBED_FROM_MEDIA_GALLERY_PAGE_SINGLE        = ('xpath', "//a[@data-original-title='Media Gallery']")
    KAF_SAVE_AND_EMBED_UPLOAD_MEDIA                 = ('xpath', '//button[@data-original-title="Save and Embed"]')  
    KAF_EMBED_TITLE_AFTER_CREATE_EMBED              = ('xpath', '//span[contains(text(), "EMBED_TITLE")]')
    KAF_GRID_VIEW                                   = ('xpath', "//button[@id='MyMediaGrid']")
    KAF_SR_ENTRY_CHECKBOX                           = ('xpath', '//input[@type="checkbox" and @title="ENTRY_NAME"]')
    KAF_EMBED_LOADING_MESSAGE                       = ('xpath', '//div[@class="elementLoader"]')
    KAF_CLEAR_SREACH_ICON                           = ('xpath', "//i[@class='v2ui-close-icon']")
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
    
    def navigateToMyMediaKAF(self): 
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
            if self.clsCommon.canvas.navigateToMyMediaCanvas() == False:
                writeToLog("INFO","FAILED navigate to My Media")
                return False   
            
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            if self.clsCommon.sakai.navigateToMyMediaSakai() == False:
                writeToLog("INFO","FAILED navigate to My Media")
                return False 
    
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
            if self.clsCommon.blackBoardUltra.navigateToMyMediaBlackboardUltra() == False:
                writeToLog("INFO","FAILED navigate to My Media")
                return False     
       
        else: 
            if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
                writeToLog("INFO","FAILED navigate to My Media")
                return False
            
            if self.switchToKAFIframeGeneric()== False:
                writeToLog("INFO","FAILED switch to iframe")
                return False
            
            self.wait_element(self.clsCommon.upload.UPLOAD_MENU_DROP_DOWN_ELEMENT, timeout=20)
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 30) == False:
                writeToLog("INFO","FAILED navigate to My Media")
                return False
         
        return True


    def switchToKAFIframeGeneric(self):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.switchToBlackboardIframe() == False:
                writeToLog("INFO","FAILED to switch to blackboard iframe")
                return False
        
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
            if self.clsCommon.moodle.switchToMoodleIframe() == False:
                writeToLog("INFO","FAILED to switch to moodle iframe")
                return False
        
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            if self.clsCommon.sharePoint.switchToSharepointIframe() == False:
                writeToLog("INFO","FAILED to switch to sharepoint iframe")
                return False
            
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
            if self.clsCommon.canvas.switchToCanvasIframe() == False:
                writeToLog("INFO","FAILED to switch to canvas iframe")
                return False
    
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
            if self.clsCommon.d2l.switchToD2LIframe() == False:
                writeToLog("INFO","FAILED to switch to canvas iframe")
                return False
            
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            if self.clsCommon.jive.switchToJiveIframe()== False:
                writeToLog("INFO","FAILED to switch to canvas iframe")
                return False

        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            if self.clsCommon.sakai.switchToSakaiIframe()== False:
                writeToLog("INFO","FAILED to switch to sakai iframe")
                return False
        
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            if self.clsCommon.sharePoint.switchToSharepointIframe() == False:
                writeToLog("INFO","FAILED to switch to share point iframe")
                return False

        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
            if self.clsCommon.blackBoardUltra.switchToBlackboardUltraIframe() == False:
                writeToLog("INFO","FAILED to switch to blackboard ultra iframe")
                return False
        
        return True
    
    
    def navigateToUploadPageKAF(self):
        if self.navigateToMyMediaKAF() == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        if self.switchToKAFIframeGeneric() == False:
            writeToLog("INFO","FAILED switch to iframe")
            return False
        
        return True
    

    # Author: Michal Zomper
    def navigateToGallery(self, galleryName, forceNavigate=False):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.navigateToGalleryBB(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to gallery:" + galleryName)
                return False 
            
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
            if self.clsCommon.moodle.navigateToGalleryMoodle(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to gallery:" + galleryName)
                return False 
            
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
            if self.clsCommon.canvas.navigateToGalleryCanvas(forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False 
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
            if self.clsCommon.d2l.navigateToGalleryD2L(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False   
            
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            if self.clsCommon.jive.navigateToGalleryJive(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False 
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            if self.clsCommon.sakai.navigateToGallerySakai(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False 

        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            if self.clsCommon.sharePoint.navigateToGallerySharePoint(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False 
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
            if self.clsCommon.blackBoardUltra.navigateToGalleryBlackBoardUltra(galleryName, forceNavigate) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False 
            
        return True
        
    
    # Author: Michal Zomper    
    def navigateToEntryPageFromGalleryPage(self, entryName, galleryName, forceNavigate=False):
        self.switchToKAFIframeGeneric() 
        tmpEntryName = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_element(tmpEntryName, 5) != False:
            writeToLog("INFO","Already in entry page: '" + entryName + "'")
            return True
        
        if self.navigateToGallery(galleryName, forceNavigate) == False:
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
        
        if self.wait_element(tmpEntryName, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
           
        return True
    
    
    
    # Author: Michal Zomper  
    # This function add media to gallery from the gallery page, clicking on add new and them choosing from my media entries
    # isGalleryModerate - if the user is the admin of the gallery this parameter need to be NO, if not admin need to be YES 
    def addMediaToGallery(self, galleryName, entriesNames, isGalleryModerate):
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to  gallery: " +  galleryName)
            return False
        
        if self.click(self.clsCommon.channel.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to gallery button")
            return False           
        
        sleep(1)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)
            
        if self.clsCommon.channel.addContentFromMyMedia(entriesNames) == False:
            writeToLog("INFO","FAILED to publish entries to gallery: " + galleryName)
            return False
            
        published = False
        
        if isGalleryModerate == True:
            if self.wait_visible(self.clsCommon.channel.CHANNEL_MODARATE_PUBLISH_MSG, 30) != False:
                published = True
        else:
            if self.wait_visible(self.clsCommon.channel.CHANNEL_PUBLISH_MSG, 30) != False:
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
                if self.addNewContentToGalleryWithoutNavigate(galleryName, entry, isGalleryModerate) == False:
                    writeToLog("INFO","FAILED to upload new media to gallery")
                    return False 
                sleep(2)
        else:
            if self.addNewContentToGalleryWithoutNavigate(galleryName, uploadEntrieList, isGalleryModerate) == False:
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
    def addNewContentToGalleryWithoutNavigate(self, galleryName, uploadEntry, isGalleryModerate=''):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
            self.clsCommon.blackBoardUltra.switchToBlackboardUltraIframe() 
                      
        if self.click(self.KAF_GALLERY_ADD_MEDIA_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click add to Gallery button")
            return False     
        sleep(4)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on Add New at gallery page")
            return False
        sleep(2)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New -> Media upload, at gallery page")
            return False
        sleep(3)
        
        if self.clsCommon.upload.uploadEntry(uploadEntry.filePath, uploadEntry.name, uploadEntry.description, uploadEntry.tags, uploadEntry.timeout,retries=1,  uploadFrom=None, verifyModerationWarning=isGalleryModerate) == None:
            writeToLog("INFO","FAILED to upload media from gallery page: " + uploadEntry.name)
            return False
        sleep(10)
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            self.click(self.clsCommon.upload.UPLOAD_PAGE_TITLE)
            self.get_body_element().send_keys(Keys.PAGE_DOWN) 
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            if self.navigateToGallery(galleryName) == False:
                writeToLog("INFO","FAILED navigate to media gallery")
                return False
        else:
            # Click 'Go To media gallery'
            if self.click(self.KAF_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on 'Go To gallery'")
                return False
        sleep(5)
        return True
    
    
    def handlePendingEntriesIngallery(self, galleryName, toRejectEntriesNames, toApproveEntriesNames , navigate=True):
        if navigate == True:
            if self.navigateToGallery(galleryName) == False:
                writeToLog("INFO","FAILED navigate to  gallery: " +  galleryName)
                return False
            
            if self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on gallery moderation tab")
                return False        
        
        sleep(4)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30) 
        self.clsCommon.channel.showAllEntriesPendingTab()
        if len(toApproveEntriesNames) != 0:
            if self.clsCommon.channel.approveEntriesInPandingTab(toApproveEntriesNames) == False:
                writeToLog("INFO","FAILED to approve entries")
                return False  
        
        if len(toRejectEntriesNames) != 0:
            if self.wait_element(self.KAF_CLEAR_SREACH_ICON,  multipleElements=True) == True:
                self.click(self.KAF_CLEAR_SREACH_ICON, multipleElements=True)
                self.clsCommon.general.waitForLoaderToDisappear()
                self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, multipleElements=True)
                
            self.clsCommon.channel.showAllEntriesPendingTab()
            self.click(self.KAF_REFRSH_BUTTON, multipleElements=True)
            sleep(4)
            self.click(self.KAF_GRID_VIEW)
            self.get_body_element().send_keys(Keys.PAGE_UP)
            sleep(2)
            self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, timeout=60, multipleElements=True)
            sleep(2)
            self.clsCommon.channel.showAllEntriesPendingTab()
            if self.clsCommon.channel.rejectEntriesInPandingTab(toRejectEntriesNames) == False:
                writeToLog("INFO","FAILED to reject entries")
                return False
        
        # verify that entry approve/ rejected in gallery 
        if self.navigateToGallery(galleryName, forceNavigate=True) == False:
            writeToLog("INFO","FAILED navigate to  gallery: " +  galleryName)
            return False
        
        self.click(self.clsCommon.kafGeneric.KAF_REFRSH_BUTTON)
        if self.clsCommon.channel.verifyEntriesApprovedAndRejectedInChannelOrGallery(toRejectEntriesNames, toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED, not all entries was approved/ rejected as needed")
            return False 
        
        return True  
    
    
    # @Author: Inbar Willman
    # Before and after calling this function need to call switch window
    def embedMedia(self, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None, application=enums.Application.BLACK_BOARD, activity=enums.MoodleActivities.SITE_BLOG, isAssignmentEnable=False, submitAssignment=False, isTagsNeeded=True, isGradebook=False):
        if application == enums.Application.MOODLE:
            if activity == enums.MoodleActivities.SITE_BLOG:
                self.clsCommon.base.swith_to_iframe(self.clsCommon.moodle.MOODLE_EMBED_IFRAME)
                
        sleep(10)
          
        if self.wait_element(self.KAF_EMBED_FROM_MY_MEDIA_PAGE, timeout=60) == False:
                writeToLog("INFO","FAILED to display embed page")
                return False  
                        
        if embedFrom == enums.Location.MY_MEDIA:
            if self.click(self.KAF_EMBED_FROM_MY_MEDIA_PAGE) == False:
                writeToLog("INFO","FAILED to click on embed from my media tab")
                return False  
              
        elif embedFrom == enums.Location.SHARED_REPOSITORY:   
            if self.click(self.KAF_EMBED_FROM_SR_PAGE) == False:    
                writeToLog("INFO","FAILED to click on embed from SR tab")
                return False        
        
        elif embedFrom == enums.Location.MEDIA_GALLARY:
            if chooseMediaGalleryinEmbed == True:
                if self.click(self.KAF_EMBED_FROM_MEDIA_GALLERY_PAGE_MULTIPLE) == False:
                    writeToLog("INFO","FAILED to click on embed from media gallery tab")
                    return False   
            
                tmpMediaGallery = (self.KAF_EMBED_FROM_MEDIA_GALLERY_NAME[0], self.KAF_EMBED_FROM_MEDIA_GALLERY_NAME[1].replace('MEDIA_GALLERY_NAME', mediaGalleryName))          
                if self.click(tmpMediaGallery) == False:
                    writeToLog("INFO","FAILED to click on media gallery name in dropdown")
                    return False 
            else:
                if self.click(self.KAF_EMBED_FROM_MEDIA_GALLERY_PAGE_SINGLE) == False:
                    writeToLog("INFO","FAILED to click on embed from media gallery tab")
                    return False 
                
                self.clsCommon.general.waitForLoaderToDisappear()
                
        elif embedFrom == enums.Location.UPLOAD_PAGE_EMBED:
            # Upload entry
            if self.clsCommon.upload.uploadEntry(filePath, entryName, description, tags, uploadFrom=enums.Location.UPLOAD_PAGE_EMBED, isTagsNeeded=isTagsNeeded) == None:
                writeToLog("INFO","FAILED to upload new entry to embed page embed page")
                return False  
            
            sleep(3)
            
            # Click Save and embed
            if self.click(self.KAF_SAVE_AND_EMBED_UPLOAD_MEDIA) == False:
                writeToLog("INFO","FAILED to click on save and embed button")
                return False 
            
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
                self.switch_to_default_content()  
            
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.switch_to_default_content()
                self.swith_to_iframe(self.clsCommon.d2l.D2L_INSERT_STUFF_IFRAME)
                
                if self.wait_element(self.clsCommon.d2l.D2L_EMBED_INSERT_BTN, timeout=15) == False:
                    writeToLog("INFO","FAILED to displayed 'insert' button")
                    return False                  
                if self.click(self.clsCommon.d2l.D2L_EMBED_INSERT_BTN) == False:
                    writeToLog("INFO","FAILED to click on 'insert' button")
                    return False  
            
            sleep(2)
            self.clsCommon.general.waitForLoaderToDisappear() 
            
            return True   
        
        self.wait_while_not_visible(self.KAF_EMBED_LOADING_MESSAGE, 80)                             
            
        if self.searchInEmbedPage(entryName, embedPage=embedFrom) == False:
            writeToLog("INFO","FAILED to make a search in embed page")
            return False 
        
        # Get an element witch contains the entry name
        tmpResult = (self.KAF_EMBED_RESULT_AFTER_SEARCH[0], self.KAF_EMBED_RESULT_AFTER_SEARCH[1].replace('ENTRY_NAME', entryName))
        entryElement = self.wait_element(tmpResult)
        if entryElement == False:
            writeToLog("INFO","FAILED to get after search result element")
            return False        
        
        # Get the entry ID from the element
        entryId = entryElement.get_attribute("id").split('-')[2]
        tmpSelectBtn = (self.KAF_EMBED_EMBED_MEDIA_BTN[0], self.KAF_EMBED_EMBED_MEDIA_BTN[1].replace('ENTRY_ID', entryId))
        
        # Use the entry ID to click on the '</> Embed' button
        if self.click(tmpSelectBtn, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on the '</> Embed' button")
            return False
        
#        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(10)
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
            if isAssignmentEnable == True:
                if submitAssignment == True:
                    if self.clsCommon.moodle.submitMediaAsAssignment(True) == False:
                        writeToLog("INFO","FAILED to create embed as assignment submission")
                        return False
                else:
                    if self.clsCommon.moodle.submitMediaAsAssignment(False) == False:
                        writeToLog("INFO","FAILED to create embed not as assignment submission")
                        return False 
                    
                self.clsCommon.general.waitForLoaderToDisappear()
                                                               
            if activity == enums.MoodleActivities.SITE_BLOG:
                sleep(5)
                self.switch_to_default_content()
                if self.click(self.clsCommon.moodle.MOODLE_EMBED_BTN) == False:
                    writeToLog("INFO","FAILED to click on 'embed' button")
                    return False    
                
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
            if isGradebook == False:
                sleep(5)
                self.switch_to_default_content()
                self.swith_to_iframe(self.clsCommon.d2l.D2L_INSERT_STUFF_IFRAME)
            
                if self.click(self.clsCommon.d2l.D2L_EMBED_INSERT_BTN) == False:
                    writeToLog("INFO","FAILED to click on 'insert' button")
                    return False                               
        
        return True   
    
    
    # @Author: Inbar Willman
    # Make a search in embed page
    def searchInEmbedPage(self, entryName, exactSearch=False, embedPage = enums.Location.MY_MEDIA):
        if self.clsCommon.isElasticSearchOnPage():    
            searchBarElement = self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_ELASTIC_SEARCH_BAR, multipleElements=True)
        else:
            searchBarElement = self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_SEARCH_BAR, multipleElements=True)
            
        if searchBarElement == False:
            writeToLog("INFO","FAILED to get search bar element")
            return False         

        searchBarElement.click()
        
        if exactSearch == True:
            searchLine = '"' + entryName + '"'
        else:
            if self.clsCommon.isElasticSearchOnPage():
                searchLine = '"' + entryName + '"'
            else:
                searchLine = entryName
            
        searchBarElement.send_keys(searchLine + Keys.ENTER)
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True      

    
    # @Author: Oleg Sigalov
    # Verify embed entry generic
    # 'imageThumbnail'' is the expecterQrCode of embed image - when the value different then '', means that the type is image
    # 'imageThumbnail' is the expecterQrCode of embed video - when the value different then '', means that the type is video
    # 'activity' is relevant just for moodle KAF
    def verifyEmbedEntry(self, embedTitle, imageThumbnail='', delay='', application=enums.Application.BLACK_BOARD, activity=enums.MoodleActivities.SITE_BLOG, forceNavigate=False, isQuiz=False):
        if application == enums.Application.BLACK_BOARD:
            return self.clsCommon.blackBoard.verifyBlackboardEmbedEntry(embedTitle, imageThumbnail, delay, isQuiz)
        elif application == enums.Application.MOODLE:
            return self.clsCommon.moodle.verifyMoodleEmbedEntry(embedTitle, imageThumbnail, delay, activity, forceNavigate, isQuiz)
        elif application == enums.Application.CANVAS:
            return self.clsCommon.canvas.verifyCanvasEmbedEntry(embedTitle, imageThumbnail, delay, forceNavigate, isQuiz)
        elif application == enums.Application.D2L:
            return self.clsCommon.d2l.verifyD2lEmbedEntry(embedTitle, imageThumbnail, delay, forceNavigate, isQuiz)
#         elif application == enums.Application.JIVE:
#             return self.clsCommon.jive.verifyJiveEmbedEntry(embedTitle, imageThumbnail, delay, forceNavigate, isQuiz)                       
        else:
            writeToLog("INFO","FAILED unknown application: " + application.value)   
            return False
        
        return True     
    
    
    # @Author: Inbar Willman
    # Add media to media gallery from SR
    def addSharedRepositoryMedieToMediaGallery(self, galleryName, entriesNames):
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to  gallery: " +  galleryName)
            return False
            
        if self.addContentFromSR(entriesNames) == False:
            writeToLog("INFO","FAILED to publish entries to media gallery: " + galleryName)
            return False    
        
        writeToLog("INFO","Success to publish entry from SR tab to: " + galleryName)
        return True    
    
    
    # @Author: Inbar Willman
    def addContentFromSR(self, entriesNames):   
        # Checking if entriesNames list type
        if type(entriesNames) is list: 
            for entryName in entriesNames:
                if self.clickAddMediaAndSharedRepository() == False:
                    writeToLog("INFO","FAILED to open shared repository section")
                    return False
                
                if self.checkSingleEntryInSharedRepository(entryName, withSearch=True) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entryName + ", At add content -> my media flow")
                    return False
                
                writeToLog("INFO","Going to publish Entry: " + entryName)
                if self.clickPublishAndWaitForLoaderToDisappear() == False:
                    return False   
                writeToLog("INFO","Entry: '" + entryName + "' was published successfully")
            return True

        # Single entry
        else:
            if self.clickAddMediaAndSharedRepository() == False:
                writeToLog("INFO","FAILED to open shared repository section")
                return False  
                          
            if self.checkSingleEntryInSharedRepository(entriesNames) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entriesNames + ", At add content -> my media flow")
                    return False
                
            writeToLog("INFO","Going to publish Entry: " + entriesNames)
            
        if self.clickPublishAndWaitForLoaderToDisappear() == False:
            return False             
        
        # Single entry log
        writeToLog("INFO","Entry: '" + entriesNames + "' was published successfully")
        return True    
    
    
    # @Author: Oleg Sigalov
    # Method flow: Click Add Media, Click on shared repository menu, Click shared repository dropdown
    def clickAddMediaAndSharedRepository(self):
        if self.click(self.clsCommon.channel.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to gallery button")
            return False           
        
        sleep(1)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)   
        
        # open shared repository list
        if self.click(self.clsCommon.channel.CHANNEL_ADD_CONTENT_FOR_SHAREDREPOSITORY) == False:
            writeToLog("INFO","FAILED to click on Shared repository tab")
            return False
        
        #chose shared repository channel 
        tmpSharedRepositoryChannel = (self.clsCommon.channel.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[0], self.clsCommon.channel.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[1].replace('CHANNEL_NAME', "Shared Repository"))
        if self.click(tmpSharedRepositoryChannel) == False:
            writeToLog("INFO","FAILED to select Shared repository option in dropdown")
            return False
        
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)
        return True
    
        
    # @Author: Oleg Sigalov
    def clickPublishAndWaitForLoaderToDisappear(self):
        if self.click(self.clsCommon.channel.CHANNEL_PUBLISH_BUTTON) == False:
            writeToLog("INFO","FAILED to CHECK the entry, At add content -> my media flow")
            return False             
        
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True        
    
    
    # @Author: Inbar Willman
    def checkSingleEntryInSharedRepository(self, entryName, withSearch=False):
        if withSearch == True:
            self.clsCommon.channel.searchInAddToChannel(entryName, tabToSearcFrom=enums.AddToChannelTabs.SHARED_REPOSITORY)
        # Click on the Entry's check-box in MyMedia page
        tmp_entry_name = (self.KAF_SR_ENTRY_CHECKBOX[0], self.KAF_SR_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
                
        if self.click(tmp_entry_name, multipleElements=True) == False:
            # If entry not found, search for 'No Entries Found' alert
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        return True   
    
    
    # Author: Michal Zomper
    def navigateToEditGalleyPage(self, galleryName):
        if self.navigateToGallery(galleryName) == False:
            writeToLog("INFO","FAILED navigate to gallery page")
            return False
        
        if self.click(self.clsCommon.channel.CHANNEL_EDIT_DROP_DOWN_MENU,timeout=20) == False:
            writeToLog("INFO","FAILED to Click on action menu button")
            return False  
        sleep(2)
        
        if self.click(self.clsCommon.channel.CHANNEL_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to Click on edit drop down menu")
            return False  
        sleep(2)
    
        return True
    
    
    # Author: Michal Zomper
    def editGalleryMatedate(self, galleryName, newGallerydescription="", newGalleryTags=""):
        if self.navigateToEditGalleyPage(galleryName) == False:
            writeToLog("INFO","FAILED navigate to ediat gallery page")    
            return False
        
        if newGallerydescription != "":
            if self.clsCommon.category.fillCategoryDescription(newGallerydescription, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace channel description to:'" + newGallerydescription + "'")    
                return False
        
        if newGalleryTags != "":
            if self.clsCommon.category.fillCategoryTags(newGalleryTags, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace channel tags to:'" + newGalleryTags + "'")    
                return False   
            
        # Click Save
        if self.click(self.clsCommon.category.EDIT_CATEGORY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()        
        
        writeToLog("INFO","Success, media gallery metadata was changed successfully")
        return True
    
    
    # Author: Michal Zomper   
    def varifyGalleyMatedate(self, galleryName, galleryDescription, galleryTags):
        if self.navigateToGallery(galleryName, forceNavigate=True) == False:
            writeToLog("INFO","FAILED navigate to  gallery page")    
            return False
        
        tmpGalleryDescription = (self.clsCommon.category.CATEGORY_DESCRIPTION[0], self.clsCommon.category.CATEGORY_DESCRIPTION[1].replace('CATEGORY_DESCRIPTION', galleryDescription))
        if self.wait_visible(tmpGalleryDescription, 30) == False:
            writeToLog("INFO","FAILED to verify gallery description")
            return False
        
        tmpGalleryTags = (self.clsCommon.category.CATEGORY_TAGS[0], self.clsCommon.category.CATEGORY_TAGS[1].replace('CATEGORY_TAGS', galleryTags[:-1]))
        if self.wait_visible(tmpGalleryTags, 30) == False:
            writeToLog("INFO","FAILED to verify gallery tags")
            return False
        
        writeToLog("INFO","Success, media gallery metadata was verified successfully")
        return True
    
    
    # @Author: Inbar Willman
    def logOutOfKAF(self):
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
#             if self.clsCommon.blackBoard.logOutOfBB() == False:
#                 writeToLog("INFO","FAILED to log out from BB)
#                 return False 
#             
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
            if self.clsCommon.moodle.logOutOfMoodle() == False:
                writeToLog("INFO","FAILED navigate to log out from moodle")
                return False 
#             
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
#             if self.clsCommon.canvas.navigateToGalleryCanvas(forceNavigate) == False:
#                 writeToLog("INFO","FAILED navigate to media gallery")
#                 return False 
#         
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
#             if self.clsCommon.d2l.navigateToGalleryD2L(galleryName, forceNavigate) == False:
#                 writeToLog("INFO","FAILED navigate to media gallery")
#                 return False   
#             
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
#             if self.clsCommon.jive.navigateToGalleryJive(galleryName, forceNavigate) == False:
#                 writeToLog("INFO","FAILED navigate to media gallery")
#                 return False 
#         
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
#             if self.clsCommon.sakai.navigateToGallerySakai(galleryName, forceNavigate) == False:
#                 writeToLog("INFO","FAILED navigate to media gallery")
#                 return False 
# 
#         if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
#             if self.clsCommon.sharePoint.navigateToGallerySharePoint(galleryName, forceNavigate) == False:
#                 writeToLog("INFO","FAILED navigate to media gallery")
#                 return False  

        return True