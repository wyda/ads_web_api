from pathlib import Path
import jsonpickle
import logging
from flaskr.db import get_db, g
class AdsConfig():
    def __init__(self):                
        self.ads_port = 851
        self.ams_address = ""            
        self.log_level = logging.NOTSET                         

    def load_config(self):
        if not 'db' in g:
            logging.info('loading db in AdsConfig')
            g.db = get_db()           

        config=g.db.execute(
            'SELECT * FROM ads_config WHERE id = ?', (1,)
        ).fetchone()        

        self.ads_port = config['port']
        self.ams_address = config['ams_address']
        self.log_level = config['log_level']
        return self
