import logging
import pyads
from .ads_config import AdsConfig

class AdsClient():
    def __init__(self):                              
        self.ads_config = AdsConfig()
        self.ads_config.load_config()                     
        logger = logging.getLogger('ads client')      

        self.plc = pyads.Connection(self.ads_config.ams_address, self.ads_config.ams_port)
        self.plc.open()
        logger.info('ads client started')