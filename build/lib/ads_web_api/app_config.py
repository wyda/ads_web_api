import logging
import jsonpickle


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
            with open(config_file, 'r') as paramFile:                               
                return jsonpickle.decode(paramFile.read())                           
        except FileNotFoundError:            
            logger.warning('No valid param file available! Creating empty parameter file...')

            with open(config_file, 'w') as paramFile:   
                paramFile.write(jsonpickle.encode(self))
                logger.debug('...new parameter file created')        
            logger.debug('return empty parameter file!')    
            return self.load(config_file) 

    def load_api(self, api_file):
        logger = logging.getLogger('AppConfig')        
        try:                        
            logger.info(api_file)
            with open(api_file, 'r') as paramFile:                               
                return jsonpickle.decode(paramFile.read())                           
        except FileNotFoundError:
            logger.error('No valid api file available!')
            with open(api_file, 'w') as api_file:       
                logger.debug('...new empty api file created')
            logger.debug('return empty api file!')
            raise Exception("No valid api description found!")
