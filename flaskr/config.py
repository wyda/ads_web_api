import logging
import jsonpickle


class AppConfig():
    def __init__(self):        
        self.ams_port = 851
        self.ams_address = ""
        self.log_level = 0
        self.allow_var_req = False               

    def load(self, config_file):
        try:                        
            with open(config_file) as paramFile:                               
                return jsonpickle.decode(paramFile.read())                           
        except FileNotFoundError:            
            logging.info('No valid param file available! Creating empty parameter file...')

            with open(config_file, 'w') as paramFile:   
                paramFile.write(jsonpickle.encode(self))
                logging.debug('...new parameter file created')
            return self.load(config_file)               