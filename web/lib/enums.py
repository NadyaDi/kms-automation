from enum import Enum


class Application(Enum):
    def __str__(self):
        return str(self.value)

    MEDIA_SPACE         = 'Media Space'
    BLACK_BOARD         = 'Black Board'       
    CANVAS              = 'Canvas'
    MOODLE              = 'Moodle'
    D2L                 = 'D2L'
    JIVE                = 'Jive'
    SHARE_POINT         = 'Share Point'
    SAKAI               = 'Sakai'


class ChannelPrivacyType(Enum):
    def __str__(self):
        return str(self.value)

    OPEN                = 'open'       
    RESTRICTED          = "restricted"
    PRIVATE             = "private"
    SHAREDREPOSITORY    = "sharedrepository"
    PUBLIC              = "public"
    UNLISTED            = "Unlisted"
    
    
class DisclaimerDisplayArea(Enum):
    def __str__(self):
        return str(self.value)

    BEFORE_UPLOAD        = 'Before Upload'       
    BEFORE_PUBLISH       = 'Before Publish'


class Location(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA               = 'my media'
    ENTRY_PAGE             = 'entry page'
    UPLOAD_PAGE            = 'upload page'
    CHANNEL_PAGE           = 'channel page'
    CATEGORY_PAGE          = 'category page'
    MY_CHANNELS_PAGE       = 'my channels page'
    CHANNELS_PAGE          = 'channels page'
    MY_PLAYLISTS           = 'my playlists'
    EDIT_ENTRY_PAGE        = 'edit entry page'
    MY_HISTORY             = 'my history'
    PENDING_TAB            = 'channel - Pending tab' 
    HOME                   = 'home'


class EditEntryPageTabName(Enum):
    def __str__(self):
        return str(self.value)
    
    
    DETAILS                = 'details'
    OPTIONS                = 'options'
    COLLABORATION          = 'collaboration'
    THUMBNAILS             = 'thumbnails'
    CAPTIONS               = 'captions'
    DOWNLOADS              = 'downloads'
    TIMELINE               = 'timeline'
    
    
class IframeName(Enum):
    def __str__(self):
        return str(self.value)

    DEFAULT                             = 'DEFAULT'
    PLAYER                              = 'PLAYER'
    KEA                                 = 'KEA'
    KEA_QUIZ_PLAYER                     = 'KEA_QUIZ_PLAYER'
    EMBED_PLAYER                        = 'EMBED_PLAYER'
    KAF_BLACKBOARD                      = 'KAF_BLACKBOARD'
    
    
class PlayerView(Enum):
    def __str__(self):
        return str(self.value)
    
    PIP                = 'pip'
    SIDEBYSIDE         = 'sideBySide' 
    SINGLEVIEW         = 'singleView'
    SWITCHVIEW         = 'switchView'
    
    
class EntryPrivacyType(Enum):
    def __str__(self):
        return str(self.value)
    
    ALL_STATUSSES      = 'All Statuses'
    PRIVATE            = 'Private'       
    UNLISTED           = "Unlisted"
    PUBLISHED          = "Published"
    PENDING            = "Pending"
    REJECTED           = "Rejected"
    
    
class SortBy(Enum):
    def __str__(self):
        return str(self.value)

    MOST_RECENT             = 'Most Recent'  
    VIEWS                   = 'Views'
    LIKES                   = 'Likes'
    ALPHABETICAL            = "Alphabetical"
    COMMENTS                = "Comments"
    SCHEDULING_ASC          = "Scheduling Ascending"
    SCHEDULING_DESC         = "Scheduling Descending" 
    
    
class MediaType(Enum):
    def __str__(self):
        return str(self.value)

    ALL_MEDIA               = 'All Media'  
    VIDEO                   = 'Video'      
    QUIZ                    = "Quiz"
    AUDIO                   = "Audio"
    IMAGE                   = "Image"
    
    
class Collaboration(Enum):
    def __str__(self):
        return str(self.value)

    MEDIA_I_OWN               = 'Media I Own'  
    CO_PUBLISH                = 'Media I Can Publish'      
    CO_EDIT                   = "Media I Can Edit"
    
    
class Scheduling(Enum):
    def __str__(self):
        return str(self.value)

    ALL                       = 'All Availabilities'  
    FUTURE_SCHEDULING         = 'Future Scheduling'      
    AVAILABLE_NOW             = "Available Now"
    PAST_SCHEDULING           = "Past Scheduling" 


class SortAndFilter(Enum):
    def __str__(self):
        return str(self.value)

    SORT_BY                   = 'Sort by'  
    PRIVACY                   = 'Privacy Type'      
    MEDIA_TYPE                = "MediaType"
    COLLABORATION             = "Collaboration"
    SCHEDULING                = 'Scheduling'
    

class KeaQuizButtons(Enum):
    def __str__(self):
        return str(self.value)

    SAVE                       = 'Save'  
    DELETE                     = 'Delete'      
    START                      = 'Start'
    DONE                       = 'Done'
    GO_TO_MEDIA_PAGE           = 'Go to Media Page'
    EDIT_QUIZ                  = 'Edit Quiz'

    
class PlayerPart(Enum):
    def __str__(self):
        return str(self.value)

    TOP                       = 'top'  
    BOTTOM                    = 'bottom'
    

class ProgressBarStatus(Enum):
    def __str__(self):
        return str(self.value)
    
    COMPLETE                  = 'Complete'  
    STARTED                   = 'Started'


class EntryPageShareOptions(Enum):
    def __str__(self):
        return str(self.value)
    
    LINK_TO_MEDIA_PAGE      = 'Link to Media Page'  
    EMBED                   = 'Embed'
    EMAIL                   = 'Email'