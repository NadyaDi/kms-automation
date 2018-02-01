import enums
from base import *
import clsTestService
from general import General


class MyPlaylists(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Playlist locators:
    #=============================================================================================================
    CREATE_PLAYLIST_TEXT_FIELD               = ('xpath' ,"//input[@value='Create new playlist']")
    CREATE_PLAYLIST_CREATE_BUTTON            = ('xpath', "//button[@id='playlistAddButton']")
    CREATE_PLAYLIST_SAVE_BUTTON              = ('xpath', "//button[@id='playlists-submit']")
    CREATE_PLAYLIST_CONFIRM_MSG              = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'Now your selected media is part of the selected playlist(s).')]")
    PLAYLIST_CHECKBOX                        = ('xpath', "//span[text() = 'PLAYLIST_NAME']")
    PLAYLIST_NAME                            = ('xpath', "//a[contains(@data-original-title,'PLAYLIST_NAME')]")
    PLAYLIST_DELETE_BUTTON                   = ('xpath', "//i[contains(@class,'icon-trash')]")
    PLAYLIST_DELETE_BUTTON_CONFIRM           = ('xpath', "//a[@class='btn btn-danger']")
    PLAYLIST_ENTRY_NAME_IN_PLAYLIST          = ('xpath', "//a[contains(@href,'/media/') and contains(text(), 'ENTRY_NAME')]")
    #============================================================================================================

    # TODO BOM add description and how to use (playlistName....)
    def addSingleEntryToPlaylist(self, entryName, playlistName='', toCreateNewPlaylist = False, currentLocation = enums.Location.MY_MEDIA):
        try:
            if currentLocation == enums.Location.MY_MEDIA: 
                if self.clsCommon.myMedia.navigateToMyMedia() == False:
                    writeToLog("INFO","FAILED to navigate to my media")
                    return False
                
                if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                    return False
             
                if self.clsCommon.myMedia.clickActionsAndAddToPlaylistFromMyMedia() == False:
                    writeToLog("INFO","FAILED to click on action button")
                    return False
                    sleep(7)  
                      
            elif currentLocation == enums.Location.ENTRY_PAGE: 
                sleep(1)
                # Click on action tab
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                    writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                    return False  
                
                sleep(1)
                # Click on publish button
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ADDTOPLAYLIST_BUTTON, 30) == False:
                    writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                    return False
            
            else:
                writeToLog("INFO","FAILED, Add entry to playlist: the provided ""currentLocation"" Value is not accepted ")
                return False
            
            
            if toCreateNewPlaylist != False:
                self.clear_and_send_keys(self.CREATE_PLAYLIST_TEXT_FIELD, playlistName)
                sleep(1)
            
                if self.click(self.CREATE_PLAYLIST_CREATE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                
                sleep(1)
                if self.click(self.CREATE_PLAYLIST_SAVE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                if self.wait_visible(self.CREATE_PLAYLIST_CONFIRM_MSG, 10) == False:
                    writeToLog("INFO","FAILED to create playlist, Playlist name: " + playlistName + "")
                    return False
                
                writeToLog("INFO","Playlist: " + playlistName + " successfully created")
            
            else:
                tmp_playlist_name = (self.PLAYLIST_CHECKBOX[0], self.PLAYLIST_CHECKBOX[1].replace('PLAYLIST_NAME', playlistName))   
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to Check for playlist: '" + playlistName + "' something went wrong")
                    return False
                
                if self.click(self.CREATE_PLAYLIST_SAVE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                sleep(1)
                
                if self.wait_visible(self.CREATE_PLAYLIST_CONFIRM_MSG, 10) == False:
                    writeToLog("INFO","FAILED to add entry: " + entryName + " to Playlist: " + playlistName )
                    return False
                
                writeToLog("INFO","Entry: """ + entryName + """ added to Playlist: """ + playlistName + "")
                                       
        except NoSuchElementException:
            return False
            
        return True
    
    
    def navigateToMyPlaylists(self, forceNavigate = False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL, False, 1) == True:
                writeToLog("INFO","Success Already in my playlists page")
                return True
        
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Media
        if self.click(self.clsCommon.general.USER_MENU_MY_PLAYLISTS_BUTTON) == False:
            writeToLog("INFO","FAILED to on My playlists from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My playlists")
            return False
        
        return True
    
    
    def deletePlaylist(self, playlistName):
        try:
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False
    

                if self.click(self.PLAYLIST_DELETE_BUTTON, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on playlist delete button (at my playlist page)")
                    return False
                
                sleep(2)
                if self.click(self.PLAYLIST_DELETE_BUTTON_CONFIRM, 30) == False:
                    writeToLog("INFO","FAILED to click on delete button confirmation, playlist name: '" + playlistName + "'")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                
                tmp_playlist_name_after_delete = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name_after_delete, timeout=3) == False:
                    writeToLog("INFO","Playlist: '" + playlistName + "' Was Deleted")
                    return True
                        
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlistName")
                return False
                        
        except NoSuchElementException:
            return False
            
        return True
    
    
    def verifySingleEntryInPlaylist(self, playlistName, entryName, isExpected=True):
        try:                
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False

                tmp_entry_name = (self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[0], self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[1].replace('ENTRY_NAME', entryName))
                if self.wait_visible(tmp_entry_name, 5) != False:
                    if isExpected == True:
                        writeToLog("INFO","As Expected: Entry was found in the Playlists")
                        return True
                    else:
                        writeToLog("INFO","NOT Expected: Entry was found in the Playlists")
                        return False
                else:
                    if isExpected == False:
                        writeToLog("INFO","As Expected: Entry was not found in the Playlists")
                        return True
                    else:
                        writeToLog("INFO","NOT Expected: Entry wasn't found in the Playlists")
                        return False                    
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlistName")
                return False                
                
        except NoSuchElementException:
            return False
            
        return True   