import logging
import jsonpickle
from flask import current_app


class AppConfig():
    def __init__(self):        
        self.ams_port = 851
        self.ams_address = ""
        self.log_level = 0
        self.allow_var_req = False   
        self.omit_var_name = True            

    def load(self, config_file):
        logger = logging.getLogger('AppConfig')

        try:                        
            with current_app.open_resource(config_file, 'r') as f:                              
                return jsonpickle.decode(f.read())                           
        except FileNotFoundError:            
            logger.warning('No valid param file available! Creating empty parameter file...')

            with current_app.open_resource(config_file, 'w') as f: 
                f.write(jsonpickle.encode(self))
                logger.info('...new parameter file created')        
            logger.info('return empty parameter file!')    
            return self.load(config_file)

    def load_api(self, api_file):
        logger = logging.getLogger('AppConfig')        
        try:                        
            logger.info(api_file)
            with current_app.open_resource(api_file, 'r') as f:                                
                return jsonpickle.decode(f.read())                           
        except FileNotFoundError:            
            logger.error('No valid api file available!')
            with current_app.open_resource(api_file, 'w') as f:                                
                logger.info('...new empty api file created')
            logger.info('return empty api file (api.json)! Add API description to this file!')
            raise Exception("No valid api description found!")
          
