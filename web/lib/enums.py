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
    BEFORE_PUBLISH         = "Before Publish"
