import logging
#import pyads
from . import app_init
from flask import g, current_app
from flask.cli import with_appcontext
#from multiprocessing import Process, Queue

class AdsClient():
    def start(self):                              
        self.app_config = app_init.load_config()     
        print(type(self.app_config))   
        logging.basicConfig(filename='app.log', encoding='utf-8', 
                            level=self.app_config.log_level, 
                            format='%(asctime)s %(message)s')                
                
        logging.info('App started')                   

def init_ads(app):
    with app.app_context():        
        ads_client = AdsClient()
        g.ads = ads_client
        g.ads.start()        