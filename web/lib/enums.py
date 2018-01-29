from enum import Enum

class ChannelPrivacyType(Enum):
    def __str__(self):
        return str(self.value)

    OPEN               = 'open'       
    RESTRICTED         = "restricted"
    PRIVATE            = "private"
    SHAREDREPOSITORY   = "sharedrepository"
    PUBLIC             = "public"
    
    
class DisclaimerDisplayArea(Enum):
    def __str__(self):
        return str(self.value)

    BEFORE_UPLOAD          = 'Before Upload'       
    BEFORE_PUBLISH         = 'Before Publish'


class PublishFrom(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA               = 'my media'
    ENTRY_PAGE             = 'entry page'
    UPLOAD_PAGE            = 'upload page'


class EditEntryPageTabName(Enum):
    def __str__(self):
        return str(self.value)
    
    OPTIONS                = 'options'
    COLLABORATION          = 'collaboration'
    THUMBNAILS             = 'thumbnails'
    CAPTIONS               = 'captions'
    DOWNLOADS              = 'downloads'
    TIMELINE               = 'timeline'
    
     

