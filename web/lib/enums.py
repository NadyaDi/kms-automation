from enum import Enum

class AdType(Enum):
    def __str__(self):
        return str(self.value)

    DFP                     = "DFP"        
    DFP_PREROLL             = "DfpPreroll"
    DFP_OVERLAY             = "DfpOverlay"
    DFP_OVERLAY_COMPANION   = "DfpOverlayCompanion"
    VAST                    = "Vast"
    BUMPER                  = "Bumper"
 
class entryType(Enum):
    
    def __str__(self):
        return str(self.value)
    
    ENTRY_TYPE_AUDIO                   = "AUDIO"
    ENTRY_TYPE_VIDEO                   = "VIDEO"
    ENTRY_TYPE_LIVE_KALTURA_WITH_DVR   = "LIVE_KALTURA_WITH_DVR"
    ENTRY_TYPE_LIVE_KALTURA            = "LIVE_KALTURA"
    ENTRY_TYPE_LIVE_UNIVERSAL          = "LIVE_UNIVERSAL"
    ENTRY_TYPE_LIVE_UNIVERSAL_WITH_DVR = "LIVE_UNIVERSAL_WITH_DVR"