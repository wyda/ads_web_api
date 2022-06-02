import logging
import pyads
from . import ads_init

class AdsClient():
    def __init__(self):                              
        self.ads_config = ads_init.load_config()          
        logging.basicConfig(filename='app.log', encoding='utf-8', 
                            level=self.ads_config.log_level, 
                            format='%(asctime)s %(message)s')                

        self.plc = pyads.Connection(self.ads_config.ams_address, self.ads_config.ads_port)
        self.plc.open()
        logging.info('ads client started')