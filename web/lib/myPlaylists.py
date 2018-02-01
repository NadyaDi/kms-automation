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
    PLAYLIAT_CHECKBOX                        = ('xpath', "//span[text() = 'PLAYLIST_NAME']")
    #============================================================================================================

    
    def addSingleEntryToPlaylist(self, entryName, playlistName='', toCreateNewPlaylist = False, From = enums.Location.MY_MEDIA):
        try:
            if From == enums.Location.MY_MEDIA: 
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
                      
            elif From == enums.Location.ENTRY_PAGE: 
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
                writeToLog("INFO","FAILED, Add entry to playlist: the provided ""From"" Value is not accepted ")
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
                tmp_playlist_name = (self.PLAYLIAT_CHECKBOX[0], self.PLAYLIAT_CHECKBOX[1].replace('PLAYLIST_NAME', playlistName))   
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to Check for playlist: '" + playlistName + "' something went wrong")
                    return False
        
                                       
        except NoSuchElementException:
            return False
            
        return True