from pathlib import Path
import logging
from ads_web_api.db import get_db
class AdsConfig():
    def __init__(self):          
        self.ams_port = 851
        self.ams_address = ""
        self.log_level = logging.NOTSET                         

    def load_config(self):
        logger = logging.getLogger('ads config')
        logger.debug('get db')
        db = get_db()
        logger.debug('load ads config from db')
        config=db.execute(
            'SELECT * FROM ads_config WHERE id = ?', (1,)
        ).fetchone()

        self.ams_port = config['port']
        self.ams_address = config['ams_address']
        self.log_level = config['log_level']
        return self
